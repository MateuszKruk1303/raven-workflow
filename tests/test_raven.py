import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('raven', ROOT / 'tools/raven.py')
raven = importlib.util.module_from_spec(spec)
spec.loader.exec_module(raven)


class DoctorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'
        self.root.mkdir()
        shutil.copytree(ROOT / 'skills', self.root / 'skills')
        shutil.copytree(ROOT / '.github', self.root / '.github')
        for name in ['README.md', 'workflow-contract.json']:
            shutil.copy2(ROOT / name, self.root / name)
        self.skill = self.root / 'skills/raven-browser/SKILL.md'

    def codes(self):
        return {e['code'] for e in raven.doctor(self.root)}

    def test_repository_passes(self):
        self.assertEqual(raven.doctor(ROOT), [])

    def test_missing_referenced_resource_fails(self):
        self.skill.write_text(self.skill.read_text() + '\n[required](references/missing.md)\n')
        self.assertIn('link.missing', self.codes())

    def test_code_examples_do_not_create_fake_dependencies(self):
        self.skill.write_text(self.skill.read_text() + '\n```md\n[example](absent.md)\n```\n')
        self.assertNotIn('link.missing', self.codes())

    def test_name_mismatch_fails(self):
        self.skill.write_text(self.skill.read_text().replace('name: raven-browser', 'name: wrong'))
        self.assertIn('skill.metadata', self.codes())

    def test_removed_skill_breaks_catalog_and_links(self):
        shutil.rmtree(self.root / 'skills/raven-browser')
        self.assertTrue({'skill.missing', 'link.missing'} <= self.codes())

    def test_retired_skill_cannot_return(self):
        (self.root / 'skills/raven-pilot-init').mkdir()
        self.assertIn('skill.retired', self.codes())

    def test_removed_raven_implement_cannot_return(self):
        (self.root / 'skills/raven-implement').mkdir()
        self.assertIn('skill.retired', self.codes())

    def test_catalog_omission_fails(self):
        p = self.root / 'README.md'
        p.write_text(p.read_text().replace('(skills/raven-browser/SKILL.md)', '(skills/raven-workflow/SKILL.md)'))
        self.assertIn('catalog.undocumented', self.codes())

    def test_unknown_installation_is_not_reported_as_current(self):
        issues = raven.doctor(self.root, self.root / 'absent')
        self.assertIn('sync.source', {e['code'] for e in issues})

    def test_malformed_contract_is_reported(self):
        (self.root / 'workflow-contract.json').write_text('{')
        self.assertIn('contract.invalid', self.codes())


class ProcessTests(unittest.TestCase):
    def setUp(self):
        self.contract = json.loads((ROOT / 'workflow-contract.json').read_text())

    def check(self):
        raven.validate_process(self.contract, set(self.contract['skills']))

    def test_missing_producer_breaks_handoff(self):
        self.contract['stages'][0]['produces'] = []
        with self.assertRaisesRegex(ValueError, 'Wrong artifact producer'):
            self.check()

    def test_self_review_is_rejected(self):
        self.contract['stages'][1]['fresh_context'] = False
        with self.assertRaisesRegex(ValueError, 'Independent context'):
            self.check()

    def test_auto_implementation_contract_is_required(self):
        self.contract.pop('auto_implementation')
        with self.assertRaisesRegex(ValueError, 'Auto implementation'):
            self.check()

    def test_auto_execution_cannot_restore_workflow_requirements(self):
        original = copy.deepcopy(self.contract['auto_implementation'])
        mutations = [
            ('execution', 'delegated_implementer'), ('role', 'implementer'),
            ('requires', ['plan_review', 'issue_started']),
            ('inputs', ['plan_contract', 'plan_review']),
            ('scope', 'replan_and_review_current_instruction'),
            ('verification_levels', ['standard']), ('default_level', 'thorough'),
            ('level_change', 'any'), ('functional_check', 'never'),
            ('independent_review', 'every_level'), ('existing_tests', 'duplicate_all_layers'),
            ('unrelated_failures', 'repair_all'), ('handoff', 'acceptance.md'),
            ('retry_limit_per_defect', 2), ('checkpoint', 'required'),
        ]
        for key, value in mutations:
            with self.subTest(key=key, value=value):
                self.contract['auto_implementation'] = copy.deepcopy(original)
                self.contract['auto_implementation'][key] = value
                with self.assertRaisesRegex(ValueError, 'Auto implementation'):
                    self.check()

    def test_auto_inputs_are_sufficient_without_workflow_artifacts(self):
        self.check()
        auto = self.contract['auto_implementation']
        self.assertEqual(auto['execution'], 'current_agent')
        self.assertEqual(set(auto['inputs']), {'indicated_plan', 'current_user_instruction'})
        self.assertEqual(auto['verification_levels'], ['quick', 'standard', 'thorough'])
        self.assertEqual(auto['independent_review'], 'thorough_only_single_round')
        self.assertEqual(self.stage('implement')['skills'], ['raven-auto-implement'])
        self.assertEqual(self.stage('implement')['requires'], ['plan_contract'])
        self.assertEqual(self.stage('code_review')['skills'], ['raven-implement-review'])
        self.assertIn('code_review', self.stage('test')['requires'])
        self.assertIn('regression_evidence', self.stage('pr')['requires'])
        self.assertIn('code_review', self.stage('merge')['requires'])

    def test_implementation_owned_only_by_auto_implement(self):
        self.stage('implement')['skills'].append('raven-test')
        with self.assertRaisesRegex(ValueError, 'owned by raven-auto-implement'):
            self.check()

    def test_auto_implement_cannot_own_other_stages(self):
        self.stage('test')['skills'].append('raven-auto-implement')
        with self.assertRaisesRegex(ValueError, 'only the implement stage'):
            self.check()

    def test_auto_implementation_cannot_own_code_review(self):
        self.stage('code_review')['skills'].append('raven-auto-implement')
        with self.assertRaisesRegex(ValueError, 'separately invoked'):
            self.check()

    def test_legacy_automatic_qa_contract_cannot_return(self):
        self.contract['auto_implementation_qa'] = {'required_before_completion': True}
        with self.assertRaisesRegex(ValueError, 'Auto implementation'):
            self.check()

    def test_doctor_reports_missing_auto_execution_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'repo'
            shutil.copytree(ROOT / 'skills', root / 'skills')
            shutil.copy2(ROOT / 'README.md', root / 'README.md')
            self.contract.pop('auto_implementation')
            (root / 'workflow-contract.json').write_text(json.dumps(self.contract))
            errors = raven.doctor(root)
            self.assertTrue(any(error['code'] == 'workflow.contract'
                                and 'Auto implementation' in error['detail']
                                for error in errors))

    def test_review_before_plan_is_rejected(self):
        stages = self.contract['stages']
        stages[0], stages[1] = stages[1], stages[0]
        with self.assertRaisesRegex(ValueError, 'Unmet handoff'):
            self.check()

    def test_agent_cannot_grant_product_acceptance(self):
        self.contract['stages'][0]['produces'].append('user_acceptance')
        with self.assertRaisesRegex(ValueError, 'external acceptance'):
            self.check()

    def test_implementation_requires_only_plan(self):
        for extra in ('plan_review', 'issue_started', 'pull_request'):
            with self.subTest(extra=extra):
                self.stage('implement')['requires'] = ['plan_contract', extra]
                with self.assertRaisesRegex(ValueError, 'requires only the plan'):
                    self.check()

    def test_new_plan_handoff_has_review_without_plan_acceptance(self):
        self.check()
        self.assertNotIn('plan_accepted', self.contract['initial_artifacts'])
        self.assertEqual(self.stage('implement')['requires'], ['plan_contract'])
        self.assertEqual(self.contract['invariants']['plan_review'], 'contract_fingerprint')
        self.assertFalse(self.contract['invariants']['progress_invalidates_plan_review'])
        for stage in self.contract['stages']:
            self.assertNotIn('plan_accepted', stage['requires'] + stage['produces'])

    def test_retired_plan_acceptance_cannot_return_as_external_gate(self):
        self.contract['initial_artifacts'].append('plan_accepted')
        self.stage('implement')['requires'].append('plan_accepted')
        with self.assertRaisesRegex(ValueError, 'External artifacts'):
            self.check()

    def test_contract_does_not_pin_models(self):
        self.contract['roles'] = {'reviewer': {'model': 'any-model', 'effort': 'high'}}
        with self.assertRaisesRegex(ValueError, 'must not pin agent models'):
            self.check()

    def test_reviewer_role_cannot_become_author(self):
        next(s for s in self.contract['stages'] if s['id'] == 'code_review')['role'] = 'implementer'
        with self.assertRaisesRegex(ValueError, 'Wrong role'):
            self.check()

    def stage(self, name):
        return next(s for s in self.contract['stages'] if s['id'] == name)

    def test_tests_are_produced_with_implementation(self):
        self.check()
        self.assertIn('test_evidence', self.stage('implement')['produces'])
        self.stage('implement')['produces'].remove('test_evidence')
        with self.assertRaisesRegex(ValueError, 'Wrong artifact producer'):
            self.check()

    def test_review_requires_tests_and_requirements(self):
        for artifact in ('test_evidence', 'plan_contract'):
            with self.subTest(artifact=artifact):
                original = self.stage('code_review')['requires'][:]
                self.stage('code_review')['requires'].remove(artifact)
                with self.assertRaisesRegex(ValueError, 'must require'):
                    self.check()
                self.stage('code_review')['requires'] = original

    def test_standard_cycle_keeps_tests_with_implementation_and_closes_regression(self):
        self.check()
        self.assertEqual({s['id'] for s in self.contract['stages']},
                         {'plan', 'plan_review', 'implement', 'code_review', 'test', 'pr', 'merge'})
        self.assertEqual(self.stage('merge')['produces'], ['merged_pr', 'issue_done'])
        self.assertNotIn('pull_request', self.stage('implement')['requires'])
        self.assertNotIn('side_operation', self.stage('pr'))
        self.assertEqual(self.stage('test')['produces'], ['regression_evidence'])

    def test_standard_publication_requires_regression_and_external_acceptance(self):
        self.check()
        self.assertEqual(set(self.stage('pr')['requires']),
                         {'plan_contract', 'implementation', 'regression_evidence',
                          'publication_requested', 'user_acceptance'})
        self.assertLess(self.contract['stages'].index(self.stage('test')),
                        self.contract['stages'].index(self.stage('pr')))
        for artifact in ('implementation', 'regression_evidence', 'user_acceptance'):
            original = self.stage('pr')['requires'][:]
            self.stage('pr')['requires'].remove(artifact)
            with self.assertRaisesRegex(ValueError, 'must require'):
                self.check()
            self.stage('pr')['requires'] = original

    def test_regression_audit_cannot_be_replaced_with_implementation_pass(self):
        self.stage('test')['requires'].remove('manual_verification')
        with self.assertRaisesRegex(ValueError, 'must require'):
            self.check()
        self.stage('test')['requires'].append('manual_verification')
        self.stage('test')['produces'] = ['test_evidence']
        with self.assertRaisesRegex(ValueError, 'Wrong artifact producer'):
            self.check()

    def test_publication_exception_never_manufactures_acceptance_or_bypasses_merge(self):
        exceptions = copy.deepcopy(self.contract['publication_exceptions'])
        mutations = [('early_draft', 'user_acceptance', True),
                     ('early_draft', 'authorization', 'automatic'),
                     ('missing_test_evidence', 'requires_explicit_confirmation', False),
                     ('missing_test_evidence', 'records_gaps', False),
                     ('missing_test_evidence', 'waives_merge_gates', True)]
        for section, key, value in mutations:
            with self.subTest(section=section, key=key):
                self.contract['publication_exceptions'] = copy.deepcopy(exceptions)
                self.contract['publication_exceptions'][section][key] = value
                with self.assertRaisesRegex(ValueError, 'Publication exceptions'):
                    self.check()

    def test_agent_cannot_produce_manual_verification_or_product_acceptance(self):
        for stage, artifact in [('test', 'manual_verification'), ('pr', 'user_acceptance')]:
            self.stage(stage)['produces'].append(artifact)
            with self.assertRaisesRegex(ValueError, 'external acceptance'):
                self.check()
            self.stage(stage)['produces'].remove(artifact)

    def test_manual_instructions_are_chat_only_and_do_not_accept_product(self):
        self.assertEqual(self.contract['auto_implementation']['handoff'], 'final_chat_only')
        self.assertNotIn('acceptance_instructions', self.contract['source_of_truth'])
        self.contract['source_of_truth']['acceptance_instructions'] = 'acceptance.md'
        with self.assertRaisesRegex(ValueError, 'sources of truth'):
            self.check()

    def test_regression_stage_cannot_become_only_optional(self):
        self.contract['stages'].remove(self.stage('test'))
        with self.assertRaisesRegex(ValueError, 'exactly'):
            self.check()

    def test_merge_stage_cannot_disappear(self):
        self.contract['stages'].remove(self.stage('merge'))
        with self.assertRaisesRegex(ValueError, 'exactly'):
            self.check()

    def test_review_before_implementation_is_rejected(self):
        stages = self.contract['stages']
        a, b = stages.index(self.stage('implement')), stages.index(self.stage('code_review'))
        stages[a], stages[b] = stages[b], stages[a]
        with self.assertRaisesRegex(ValueError, 'Unmet handoff'):
            self.check()

    def test_merge_cannot_treat_publication_as_readiness(self):
        self.stage('merge')['requires'] = ['pull_request', 'merge_requested']
        with self.assertRaisesRegex(ValueError, 'must require'):
            self.check()

    def test_publication_cannot_grant_merge_authorization(self):
        self.stage('pr')['produces'].append('merge_requested')
        with self.assertRaisesRegex(ValueError, 'external acceptance'):
            self.check()

    def test_merge_requires_its_own_authorization_and_current_evidence(self):
        for artifact in ('merge_requested', 'ci_passed', 'user_acceptance', 'test_evidence', 'code_review', 'regression_evidence'):
            with self.subTest(artifact=artifact):
                original = self.stage('merge')['requires'][:]
                self.stage('merge')['requires'].remove(artifact)
                with self.assertRaisesRegex(ValueError, 'must require'):
                    self.check()
                self.stage('merge')['requires'] = original

    def test_merge_evidence_cannot_be_initial_or_pending(self):
        self.contract['initial_artifacts'].append('merged_pr')
        with self.assertRaisesRegex(ValueError, 'External artifacts'):
            self.check()
        self.contract['initial_artifacts'].remove('merged_pr')
        self.stage('merge')['produces'] = ['merge_queued']
        with self.assertRaisesRegex(ValueError, 'Wrong artifact producer'):
            self.check()

    def test_issue_start_is_required_before_planning(self):
        self.stage('plan')['requires'].remove('issue_started')
        with self.assertRaisesRegex(ValueError, 'must require'):
            self.check()
        self.stage('plan')['requires'].append('issue_started')

    def test_merge_cannot_also_claim_board_done(self):
        self.stage('merge')['produces'].append('board_done')
        with self.assertRaisesRegex(ValueError, 'Wrong artifact producer'):
            self.check()

    def test_merge_belongs_to_merge_skill(self):
        self.stage('merge')['skills'] = ['raven-pr']
        with self.assertRaisesRegex(ValueError, 'owned by raven-merge'):
            self.check()

    def test_manual_auto_share_gates(self):
        self.stage('merge')['modes'] = ['auto']
        with self.assertRaisesRegex(ValueError, 'Wrong modes'):
            self.check()

    def test_git_first_invariants_cannot_remove_mandatory_tracker(self):
        self.contract['invariants']['mandatory_task_issues'] = False
        with self.assertRaisesRegex(ValueError, 'invariants'):
            self.check()

    def test_contract_does_not_allow_github_as_plan_database(self):
        self.contract['source_of_truth']['change'] = 'github_issue'
        with self.assertRaisesRegex(ValueError, 'sources of truth'):
            self.check()

    def test_review_covers_product_and_tests(self):
        self.stage('code_review')['covers'] = ['code']
        with self.assertRaisesRegex(ValueError, 'must cover'):
            self.check()

    def test_legacy_schema_is_rejected(self):
        self.contract['schema_version'] = 1
        with self.assertRaisesRegex(ValueError, 'Unsupported schema_version'):
            self.check()


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.src, self.dst = self.root / 'src', self.root / 'dst'
        self.names = ['raven-example']
        for base in (self.src, self.dst):
            (base / 'raven-example').mkdir(parents=True)
            (base / 'raven-example/SKILL.md').write_text('source' if base == self.src else 'old')
        (self.dst / 'other-skill').mkdir()
        (self.dst / 'other-skill/user.txt').write_text('keep')
        (self.dst / 'raven-example/stale.md').write_text('old helper')
        (self.dst / 'raven-pilot-init').mkdir()
        (self.dst / 'raven-pilot-init/SKILL.md').write_text('retired')

    def test_preview_is_read_only(self):
        changes, backup = raven.synchronize(self.src, self.dst, self.names)
        self.assertIsNone(backup)
        self.assertEqual((self.dst / 'raven-example/SKILL.md').read_text(), 'old')
        self.assertEqual({c['action'] for c in changes}, {'update', 'delete', 'retire'})

    def test_apply_backs_up_preserves_unrelated_and_is_idempotent(self):
        changes, backup = raven.synchronize(self.src, self.dst, self.names, True)
        self.addCleanup(shutil.rmtree, backup)
        self.assertEqual((backup / 'raven-example/SKILL.md').read_text(), 'old')
        self.assertTrue((backup / 'raven-pilot-init/SKILL.md').exists())
        self.assertFalse((self.dst / 'raven-example/stale.md').exists())
        self.assertEqual((self.dst / 'other-skill/user.txt').read_text(), 'keep')
        self.assertEqual(raven.sync_plan(self.src, self.dst, self.names), [])

    def test_missing_source_never_deletes_destination(self):
        (self.src / 'raven-example/SKILL.md').unlink()
        with self.assertRaises(ValueError):
            raven.synchronize(self.src, self.dst, self.names, True)
        self.assertEqual((self.dst / 'raven-example/SKILL.md').read_text(), 'old')

    def test_symlink_is_not_followed_for_writes(self):
        outside = self.root / 'outside.md'
        outside.write_text('keep')
        (self.dst / 'raven-example/linked.md').symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'Symlink'):
            raven.synchronize(self.src, self.dst, self.names, True)
        self.assertEqual(outside.read_text(), 'keep')

    def test_directory_to_file_conflict_fails_before_any_write(self):
        (self.dst / 'raven-example/resource').mkdir()
        (self.dst / 'raven-example/resource/old.txt').write_text('keep')
        (self.src / 'raven-example/resource').write_text('new file')
        with self.assertRaisesRegex(ValueError, 'File/directory conflict'):
            raven.synchronize(self.src, self.dst, self.names, True)
        self.assertEqual((self.dst / 'raven-example/SKILL.md').read_text(), 'old')
        self.assertEqual((self.dst / 'raven-example/resource/old.txt').read_text(), 'keep')

    def test_file_to_directory_conflict_fails_before_any_write(self):
        (self.dst / 'raven-example/resource').write_text('keep')
        (self.src / 'raven-example/resource').mkdir()
        (self.src / 'raven-example/resource/new.txt').write_text('new file')
        with self.assertRaisesRegex(ValueError, 'File/directory conflict'):
            raven.synchronize(self.src, self.dst, self.names, True)
        self.assertEqual((self.dst / 'raven-example/resource').read_text(), 'keep')

    def test_nested_target_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'non-nested'):
            raven.synchronize(self.src, self.src / 'child', self.names, True)


if __name__ == '__main__':
    unittest.main()
