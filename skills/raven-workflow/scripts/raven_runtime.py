#!/usr/bin/env python3
"""Small Git-first Raven runtime. Local commands never contact GitHub.

Locks/journals live in the Git common directory and coordinate only this host.
No configuration value grants permission; --apply must follow caller authorization.
"""
import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

START = '<!-- raven:contract:start -->'
END = '<!-- raven:contract:end -->'
MAX_BYTES = 1024 * 1024
CHECK_START = '<!-- raven:checkpoint:start -->'
CHECK_END = '<!-- raven:checkpoint:end -->'


def identifier(value):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', value):
        raise ValueError('Invalid change/session identifier')
    return value


def git(repo, *args):
    p = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True, timeout=30)
    if p.returncode:
        raise ValueError(p.stderr.strip() or 'Git operation failed')
    return p.stdout.strip()


def fingerprint(text):
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError('Plan requires exactly one contract marker pair')
    a, b = text.index(START) + len(START), text.index(END)
    if b <= a or not text[a:b].strip():
        raise ValueError('Empty or reversed contract markers')
    return hashlib.sha256(text[a:b].encode()).hexdigest()


def atomic_json(path, value):
    atomic_text(path, json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n')


def atomic_text(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(value)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def selected_pr(value):
    """Keep the complete body but omit unrelated REST metadata and nested users."""
    result = {key: value.get(key) for key in ('number', 'title', 'body', 'state', 'draft', 'merged', 'mergeable')}
    result['url'] = value.get('html_url')
    for side in ('base', 'head'):
        ref = value.get(side) or {}
        result[side] = {'repo': (ref.get('repo') or {}).get('full_name'), 'ref': ref.get('ref'), 'sha': ref.get('sha')}
    return result


class Runtime:
    def __init__(self, repo, change):
        self.repo = Path(git(repo, 'rev-parse', '--show-toplevel')).resolve()
        self.change = identifier(change)
        common = Path(git(self.repo, 'rev-parse', '--git-common-dir'))
        self.state = (common if common.is_absolute() else self.repo / common).resolve() / 'raven' / self.change
        self.plan = self.repo / 'context' / 'changes' / self.change / 'plan.md'
        if not self.plan.resolve().is_relative_to(self.repo) or self.plan.is_symlink():
            raise ValueError('Plan must remain inside repository')

    def journal(self):
        path = self.state / 'journal.json'
        return json.loads(path.read_text()) if path.exists() else {'schema_version': 1, 'change': self.change}

    def save(self, journal):
        atomic_json(self.state / 'journal.json', journal)

    def digest(self):
        return fingerprint(self.plan.read_text(encoding='utf-8'))

    @contextmanager
    def lock(self, session):
        identifier(session)
        self.state.mkdir(parents=True, exist_ok=True)
        path = self.state / 'lock'
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            raise ValueError('Local lock occupied; inspect owner and recover manually, never force-delete automatically') from None
        try:
            with os.fdopen(fd, 'w') as f:
                json.dump({'session': session, 'pid': os.getpid(), 'host': socket.gethostname()}, f)
            yield
        finally:
            path.unlink()

    def status(self):
        j = self.journal()
        digest = self.digest() if self.plan.exists() else None
        checkpoint = self.plan_checkpoint()
        head = git(self.repo, 'rev-parse', 'HEAD')
        return {**j, 'checkpoint': checkpoint, 'fingerprint': digest, 'plan_missing': digest is None,
                'contract_current': bool(digest) and checkpoint.get('fingerprint') == digest,
                'code_head_current': checkpoint.get('head') == head,
                'code_tree_current': checkpoint.get('code_tree') == self.code_tree(),
                'dirty': git(self.repo, 'status', '--porcelain=v1', '--untracked-files=all'),
                'branch': git(self.repo, 'branch', '--show-current'), 'head': git(self.repo, 'rev-parse', 'HEAD'),
                'local_lock': (self.state / 'lock').exists(), 'network': False}

    def code_tree(self):
        """Hash index/worktree/untracked bytes, excluding plan to avoid self-reference."""
        relative = self.plan.relative_to(self.repo).as_posix()
        h = hashlib.sha256()
        for args in (('diff', '--binary', 'HEAD', '--', '.', ':(exclude)' + relative),
                     ('diff', '--cached', '--binary', '--', '.', ':(exclude)' + relative)):
            data = subprocess.run(['git', '-C', str(self.repo), *args], capture_output=True, timeout=30, check=True).stdout
            h.update(data)
        raw = subprocess.run(['git', '-C', str(self.repo), 'ls-files', '--others', '--exclude-standard', '-z'], capture_output=True, timeout=30, check=True).stdout
        for name in sorted(raw.split(b'\0')):
            if not name or os.fsdecode(name) == relative:
                continue
            path = self.repo / os.fsdecode(name)
            h.update(name + b'\0')
            if path.is_symlink():
                h.update(os.fsencode(os.readlink(path)))
            elif path.is_file():
                with path.open('rb') as f:
                    for chunk in iter(lambda: f.read(65536), b''):
                        h.update(chunk)
            h.update(b'\0')
        return h.hexdigest()

    def plan_checkpoint(self):
        text = self.plan.read_text() if self.plan.exists() else ''
        if CHECK_START not in text and CHECK_END not in text:
            return {}
        if text.count(CHECK_START) != 1 or text.count(CHECK_END) != 1:
            raise ValueError('Invalid checkpoint marker pair')
        a, b = text.index(CHECK_START) + len(CHECK_START), text.index(CHECK_END)
        if b <= a:
            raise ValueError('Reversed checkpoint markers')
        contract_end = text.index(END) + len(END)
        if text.index(CHECK_START) < contract_end:
            raise ValueError('Checkpoint must follow contract')
        value = json.loads(text[a:b])
        if not isinstance(value, dict):
            raise ValueError('Checkpoint must be a JSON object')
        return value

    def checkpoint(self, session, stage, next_step, evidence=None, acceptance_ref=None, repair_attempts=None):
        with self.lock(session):
            j = self.journal()
            previous = self.plan_checkpoint()
            identity = {}
            for field, local in (('base', j.get('worktree', {}).get('base')),
                                 ('pr', j.get('publication', {}).get('url'))):
                canonical = previous.get(field)
                if canonical is not None and local is not None and canonical != local:
                    raise ValueError('Local journal conflicts with canonical checkpoint ' + field + '; reconcile explicitly')
                identity[field] = canonical if canonical is not None else local
            # Preserve caller-owned extensions verbatim (including their original
            # source refs). Helper-owned fields below describe this checkpoint.
            # Evidence is only the current argument, never inherited as new proof.
            item = {**previous, 'stage': stage, 'next': next_step, 'evidence': evidence,
                    'session': session, 'fingerprint': self.digest(),
                    'branch': git(self.repo, 'branch', '--show-current'),
                    'head': git(self.repo, 'rev-parse', 'HEAD'),
                    'base': identity['base'],
                    'pr': identity['pr'],
                    'code_tree': self.code_tree(),
                    'checkpoint_sequence': previous.get('checkpoint_sequence', 0) + 1}
            if 'acceptance' in previous:
                item['acceptance'] = previous['acceptance']
            if repair_attempts is not None:
                if repair_attempts < 0:
                    raise ValueError('Repair attempts must be nonnegative')
                item['repair_attempts'] = repair_attempts
            elif 'repair_attempts' in previous:
                item['repair_attempts'] = previous['repair_attempts']
            if acceptance_ref:
                item['acceptance'] = {'fingerprint': item['fingerprint'], 'decision_ref': acceptance_ref, 'verified': False}
            text = self.plan.read_text()
            block = CHECK_START + '\n' + json.dumps(item, ensure_ascii=False, sort_keys=True, indent=2) + '\n' + CHECK_END
            if CHECK_START in text:
                text = text[:text.index(CHECK_START)] + block + text[text.index(CHECK_END) + len(CHECK_END):]
            else:
                text = text.rstrip() + '\n\n' + block + '\n'
            atomic_text(self.plan, text)
            j['checkpoint'] = item
            self.save(j)
            return j

    def start(self, session, worktree, base='HEAD'):
        if self.plan.exists():
            self.digest()
        destination = Path(worktree).expanduser().resolve()
        if destination == self.repo or destination.is_relative_to(self.repo):
            raise ValueError('Worktree must be outside source repository')
        branch = 'raven/' + self.change
        with self.lock(session):
            j = self.journal()
            expected = {'branch': branch, 'path': str(destination), 'base': git(self.repo, 'rev-parse', '--verify', base + '^{commit}')}
            old = j.get('worktree')
            if old and any(old.get(k) != v for k, v in expected.items()):
                raise ValueError('Existing worktree intent differs; inspect journal')
            if destination.exists():
                # Covers recovery after successful Git creation but interrupted journal update.
                if not old or git(destination, 'branch', '--show-current') != branch or Path(git(destination, 'rev-parse', '--git-common-dir')).resolve() != self.state.parent.parent:
                    raise ValueError('Destination exists and is not this journaled worktree')
            else:
                if self.plan.exists():
                    relative_plan = self.plan.relative_to(self.repo).as_posix()
                    committed_plan = subprocess.run(['git', '-C', str(self.repo), 'show', expected['base'] + ':' + relative_plan], capture_output=True, timeout=30)
                    if committed_plan.returncode or committed_plan.stdout != self.plan.read_bytes():
                        raise ValueError('Commit complete current plan before starting its worktree')
                j['worktree'] = {**expected, 'state': 'pending', 'session': session}
                self.save(j)
                git(self.repo, 'worktree', 'add', '-b', branch, str(destination), expected['base'])
            j['worktree'] = {**expected, 'state': 'ready', 'session': session}
            self.save(j)
            return j

    def repository(self):
        path = self.repo / '.raven/config.json'
        if path.is_symlink() or not path.resolve().is_relative_to(self.repo):
            raise ValueError('Config must remain inside repository')
        config = json.loads(path.read_text())
        r = config.get('repository', {})
        if config.get('schema_version') != 1 or not all(isinstance(r.get(k), str) and r[k] for k in ('owner', 'name', 'base_branch')):
            raise ValueError('Explicit schema_version 1 repository owner/name/base_branch required')
        for k in ('owner', 'name'):
            if not re.fullmatch(r'[A-Za-z0-9_.-]+', r[k]) or r[k] in ('.', '..'):
                raise ValueError('Invalid repository identity')
        return config, r

    def publish(self, session, title, body, apply=False, api=None):
        config, r = self.repository()
        branch = git(self.repo, 'branch', '--show-current')
        if not branch or branch == r['base_branch']:
            raise ValueError('Publication requires a change branch')
        marker = '<!-- raven-change:' + self.change + ' -->'
        if len(body.encode()) > 60000 or len(title) > 256:
            raise ValueError('PR title/body exceeds bounded payload')
        payload = {'title': title, 'body': body + '\n\n' + marker, 'head': branch, 'base': r['base_branch'], 'draft': True}
        if not apply:
            return {'action': 'create-draft-pr', 'repository': r, 'payload': payload, 'network': False}
        if config.get('publication', {}).get('mode') != 'draft-pr':
            raise ValueError('Publication mode must be draft-pr (configuration does not grant authorization)')
        api = api or GitHub()
        endpoint = '/repos/' + r['owner'] + '/' + r['name'] + '/pulls'
        with self.lock(session):
            j = self.journal()
            local_head = git(self.repo, 'rev-parse', 'HEAD')
            intent = {'branch': branch, 'base': r['base_branch'], 'repository': r['owner'] + '/' + r['name'], 'marker': marker}
            old = j.get('publication')
            if old and any(old.get(k) != v for k, v in intent.items()):
                raise ValueError('Publication intent differs; inspect journal before proceeding')
            # Exact branch read includes closed PRs; never enumerate a backlog or Project.
            prs = api.request('GET', endpoint + '?' + urllib.parse.urlencode({'head': r['owner'] + ':' + branch, 'state': 'all', 'per_page': 20, 'page': 1}))
            if not isinstance(prs, list) or len(prs) >= 20:
                raise ValueError('PR lookup exceeds one bounded page; resolve explicitly')
            exact = [p for p in prs if p.get('head', {}).get('ref') == branch]
            if any(p.get('base', {}).get('ref') != r['base_branch'] for p in exact):
                raise ValueError('Existing branch PR targets another base; reconcile explicitly')
            matching = [p for p in exact if marker in (p.get('body') or '') and p.get('head', {}).get('repo', {}).get('full_name', '').lower() == intent['repository'].lower() and p.get('base', {}).get('repo', {}).get('full_name', '').lower() == intent['repository'].lower()]
            if len(matching) > 1:
                raise ValueError('Multiple matching PRs require manual reconciliation')
            if matching:
                remote = matching[0]
                state = 'published' if remote.get('state') == 'open' else 'merged' if remote.get('merged_at') else 'closed'
                if state == 'published' and remote.get('head', {}).get('sha') != local_head:
                    state = 'stale-remote'
                j['publication'] = {**intent, 'state': state, 'number': remote['number'], 'url': remote['html_url']}
                self.save(j)
                return j['publication']
            if exact:
                raise ValueError('Existing branch PR lacks verified repository/marker identity; reconcile explicitly')
            if old:
                raise ValueError('Previous publication is unresolved; no blind retry. Reconcile exact branch/marker on GitHub')
            remote_branch = api.request('GET', '/repos/' + intent['repository'] + '/git/ref/heads/' + urllib.parse.quote(branch, safe=''))
            if remote_branch.get('object', {}).get('sha') != local_head:
                raise ValueError('Push exact current HEAD to configured repository before publication')
            j['publication'] = {**intent, 'state': 'pending', 'session': session}
            self.save(j)  # Persist before mutation; an ambiguous result remains pending.
            result = api.request('POST', endpoint, payload)
            result = api.request('GET', endpoint + '/' + str(int(result['number'])))
            if (result.get('head', {}).get('ref') != branch or result.get('base', {}).get('ref') != r['base_branch']
                    or result.get('head', {}).get('sha') != local_head
                    or result.get('head', {}).get('repo', {}).get('full_name', '').lower() != intent['repository'].lower()
                    or result.get('base', {}).get('repo', {}).get('full_name', '').lower() != intent['repository'].lower()
                    or marker not in (result.get('body') or '') or result.get('state') != 'open'):
                raise ValueError('Created PR identity/state readback failed; reconcile pending publication')
            j['publication'] = {**intent, 'state': 'published', 'number': result['number'], 'url': result['html_url']}
            self.save(j)
            return j['publication']


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('GitHub redirect refused; verify repository identity explicitly')


class GitHub:
    """One-page REST adapter: bounded responses/time/retries; writes are never retried."""
    def __init__(self, token=None, opener=None, sleep=time.sleep):
        self.token = token or os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
        if not self.token:
            raise ValueError('Set GH_TOKEN or GITHUB_TOKEN; token is never logged')
        self.opener = opener or urllib.request.build_opener(NoRedirect).open
        self.sleep = sleep
        self.rate = {}

    def request(self, method, endpoint, payload=None):
        if self.rate.get('X-RateLimit-Remaining') == '0' or self.rate.get('Retry-After'):
            raise ValueError('GitHub rate limit requires deferred retry; rate metadata ' + json.dumps(self.rate))
        if not endpoint.startswith('/repos/') or '\n' in endpoint:
            raise ValueError('Only targeted repository endpoints supported')
        data = None if payload is None else json.dumps(payload).encode()
        req = urllib.request.Request('https://api.github.com' + endpoint, data=data, method=method,
            headers={'Authorization': 'Bearer ' + self.token, 'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'raven-runtime'})
        for attempt in range(3 if method == 'GET' else 1):
            try:
                with self.opener(req, timeout=15) as response:
                    self.rate = {k: response.headers.get(k) for k in ('X-RateLimit-Remaining', 'X-RateLimit-Reset', 'Retry-After')}
                    raw = response.read(MAX_BYTES + 1)
                    if len(raw) > MAX_BYTES:
                        raise ValueError('GitHub response exceeds size limit')
                    return json.loads(raw)
            except urllib.error.HTTPError as e:
                self.rate = {k: e.headers.get(k) for k in ('X-RateLimit-Remaining', 'X-RateLimit-Reset', 'Retry-After')}
                retry = e.headers.get('Retry-After')
                wait = int(retry) if retry and retry.isdigit() else 2 ** attempt
                limited = e.code in (403, 429) and (retry or e.headers.get('X-RateLimit-Remaining') == '0')
                reset = e.headers.get('X-RateLimit-Reset')
                if not retry and limited and reset and reset.isdigit():
                    wait = max(wait, int(reset) - int(time.time()))
                if retry and not retry.isdigit():
                    raise ValueError('GitHub Retry-After requires deferred retry; rate metadata ' + json.dumps(self.rate)) from None
                if e.code in (403, 429) and not retry and not (reset and reset.isdigit()):
                    raise ValueError('GitHub rate/access failure; defer retry; rate metadata ' + json.dumps(self.rate)) from None
                if method != 'GET' or attempt == 2 or (e.code < 500 and not limited) or wait > 5:
                    raise ValueError('GitHub HTTP failure ' + str(e.code) + '; rate metadata ' + json.dumps(self.rate)) from None
                self.sleep(wait)
            except (TimeoutError, urllib.error.URLError):
                if method != 'GET' or attempt == 2:
                    raise ValueError('GitHub transport outcome unknown; mutation must be reconciled before retry') from None
                self.sleep(2 ** attempt)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo', default='.')
    sub = p.add_subparsers(dest='command', required=True)
    for name in ('status', 'resume', 'fingerprint', 'start', 'checkpoint', 'publish-pr', 'read-pr'):
        s = sub.add_parser(name)
        s.add_argument('change')
        if name in ('start', 'checkpoint', 'publish-pr'):
            s.add_argument('--session', required=True)
        if name == 'start':
            s.add_argument('--worktree', required=True)
            s.add_argument('--base', default='HEAD')
        if name == 'checkpoint':
            s.add_argument('--stage', required=True)
            s.add_argument('--next', required=True)
            s.add_argument('--evidence')
            s.add_argument('--acceptance-ref')
            s.add_argument('--repair-attempts', type=int)
        if name == 'publish-pr':
            s.add_argument('--title', required=True)
            s.add_argument('--body-file', required=True, type=Path)
            g = s.add_mutually_exclusive_group(required=True)
            g.add_argument('--dry-run', action='store_true')
            g.add_argument('--apply', action='store_true')
        if name == 'read-pr':
            s.add_argument('--number', type=int, required=True)
    a = p.parse_args(argv)
    try:
        runtime = Runtime(a.repo, a.change)
        if a.command in ('status', 'resume'):
            result = runtime.status()
        elif a.command == 'fingerprint':
            result = {'fingerprint': runtime.digest()}
        elif a.command == 'start':
            result = runtime.start(a.session, a.worktree, a.base)
        elif a.command == 'checkpoint':
            result = runtime.checkpoint(a.session, a.stage, a.next, a.evidence, a.acceptance_ref, a.repair_attempts)
        elif a.command == 'publish-pr':
            result = runtime.publish(a.session, a.title, a.body_file.read_text(), a.apply)
        else:
            _, r = runtime.repository()
            if a.number <= 0:
                raise ValueError('PR number must be positive')
            result = selected_pr(GitHub().request('GET', '/repos/' + r['owner'] + '/' + r['name'] + '/pulls/' + str(a.number)))
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, subprocess.SubprocessError) as e:
        p.exit(2, str(e) + '\n')


if __name__ == '__main__':
    main()
