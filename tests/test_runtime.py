import importlib.util
import io
import json
from pathlib import Path
import subprocess
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

    def test_contract_change_invalidates_checkpoint_progress_does_not(self):
        self.r.checkpoint('s1', 'plan', 'implement', acceptance_ref='user:message-1')
        self.plan.write_text(self.plan.read_text().replace('[ ]', '[x]'))
        self.assertTrue(self.r.status()['contract_current'])
        self.plan.write_text(self.plan.read_text().replace('implementation step S1', 'implementation step S2'))
        self.assertFalse(self.r.status()['contract_current'])
        self.assertEqual(self.r.journal()['checkpoint']['acceptance']['decision_ref'], 'user:message-1')

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
        self.r.checkpoint('s1', 'implement', 'test', acceptance_ref='decision-1')
        (self.r.state / 'journal.json').unlink()
        status = self.r.status()
        self.assertTrue(status['contract_current'])
        self.assertEqual(status['checkpoint']['next'], 'test')
        self.assertFalse(status['checkpoint']['acceptance']['verified'])

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

    def test_dirty_tree_and_decision_survive_checkpoint(self):
        self.r.checkpoint('s1', 'plan', 'implement', acceptance_ref='decision-1', repair_attempts=2)
        self.r.checkpoint('s2', 'implement', 'test')
        before = self.r.status()
        self.assertTrue(before['code_tree_current'])
        self.assertEqual(before['checkpoint']['acceptance']['decision_ref'], 'decision-1')
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
