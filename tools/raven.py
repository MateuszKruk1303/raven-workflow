#!/usr/bin/env python3
"""Offline integrity checks and explicit, preview-first skill synchronization."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
IGNORED = {'.DS_Store', '__pycache__', '.git'}
RETIRED = {
    'raven-seed', 'raven-implement', 'raven-auto-plan', 'raven-plan-review', 'raven-auto-test',
    'raven-test-review', 'raven-test-plan', 'raven-frame', 'raven-agents-md', 'raven-rule-review',
    'raven-jira-roadmap',
}


def retired(name):
    return name.startswith('raven-pilot-') or name in RETIRED


def files(directory):
    return {p.relative_to(directory).as_posix(): p for p in directory.rglob('*')
            if p.is_file() and not any(part in IGNORED for part in p.relative_to(directory).parts)
            and p.suffix not in {'.pyc', '.pyo'}}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def markdown_links(text):
    # Ignore fenced and inline code: examples are not dependencies.
    text = re.sub(r'^\s*(`{3,}|~{3,}).*?^\s*\1\s*$', '', text, flags=re.M | re.S)
    text = re.sub(r'`[^`\n]+`', '', text)
    for match in re.finditer(r'\[[^\]\n]*\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\)', text):
        yield match.group(1).strip('<>')
    for match in re.finditer(r'^\s*\[[^\]]+\]:\s*(\S+)', text, re.M):
        yield match.group(1).strip('<>')


def doctor(root, installed=None):
    errors = []
    def fail(code, path, detail):
        errors.append({'code': code, 'path': str(path), 'detail': detail})
    try:
        contract = json.loads((root / 'workflow-contract.json').read_text())
        names = contract['skills']
        if not isinstance(names, list) or not names or any(not isinstance(n, str) or not re.fullmatch(r'raven-[a-z0-9-]+', n) for n in names):
            raise ValueError('skills must be a nonempty list of Raven names')
        if len(set(names)) != len(names):
            fail('catalog.duplicate', 'workflow-contract.json', 'Duplicate skills')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        fail('contract.invalid', 'workflow-contract.json', str(exc))
        return errors
    actual = {p.name for p in (root / 'skills').glob('raven-*') if p.is_dir()}
    expected = set(names)
    for name in sorted(expected - actual):
        fail('skill.missing', name, 'Listed skill directory missing')
    for name in sorted(actual - expected):
        fail('skill.unregistered', name, 'Register new skill or remove retired directory')
    for name in sorted(actual):
        if retired(name):
            fail('skill.retired', name, 'Retired skill must not be distributed')
        p = root / 'skills' / name / 'SKILL.md'
        try:
            text = p.read_text()
            match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
            if not match:
                raise ValueError('Missing YAML frontmatter')
            metadata = yaml.safe_load(match.group(1))
            if not isinstance(metadata, dict) or metadata.get('name') != name:
                raise ValueError('Frontmatter name must equal directory name')
            if not isinstance(metadata.get('description'), str) or not metadata['description'].strip():
                raise ValueError('Nonempty description required')
        except (OSError, ValueError, yaml.YAMLError) as exc:
            fail('skill.metadata', p.relative_to(root), str(exc))
        ui = p.parent / 'agents/openai.yaml'
        if ui.exists():
            try:
                data = yaml.safe_load(ui.read_text())
                if not isinstance(data, dict) or not isinstance(data.get('interface'), dict):
                    raise ValueError('Expected interface mapping')
            except (ValueError, yaml.YAMLError) as exc:
                fail('skill.ui', ui.relative_to(root), str(exc))
    docs = [root / 'README.md', *sorted((root / 'skills').rglob('*.md'))]
    for p in docs:
        if not p.exists():
            fail('doc.missing', p.relative_to(root), 'Missing document')
            continue
        for link in markdown_links(p.read_text()):
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (p.parent / unquote(parsed.path)).resolve()
            if not target.is_relative_to(root.resolve()):
                fail('link.outside', p.relative_to(root), link)
            elif not target.exists():
                fail('link.missing', p.relative_to(root), link)
    readme = (root / 'README.md').read_text() if (root / 'README.md').exists() else ''
    for name in names:
        if f'skills/{name}/SKILL.md' not in list(markdown_links(readme)):
            fail('catalog.undocumented', name, 'README must link every skill')
    try:
        validate_catalog(contract)
    except ValueError as exc:
        fail('workflow.contract', 'workflow-contract.json', str(exc))
    if installed is not None:
        if not installed.is_dir():
            fail('sync.source', installed, 'Installed skill directory not found')
        else:
            for change in sync_plan(root / 'skills', installed, names):
                fail('sync.drift', change['path'], change['action'])
    return errors


def validate_catalog(contract):
    """The contract is only a catalog: workflow lives in skills, not in process gates."""
    if contract.get('schema_version') != 3:
        raise ValueError('Unsupported schema_version')
    if set(contract) != {'schema_version', 'skills'}:
        raise ValueError('Contract is a catalog only; no stages, gates, roles or models')


def sync_plan(source, destination, names):
    changes = []
    for name in names:
        if not (source / name / 'SKILL.md').is_file():
            raise ValueError(f'Missing source skill: {name}')
        src, dst = files(source / name), files(destination / name)
        for rel in sorted(src.keys() | dst.keys()):
            action = ('delete' if rel not in src else 'add' if rel not in dst
                      else 'update' if digest(src[rel]) != digest(dst[rel]) else None)
            if action:
                changes.append({'action': action, 'path': f'{name}/{rel}'})
    for p in sorted(destination.glob('raven-*')):
        if p.is_dir() and retired(p.name):
            changes.append({'action': 'retire', 'path': p.name})
    return changes


def synchronize(source, destination, names, apply=False):
    source, destination = source.resolve(), destination.resolve()
    if source == destination or source in destination.parents or destination in source.parents:
        raise ValueError('Source and destination must be separate, non-nested directories')
    if any(p.is_symlink() for base in (source, destination) for p in base.rglob('*')
           if any(part in names or retired(part) for part in p.relative_to(base).parts)):
        raise ValueError('Symlinked skill paths are unsupported; use physical directories')
    changes = sync_plan(source, destination, names)
    # Reject type changes before any writes; replacing directories implicitly is unsafe.
    for change in changes:
        if change['action'] not in ('add', 'update'):
            continue
        target = destination / change['path']
        if target.is_dir() or any(parent.is_file() for parent in target.parents if parent != destination):
            raise ValueError(f"File/directory conflict: {change['path']}; resolve explicitly before sync")
    backup = None
    if apply and changes:
        backup = Path(tempfile.mkdtemp(prefix='raven-sync-backup-'))
        # Back up every affected existing skill before any mutation.
        for name in sorted({c['path'].split('/')[0] for c in changes}):
            if (destination / name).exists():
                shutil.copytree(destination / name, backup / name)
        print(f'Backup before applying: {backup}', file=sys.stderr)
        for c in changes:
            path = destination / c['path']
            if c['action'] == 'retire':
                shutil.rmtree(path)
            elif c['action'] == 'delete':
                path.unlink()
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source / c['path'], path)
    if apply and sync_plan(source, destination, names):
        raise ValueError(f'Synchronization readback failed; backup: {backup}')
    return changes, backup


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    check = sub.add_parser('doctor', help='Check repository; read-only, no network')
    check.add_argument('--root', type=Path, default=ROOT)
    check.add_argument('--installed', type=Path, help='Also compare installed skills with repository')
    check.add_argument('--json', action='store_true')
    sync = sub.add_parser('sync', help='Preview repo -> installation; --apply writes with backup')
    sync.add_argument('--to', type=Path, required=True)
    sync.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    try:
        issues = doctor(args.root, args.installed) if args.command == 'doctor' else doctor(ROOT)
        if args.command == 'doctor':
            if args.json:
                print(json.dumps({'ok': not issues, 'issues': issues}, ensure_ascii=False, indent=2))
            elif issues:
                for issue in issues:
                    print(f"FAIL [{issue['code']}] {issue['path']}: {issue['detail']}")
            else:
                print('PASS: metadata, links, catalog' + (' and installation match' if args.installed else ''))
            return bool(issues)
        if issues:
            raise ValueError('Repository fails doctor; fix before synchronization')
        contract = json.loads((ROOT / 'workflow-contract.json').read_text())
        changes, backup = synchronize(ROOT / 'skills', args.to, contract['skills'], args.apply)
        for change in changes:
            print(f"{change['action']:7} {change['path']}")
        print(f"{len(changes)} changes; {'applied' if args.apply else 'preview only; add --apply to write'}")
        if backup:
            print(f'Backup: {backup}')
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
