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

    def test_retired_skill_mention_fails(self):
        self.skill.write_text(self.skill.read_text() + '\nFirst run raven-plan-review.\n')
        self.assertIn('text.retired', self.codes())

    def test_retired_artifact_mention_fails(self):
        self.skill.write_text(self.skill.read_text() + '\nSave the result in `context/changes/<id>/frame.md`.\n')
        self.assertIn('text.retired', self.codes())

    def test_current_skill_with_retired_prefix_passes(self):
        self.skill.write_text(self.skill.read_text() + '\nPotem raven-implement-review.\n')
        self.assertNotIn('text.retired', self.codes())

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


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.contract = json.loads((ROOT / 'workflow-contract.json').read_text())

    def test_current_catalog_is_valid(self):
        raven.validate_catalog(self.contract)

    def test_process_gates_cannot_return(self):
        for key in ('stages', 'invariants', 'roles', 'auto_implementation', 'initial_artifacts'):
            with self.subTest(key=key):
                contract = copy.deepcopy(self.contract)
                contract[key] = []
                with self.assertRaisesRegex(ValueError, 'catalog only'):
                    raven.validate_catalog(contract)

    def test_legacy_schema_is_rejected(self):
        contract = copy.deepcopy(self.contract)
        contract['schema_version'] = 2
        with self.assertRaisesRegex(ValueError, 'schema_version'):
            raven.validate_catalog(contract)

    def test_merged_skills_cannot_return(self):
        for name in ('raven-auto-plan', 'raven-plan-review', 'raven-auto-test', 'raven-test-review',
                     'raven-test-plan', 'raven-frame', 'raven-agents-md', 'raven-rule-review',
                     'raven-jira-roadmap', 'raven-domain-distillation'):
            with self.subTest(name=name):
                self.assertTrue(raven.retired(name))
                self.assertNotIn(name, self.contract['skills'])


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
