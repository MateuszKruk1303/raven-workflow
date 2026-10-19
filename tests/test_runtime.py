import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('runtime', ROOT / 'skills/raven-workflow/scripts/raven_runtime.py')
runtime = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runtime)


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / 'repo'
        self.repo.mkdir()
        runtime.git(self.repo, 'init', '-b', 'main')
        runtime.git(self.repo, 'config', 'user.email', 'test@example.test')
        runtime.git(self.repo, 'config', 'user.name', 'Test')
        self.plan = self.repo / 'context/changes/C-01/plan.md'
        self.plan.parent.mkdir(parents=True)
        self.plan.write_text(runtime.START + '\nAC one; implementation step S1\n' + runtime.END + '\n- [ ] S1\n')
        config = self.repo / '.raven/config.json'
        config.parent.mkdir()
        config.write_text(json.dumps({'schema_version': 1, 'repository': {'owner': 'owner', 'name': 'repo', 'base_branch': 'main'}, 'publication': {'mode': 'draft-pr', 'authorized_by': None}}))
        runtime.git(self.repo, 'add', '.')
        runtime.git(self.repo, 'commit', '-m', 'initial')
        self.r = runtime.Runtime(self.repo, 'C-01')

    def issue_api(self):
        config = self.repo / '.raven/config.json'
        value = json.loads(config.read_text())
        value['tracker'] = {'type': 'github-issues', 'labels': {'in_progress': 'in-progress', 'blocked': 'blocked'}}
        config.write_text(json.dumps(value))
        class API:
            def __init__(api):
                api.value = {'number': 12, 'html_url': 'https://github.com/owner/repo/issues/12',
                             'title': 'Task', 'body': 'Requirements', 'state': 'open', 'labels': [{'name': 'feature'}], 'assignees': []}
                api.calls = []
                api.timeout = False
                api.accept = True
                api.pr = {'number': 7, 'merged': True, 'state': 'closed',
                          'body': '<!-- raven-change:C-01 -->\n<!-- raven-issue:owner/repo#12 -->\nhttps://github.com/owner/repo/issues/12',
                          'base': {'ref': 'main', 'repo': {'full_name': 'owner/repo'}},
                          'head': {'repo': {'full_name': 'owner/repo'}}}
            def request(api, method, endpoint, payload=None):
                api.calls.append((method, endpoint, payload))
                if '/pulls/' in endpoint:
                    return api.pr
                if method == 'PATCH':
                    if api.accept:
                        api.value.update(json.loads(json.dumps(payload)))
                        if 'assignees' in payload:
                            api.value['assignees'] = [{'login': x} for x in payload['assignees']]
                    if api.timeout:
                        raise ValueError('timeout')
                return json.loads(json.dumps(api.value))
        return API()

    def test_issue_start_noop_preserves_labels_and_binds_checkpoint(self):
        api = self.issue_api()
        result = self.r.issue(12, 'start', 's1', 'alice', apply=True, api=api)
        self.assertTrue(result['changed'])
        self.assertEqual(api.value['labels'], ['feature', 'in-progress'])
        result = self.r.issue(12, 'start', 's2', 'alice', apply=True, api=api)
        self.assertFalse(result['changed'])
        self.assertEqual([x[0] for x in api.calls], ['GET', 'PATCH', 'GET', 'GET'])
        digest = self.r.digest()
        self.assertEqual(self.r.checkpoint('s3', 'plan', 'review')['checkpoint']['issue'], result['url'])
        self.assertEqual(digest, self.r.digest())

    def test_issue_start_never_steals_owner_or_accepts_pr(self):
        api = self.issue_api()
        for extra in ({'assignees': [{'login': 'bob'}]}, {'pull_request': {}}, {'state': 'closed'}):
            original = api.value.copy()
            api.value.update(extra)
            with self.assertRaises(ValueError):
                self.r.issue(12, 'start', 's1', 'alice', apply=True, api=api)
            api.value = original
        self.assertTrue(all(call[0] == 'GET' for call in api.calls))

    def test_issue_block_reason_is_bounded_managed_and_noop(self):
        api = self.issue_api()
        self.r.issue(12, 'block', 's1', reason='Waiting for API', apply=True, api=api)
        self.assertTrue(api.value['body'].startswith('Requirements'))
        self.assertEqual(set(api.value['labels']), {'feature', 'blocked', 'in-progress'})
        self.assertFalse(self.r.issue(12, 'block', 's2', reason='Waiting for API', apply=True, api=api)['changed'])
        self.r.issue(12, 'block', 's3', reason='Waiting for owner', apply=True, api=api)
        self.assertNotIn('Waiting for API', api.value['body'])
        self.assertEqual(api.value['body'].count('raven:block:start'), 1)

    def test_issue_merge_gates_done_and_preserves_other_data(self):
        api = self.issue_api()
        self.r.issue(12, 'start', 's1', 'alice', apply=True, api=api)
        for key, value in (('merged', False), ('state', 'open'), ('body', 'Closes #12')):
            old = api.pr[key]
            api.pr[key] = value
            with self.assertRaisesRegex(ValueError, 'confirmed merged PR'):
                self.r.issue(12, 'merge', 's2', pr=7, apply=True, api=api)
            api.pr[key] = old
        result = self.r.issue(12, 'merge', 's3', pr=7, apply=True, api=api)
        self.assertEqual(result['state'], 'done')
        self.assertEqual(api.value['state_reason'], 'completed')
        self.assertEqual(api.value['labels'], ['feature'])
        self.assertEqual(api.value['assignees'], [{'login': 'alice'}])
        self.assertFalse(self.r.issue(12, 'merge', 's4', pr=7, apply=True, api=api)['changed'])

    def test_issue_merge_rejects_conflicting_checkpoint_or_publication_pr(self):
        for source in ('checkpoint', 'publication-url', 'publication-number'):
            with self.subTest(source=source):
                api = self.issue_api()
                self.r.save({'schema_version': 1, 'change': 'C-01'})
                if source == 'checkpoint':
                    self.r.save({'publication': {'url': 'https://github.com/owner/repo/pull/99'}})
                    self.r.checkpoint('s0', 'merge', 'done')
                    self.r.save({'schema_version': 1, 'change': 'C-01'})
                elif source == 'publication-url':
                    self.r.save({'publication': {'url': 'https://github.com/owner/repo/pull/99'}})
                else:
                    self.r.save({'publication': {'number': 99}})
                with self.assertRaisesRegex(ValueError, 'canonical checkpoint/publication'):
                    self.r.issue(12, 'merge', 's1', pr=7, apply=True, api=api)
                self.assertEqual(api.calls, [])
                self.plan.write_text(runtime.START + '\nAC one; implementation step S1\n' + runtime.END + '\n- [ ] S1\n')

    def test_issue_merge_pending_recovery_allows_base_tip_to_advance(self):
        api = self.issue_api()
        api.pr['head'].update(ref='raven/C-01', sha='head-sha')
        api.pr['base']['sha'] = 'old-base-tip'
        api.timeout = True
        with self.assertRaisesRegex(ValueError, 'timeout'):
            self.r.issue(12, 'merge', 's1', pr=7, apply=True, api=api)
        self.assertEqual(api.value['state'], 'closed')
        api.pr['base']['sha'] = 'new-base-tip'
        result = self.r.issue(12, 'merge', 's2', pr=7, apply=True, api=api)
        self.assertEqual(result['state'], 'done')
        self.assertEqual(sum(c[0] == 'PATCH' for c in api.calls), 1)
        self.assertNotIn('sha', result['pr_identity']['base'])
        self.assertEqual(result['pr_identity']['head']['sha'], 'head-sha')

    def test_issue_merge_explicit_reconcile_allows_new_base_tip_after_failed_write(self):
        api = self.issue_api()
        self.r.save({'publication': {'url': 'https://github.com/owner/repo/pull/7', 'number': 7}})
        self.r.checkpoint('s0', 'merge', 'done')
        api.pr['head'].update(ref='raven/C-01', sha='head-sha')
        api.pr['base']['sha'] = 'old-base-tip'
        api.timeout, api.accept = True, False
        with self.assertRaisesRegex(ValueError, 'timeout'):
            self.r.issue(12, 'merge', 's1', pr=7, apply=True, api=api)
        api.pr['base']['sha'] = 'new-base-tip'
        api.timeout, api.accept = False, True
        result = self.r.issue(12, 'merge', 's2', pr=7, apply=True, api=api, reconcile=True)
        self.assertEqual(result['state'], 'done')
        self.assertEqual(sum(c[0] == 'PATCH' for c in api.calls), 2)

    def test_issue_merge_pending_recovery_rejects_changed_head(self):
        api = self.issue_api()
        api.pr['head'].update(ref='raven/C-01', sha='head-sha')
        api.timeout = True
        with self.assertRaises(ValueError):
            self.r.issue(12, 'merge', 's1', pr=7, apply=True, api=api)
        api.pr['head']['sha'] = 'another-head'
        with self.assertRaisesRegex(ValueError, 'PR identity/head changed'):
            self.r.issue(12, 'merge', 's2', pr=7, apply=True, api=api)
        self.assertEqual(sum(c[0] == 'PATCH' for c in api.calls), 1)

    def test_issue_pending_timeout_recovers_without_second_write(self):
        api = self.issue_api()
        api.timeout = True
        with self.assertRaisesRegex(ValueError, 'timeout'):
            self.r.issue(12, 'start', 's1', 'alice', apply=True, api=api)
        self.assertEqual(self.r.journal()['issue']['state'], 'pending')
        result = self.r.issue(12, 'start', 's2', 'alice', apply=True, api=api)
        self.assertEqual(result['state'], 'started')
        self.assertEqual(sum(c[0] == 'PATCH' for c in api.calls), 1)

    def test_issue_pending_absence_or_new_intent_never_retries(self):
        api = self.issue_api()
        api.timeout, api.accept = True, False
        with self.assertRaises(ValueError):
            self.r.issue(12, 'start', 's1', 'alice', apply=True, api=api)
        for event, kwargs in (('start', {'assignee': 'alice'}), ('block', {'reason': 'blocked'})):
            with self.assertRaisesRegex(ValueError, 'Pending'):
                self.r.issue(12, event, 's2', apply=True, api=api, **kwargs)
        self.assertEqual(sum(c[0] == 'PATCH' for c in api.calls), 1)

    def test_issue_explicit_reconcile_uses_fresh_state_and_stops_at_two_writes(self):
        api = self.issue_api()
        api.timeout, api.accept = True, False
        for reconcile in (False, True, True):
            with self.assertRaises(ValueError):
                self.r.issue(12, 'start', 's1', 'alice', apply=True, api=api, reconcile=reconcile)
            api.value['labels'] = [{'name': 'feature'}, {'name': 'new-unrelated'}]
        writes = [c for c in api.calls if c[0] == 'PATCH']
        self.assertEqual(len(writes), 2)
        self.assertIn('new-unrelated', writes[-1][2]['labels'])

    def test_issue_reconcile_rejects_changed_owner(self):
        api = self.issue_api()
        api.timeout, api.accept = True, False
        with self.assertRaises(ValueError):
            self.r.issue(12, 'start', 's1', 'alice', apply=True, api=api)
        api.value['assignees'] = [{'login': 'bob'}]
        with self.assertRaisesRegex(ValueError, 'conflicting assignee'):
            self.r.issue(12, 'start', 's1', 'alice', apply=True, api=api, reconcile=True)
        self.assertEqual(sum(c[0] == 'PATCH' for c in api.calls), 1)

    def test_start_and_merge_clear_managed_block_reason(self):
        api = self.issue_api()
        self.r.issue(12, 'block', 's1', reason='Wait', apply=True, api=api)
        self.r.issue(12, 'start', 's2', 'alice', apply=True, api=api)
        self.assertEqual(api.value['body'], 'Requirements')
        self.assertNotIn('blocked', api.value['labels'])
        self.r.issue(12, 'block', 's3', reason='Wait again', apply=True, api=api)
        self.r.issue(12, 'merge', 's4', pr=7, apply=True, api=api)
        self.assertEqual(api.value['body'], 'Requirements')

    def test_block_rejects_foreign_owner_without_started_binding(self):
        api = self.issue_api()
        api.value['assignees'] = [{'login': 'bob'}]
        with self.assertRaisesRegex(ValueError, 'ownership'):
            self.r.issue(12, 'block', 's1', reason='Wait', apply=True, api=api)
        self.assertEqual(sum(c[0] == 'PATCH' for c in api.calls), 0)

    def test_issue_readback_checks_owner_even_when_owner_not_patched(self):
        api = self.issue_api()
        self.r.issue(12, 'start', 's1', 'alice', apply=True, api=api)
        original = api.request
        def request(method, endpoint, payload=None):
            result = original(method, endpoint, payload)
            if method == 'PATCH':
                api.value['assignees'] = [{'login': 'bob'}]
            return result
        api.request = request
        with self.assertRaisesRegex(ValueError, 'readback failed'):
            self.r.issue(12, 'block', 's2', reason='Wait', apply=True, api=api)
        self.assertEqual(self.r.journal()['issue']['state'], 'pending')

    def test_issue_read_and_dry_run_are_targeted_and_readonly(self):
        api = self.issue_api()
        self.r.issue(12, 'start', 's1', 'alice', api=api)
        self.assertEqual(api.calls, [])
        self.r.issue(12, api=api)
        self.assertEqual([(m, e) for m, e, _ in api.calls], [('GET', '/repos/owner/repo/issues/12')])
        self.assertFalse(self.r.state.exists())

    def test_contract_change_invalidates_checkpoint_progress_does_not(self):
        self.r.checkpoint('s1', 'plan', 'implement')
        self.plan.write_text(self.plan.read_text().replace('[ ]', '[x]'))
        self.assertTrue(self.r.status()['contract_current'])
        self.plan.write_text(self.plan.read_text().replace('implementation step S1', 'implementation step S2'))
        self.assertFalse(self.r.status()['contract_current'])
        self.assertNotIn('acceptance', self.r.journal()['checkpoint'])

    def test_new_plan_can_checkpoint_without_acceptance_or_automatic_execution(self):
        source = self.repo / 'product.py'
        source.write_text('value = 1\n')
        before = source.read_bytes()
        item = self.r.checkpoint('planner', 'plan-review', 'raven-auto-implement C-01')['checkpoint']
        self.assertNotIn('acceptance', item)
        self.assertNotIn('user_acceptance', item)
        self.assertEqual(item['stage'], 'plan-review')
        self.assertEqual(source.read_bytes(), before)

    def test_stale_plan_review_fingerprint_remains_stale_after_checkpoint(self):
        review = {'fingerprint': self.r.digest(), 'result': 'PASS', 'path': 'plan-review.md'}
        self.plan.write_text(self.plan.read_text() + '\n' + runtime.CHECK_START + '\n'
                             + json.dumps({'plan_review': review}) + '\n' + runtime.CHECK_END + '\n')
        self.plan.write_text(self.plan.read_text().replace('AC one', 'AC revised'))
        item = self.r.checkpoint('implementer', 'implement', 'refresh plan review')['checkpoint']
        self.assertEqual(item['plan_review'], review)
        self.assertNotEqual(item['fingerprint'], item['plan_review']['fingerprint'])
        self.assertNotIn('acceptance', item)

    def test_removed_acceptance_cli_is_rejected_without_mutation(self):
        before = self.plan.read_bytes()
        result = subprocess.run([sys.executable, str(SPEC.origin), '--repo', str(self.repo),
                                 'checkpoint', 'C-01', '--session', 's1', '--stage', 'implement',
                                 '--next', 'test', '--acceptance-ref', 'old-decision'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('unrecognized arguments', result.stderr)
        self.assertEqual(self.plan.read_bytes(), before)
        self.assertFalse(self.r.state.exists())

    def test_fingerprint_normalizes_line_endings_but_not_contract_spacing(self):
        text = self.plan.read_text()
        self.assertEqual(runtime.fingerprint(text), runtime.fingerprint(text.replace('\n', '\r\n')))
        self.assertNotEqual(runtime.fingerprint(text), runtime.fingerprint(text.replace('AC one', 'AC  one')))
        with self.assertRaises(ValueError):
            runtime.fingerprint(text + runtime.START)

    def test_unsafe_identity_and_symlink_plan_rejected(self):
        for identifier in ('../escape', '/tmp/x', 'x/y', '--help'):
            with self.assertRaises(ValueError):
                runtime.Runtime(self.repo, identifier)
        self.plan.unlink()
        self.plan.symlink_to(Path(self.tmp.name) / 'outside')
        with self.assertRaises(ValueError):
            runtime.Runtime(self.repo, 'C-01')

    def test_local_contention_preserves_lock(self):
        with self.r.lock('session-a'):
            with self.assertRaisesRegex(ValueError, 'occupied'):
                self.r.checkpoint('session-b', 'implement', 'test')
            self.assertEqual(json.loads((self.r.state / 'lock').read_text())['session'], 'session-a')
        self.assertFalse((self.r.state / 'lock').exists())

    def test_resume_is_offline_read_only_and_start_is_idempotent(self):
        target = Path(self.tmp.name) / 'worktree'
        first = self.r.start('s1', target)
        second = self.r.start('s2', target)
        self.assertEqual(first['worktree']['branch'], second['worktree']['branch'])
        before = (self.r.state / 'journal.json').read_bytes()
        self.assertFalse(self.r.status()['network'])
        self.assertEqual(before, (self.r.state / 'journal.json').read_bytes())
        self.assertEqual(len(runtime.git(self.repo, 'worktree', 'list', '--porcelain').split('worktree ')) - 1, 2)

    def test_start_never_overwrites_existing_directory(self):
        target = Path(self.tmp.name) / 'occupied'
        target.mkdir()
        (target / 'valuable').write_text('keep')
        with self.assertRaises(ValueError):
            self.r.start('s1', target)
        self.assertEqual((target / 'valuable').read_text(), 'keep')

    def publication(self):
        runtime.git(self.repo, 'switch', '-c', 'raven/C-01')

    def test_ambiguous_publication_reconciles_without_second_create(self):
        self.publication()
        head = runtime.git(self.repo, 'rev-parse', 'HEAD')
        class API:
            writes = 0
            def request(api, method, endpoint, payload=None):
                if '/git/ref/' in endpoint:
                    return {'object': {'sha': head}}
                if method == 'POST':
                    api.writes += 1
                    raise ValueError('timeout after remote acceptance')
                if api.writes:
                    return [{'number': 7, 'state': 'open', 'html_url': 'https://example.test/7', 'head': {'ref': 'raven/C-01', 'sha': head, 'repo': {'full_name': 'owner/repo'}}, 'base': {'ref': 'main', 'repo': {'full_name': 'owner/repo'}}, 'body': '<!-- raven-change:C-01 -->'}]
                return []
        api = API()
        with self.assertRaises(ValueError):
            self.r.publish('s1', 'Title', 'Body', True, api)
        self.assertEqual(self.r.journal()['publication']['state'], 'pending')
        result = self.r.publish('s2', 'Title', 'Body', True, api)
        self.assertEqual(result['number'], 7)
        self.assertEqual(api.writes, 1)

    def test_pending_absence_does_not_retry_create(self):
        self.publication()
        head = runtime.git(self.repo, 'rev-parse', 'HEAD')
        class API:
            writes = 0
            def request(api, method, endpoint, payload=None):
                if '/git/ref/' in endpoint:
                    return {'object': {'sha': head}}
                if method == 'POST':
                    api.writes += 1
                    raise ValueError('unknown')
                return []
        api = API()
        for _ in range(2):
            with self.assertRaises(ValueError):
                self.r.publish('s1', 'Title', 'Body', True, api)
        self.assertEqual(api.writes, 1)

    def test_checkpoint_travels_in_plan_without_journal(self):
        self.r.checkpoint('s1', 'implement', 'test')
        (self.r.state / 'journal.json').unlink()
        status = self.r.status()
        self.assertTrue(status['contract_current'])
        self.assertEqual(status['checkpoint']['next'], 'test')
        self.assertNotIn('acceptance', status['checkpoint'])

    def test_clone_checkpoint_preserves_versioned_base_and_pr_without_journal(self):
        base = runtime.git(self.repo, 'rev-parse', 'HEAD')
        pr = 'https://example.test/owner/repo/pull/7'
        self.r.save({'schema_version': 1, 'change': 'C-01', 'worktree': {'base': base}, 'publication': {'url': pr}})
        self.r.checkpoint('source-session', 'implement', 'test')
        runtime.git(self.repo, 'add', '.')
        runtime.git(self.repo, 'commit', '-m', 'persist checkpoint')
        clone = Path(self.tmp.name) / 'fresh-clone'
        subprocess.run(['git', 'clone', '--quiet', str(self.repo), str(clone)], check=True, capture_output=True)
        resumed = runtime.Runtime(clone, 'C-01')
        self.assertFalse((resumed.state / 'journal.json').exists())
        result = resumed.checkpoint('new-host-session', 'test', 'review')['checkpoint']
        self.assertEqual(result['base'], base)
        self.assertEqual(result['pr'], pr)

    def test_conflicting_local_journal_cannot_overwrite_canonical_identity(self):
        self.r.save({'worktree': {'base': 'base-a'}, 'publication': {'url': 'https://example.test/pr/1'}})
        self.r.checkpoint('s1', 'implement', 'test')
        original = self.plan.read_bytes()
        for journal in ({'worktree': {'base': 'base-b'}}, {'publication': {'url': 'https://example.test/pr/2'}}):
            self.r.save(journal)
            with self.assertRaisesRegex(ValueError, 'conflicts with canonical checkpoint'):
                self.r.checkpoint('s2', 'test', 'review')
            self.assertEqual(self.plan.read_bytes(), original)

    def test_checkpoint_preserves_extensions_without_rebinding_old_evidence(self):
        old_head = runtime.git(self.repo, 'rev-parse', 'HEAD')
        extensions = {'status': 'review-pending', 'models': {'planner': 'requested-model'},
                      'metadata': {'owner': 'caller'},
                      'findings': [{'message': 'original finding', 'head': old_head}],
                      'references': [{'path': 'report.md', 'head': old_head}]}
        preliminary = {**extensions, 'evidence': 'old test PASS', 'head': old_head,
                       'stage': 'test', 'next': 'review'}
        self.plan.write_text(self.plan.read_text() + '\n' + runtime.CHECK_START + '\n' + json.dumps(preliminary) + '\n' + runtime.CHECK_END + '\n')
        (self.repo / 'changed.py').write_text('changed code')
        runtime.git(self.repo, 'add', '.')
        runtime.git(self.repo, 'commit', '-m', 'new head')
        item = self.r.checkpoint('s1', 'implement', 'test')['checkpoint']
        for key, value in extensions.items():
            self.assertEqual(item[key], value)
        self.assertNotEqual(item['head'], old_head)
        self.assertIsNone(item['evidence'])
        self.assertEqual(item['stage'], 'implement')
        updated = self.r.checkpoint('s2', 'test', 'review', evidence='caller supplied new result')['checkpoint']
        self.assertEqual(updated['evidence'], 'caller supplied new result')
        self.assertEqual(updated['references'], extensions['references'])

    def test_resume_preserves_cycle_evidence_and_acceptance_versions_without_claiming_freshness(self):
        old_head = runtime.git(self.repo, 'rev-parse', 'HEAD')
        fields = {
            'acceptance': {'fingerprint': 'legacy-fingerprint', 'decision_ref': 'user:plan-acceptance', 'verified': False},
            'implementation': {'head': old_head, 'completed': True},
            'checks': [{'ac': 'AC1', 'test': 'tests/save.py::test_reload',
                        'command': 'pytest tests/save.py', 'result': 'PASS', 'head': old_head}],
            'review': {'head': old_head, 'path': 'review.md', 'result': 'PASS'},
            'qa': {'head': old_head, 'scenarios': ['S1'], 'result': 'PASS'},
            'execution_mode': 'auto', 'qa_required': True,
            'acceptance_instructions': {'path': 'acceptance.md', 'head': old_head},
            'manual_verification': {'source': 'user:message-2', 'steps': ['S1']},
            'test_stage': {'completed': True, 'sufficient': True, 'head': old_head,
                           'evidence': ['tests/save.py::test_reload'], 'gaps': []},
            'user_acceptance': {'source': 'user:raven-pr-C-01', 'scope': ['AC1'], 'head': old_head},
            'publication': {'mode': 'ready', 'url': 'https://example.test/pr/7'},
            'repair_attempts_by_problem': {'QA-1': 1, 'FEEDBACK-2': 0},
        }
        self.plan.write_text(self.plan.read_text() + '\n' + runtime.CHECK_START + '\n'
                             + json.dumps(fields) + '\n' + runtime.CHECK_END + '\n')
        self.r.checkpoint('first', 'test', 'pr')
        (self.repo / 'docs.md').write_text('documentation update')
        runtime.git(self.repo, 'add', '.')
        runtime.git(self.repo, 'commit', '-m', 'documentation delta')
        (self.r.state / 'journal.json').unlink()
        status = self.r.status()
        self.assertFalse(status['code_head_current'])
        result = self.r.checkpoint('new-session', 'pr', 'merge')['checkpoint']
        for key, value in fields.items():
            self.assertEqual(result[key], value, key)
        self.assertNotEqual(result['head'], result['user_acceptance']['head'])
        self.assertEqual(result['acceptance']['decision_ref'], 'user:plan-acceptance')
        self.assertIsNone(result['evidence'])

    def test_dirty_tree_and_repair_count_survive_checkpoint_without_acceptance(self):
        self.r.checkpoint('s1', 'plan', 'implement', repair_attempts=2)
        self.r.checkpoint('s2', 'implement', 'test')
        before = self.r.status()
        self.assertTrue(before['code_tree_current'])
        self.assertNotIn('acceptance', before['checkpoint'])
        self.assertEqual(before['checkpoint']['repair_attempts'], 2)
        self.assertEqual(before['checkpoint']['checkpoint_sequence'], 2)
        (self.repo / 'untracked.py').write_text('new code')
        after = self.r.status()
        self.assertFalse(after['code_tree_current'])
        self.assertTrue(after['code_head_current'])
        self.assertIn('untracked.py', after['dirty'])

    def test_start_refuses_uncommitted_checkpoint_loss(self):
        self.r.checkpoint('s1', 'plan', 'implement')
        with self.assertRaisesRegex(ValueError, 'complete current plan'):
            self.r.start('s1', Path(self.tmp.name) / 'worktree')

    def test_start_without_plan_supports_planning(self):
        self.plan.unlink()
        target = Path(self.tmp.name) / 'planning'
        self.assertTrue(self.r.status()['plan_missing'])
        self.r.start('s1', target)
        self.assertTrue(target.is_dir())

    def test_existing_branch_pr_without_marker_never_creates_duplicate(self):
        self.publication()
        class API:
            def request(api, method, endpoint, payload=None):
                self.assertEqual(method, 'GET')
                return [{'head': {'ref': 'raven/C-01'}, 'base': {'ref': 'main'}, 'body': ''}]
        with self.assertRaisesRegex(ValueError, 'Existing branch PR'):
            self.r.publish('s1', 'Title', 'Body', True, API())

    def test_existing_branch_pr_other_base_is_not_hidden(self):
        self.publication()
        class API:
            def request(api, method, endpoint, payload=None):
                self.assertNotIn('base=', endpoint)
                self.assertEqual(method, 'GET')
                return [{'head': {'ref': 'raven/C-01'}, 'base': {'ref': 'other'}, 'body': '<!-- raven-change:C-01 -->'}]
        with self.assertRaisesRegex(ValueError, 'another base'):
            self.r.publish('s1', 'Title', 'Body', True, API())

    def test_existing_pr_stale_head_is_not_claimed_published(self):
        self.publication()
        class API:
            def request(api, method, endpoint, payload=None):
                self.assertEqual(method, 'GET')
                return [{'number': 9, 'html_url': 'https://example.test/9', 'state': 'open',
                         'head': {'ref': 'raven/C-01', 'sha': '0' * 40, 'repo': {'full_name': 'owner/repo'}},
                         'base': {'ref': 'main', 'repo': {'full_name': 'owner/repo'}},
                         'body': '<!-- raven-change:C-01 -->'}]
        self.assertEqual(self.r.publish('s1', 'Title', 'Body', True, API())['state'], 'stale-remote')

    def test_create_readback_wrong_sha_remains_pending(self):
        self.publication()
        head = runtime.git(self.repo, 'rev-parse', 'HEAD')
        class API:
            writes = 0
            def request(api, method, endpoint, payload=None):
                if '/git/ref/' in endpoint:
                    return {'object': {'sha': head}}
                if method == 'POST':
                    api.writes += 1
                    return {'number': 10}
                if endpoint.endswith('/10'):
                    return {'number': 10, 'state': 'open', 'head': {'ref': 'raven/C-01', 'sha': '0' * 40, 'repo': {'full_name': 'owner/repo'}},
                            'base': {'ref': 'main', 'repo': {'full_name': 'owner/repo'}}, 'body': '<!-- raven-change:C-01 -->'}
                return []
        api = API()
        with self.assertRaisesRegex(ValueError, 'readback failed'):
            self.r.publish('s1', 'Title', 'Body', True, api)
        self.assertEqual(api.writes, 1)
        self.assertEqual(self.r.journal()['publication']['state'], 'pending')

    def test_dry_run_has_no_lock_journal_or_network(self):
        self.publication()
        result = self.r.publish('s1', 'Title', 'Body')
        self.assertTrue(result['payload']['draft'])
        self.assertFalse(result['network'])
        self.assertFalse(self.r.state.exists())


class AdapterTests(unittest.TestCase):
    def test_read_pr_selects_fields_without_truncating_body(self):
        body = 'Complete requirements\n' * 100
        result = runtime.selected_pr({'number': 1, 'html_url': 'https://example.test/1', 'title': 'Title', 'body': body,
            'state': 'open', 'draft': True, 'merged': False, 'mergeable': None,
            'head': {'ref': 'branch', 'sha': 'abc', 'repo': {'full_name': 'owner/repo', 'owner': {'large': 'data'}}},
            'base': {'ref': 'main', 'sha': 'def', 'repo': {'full_name': 'owner/repo'}},
            'user': {'unneeded': 'data'}, 'comments_url': 'unused'})
        self.assertEqual(result['body'], body)
        self.assertEqual(result['head'], {'ref': 'branch', 'sha': 'abc', 'repo': 'owner/repo'})
        self.assertEqual(set(result), {'number', 'url', 'title', 'body', 'state', 'draft', 'merged', 'mergeable', 'base', 'head'})

    def test_success_at_limit_stops_next_operation(self):
        calls = []
        class Response(io.BytesIO):
            headers = {'X-RateLimit-Remaining': '0', 'X-RateLimit-Reset': '9999999999'}
        def respond(*args, **kwargs):
            calls.append(1)
            return Response(b'[]')
        api = runtime.GitHub('secret', respond)
        self.assertEqual(api.request('GET', '/repos/owner/repo/pulls'), [])
        with self.assertRaisesRegex(ValueError, 'deferred retry'):
            api.request('POST', '/repos/owner/repo/pulls', {})
        self.assertEqual(len(calls), 1)

    def test_reads_retry_bounded_and_writes_never_retry(self):
        calls, waits = [], []
        def fail(req, timeout):
            calls.append(req.method)
            raise urllib.error.HTTPError(req.full_url, 503, 'failure', {}, io.BytesIO())
        api = runtime.GitHub('secret', fail, waits.append)
        with self.assertRaisesRegex(ValueError, '503'):
            api.request('GET', '/repos/owner/repo/pulls/1')
        self.assertEqual(len(calls), 3)
        self.assertEqual(waits, [1, 2])
        calls.clear()
        with self.assertRaises(ValueError):
            api.request('POST', '/repos/owner/repo/pulls', {})
        self.assertEqual(len(calls), 1)

    def test_issue_patch_transport_timeout_is_never_retried(self):
        calls, waits = [], []
        def fail(req, timeout):
            calls.append(req.method)
            raise TimeoutError('unknown outcome')
        api = runtime.GitHub('secret', fail, waits.append)
        with self.assertRaisesRegex(ValueError, 'must be reconciled'):
            api.request('PATCH', '/repos/owner/repo/issues/12', {'labels': ['in-progress']})
        self.assertEqual(calls, ['PATCH'])
        self.assertEqual(waits, [])

    def test_retry_after_is_honored_and_long_wait_is_reported(self):
        waits = []
        def fail(req, timeout):
            raise urllib.error.HTTPError(req.full_url, 429, 'rate', {'Retry-After': '60', 'X-RateLimit-Remaining': '0'}, io.BytesIO())
        api = runtime.GitHub('secret', fail, waits.append)
        with self.assertRaisesRegex(ValueError, 'Retry-After'):
            api.request('GET', '/repos/owner/repo/pulls/1')
        self.assertEqual(waits, [])

    def test_response_limit(self):
        class Response(io.BytesIO):
            headers = {}
        api = runtime.GitHub('secret', lambda *a, **k: Response(b'x' * (runtime.MAX_BYTES + 1)))
        with self.assertRaisesRegex(ValueError, 'size limit'):
            api.request('GET', '/repos/owner/repo/pulls/1')


if __name__ == '__main__':
    unittest.main()
