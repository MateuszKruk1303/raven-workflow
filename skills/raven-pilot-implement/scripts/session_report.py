#!/usr/bin/env python3
"""Local, read-only Codex telemetry -> redacted Raven Pilot session artifacts."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sqlite3

FIELDS = ('input_tokens', 'cached_input_tokens', 'cache_write_input_tokens',
          'output_tokens', 'reasoning_output_tokens', 'total_tokens')

def timestamp(value):
    t = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if t.tzinfo is None:
        raise ValueError('Timestamp must include timezone')
    return t.astimezone(timezone.utc)

def iso(value):
    return value.isoformat().replace('+00:00', 'Z')

def duration(value):
    if isinstance(value, dict):
        secs, nanos = value.get('secs'), value.get('nanos')
        if type(secs) is int and type(nanos) is int and secs >= 0 and nanos >= 0:
            return secs + nanos / 1e9
    return None

def read_threads(database, root):
    db = sqlite3.connect(database.resolve().as_uri() + '?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    try:
        ids = [root]
        seen = set()
        rows = []
        columns = {r[1] for r in db.execute('PRAGMA table_info(threads)')}
        created_column = ', created_at' if 'created_at' in columns else ''
        while ids:
            ident = ids.pop()
            if ident in seen:
                continue
            seen.add(ident)
            row = db.execute('SELECT id, agent_path, agent_nickname, rollout_path' + created_column + ' FROM threads WHERE id=?', (ident,)).fetchone()
            if row is None:
                if ident == root:
                    raise ValueError('Requested root thread not found: ' + ident)
                rows.append({'id': ident, 'agent_path': ident, 'rollout_path': None})
                continue
            rows.append(dict(row))
            ids.extend(r[0] for r in db.execute('SELECT child_thread_id FROM thread_spawn_edges WHERE parent_thread_id=?', (ident,)))
        return rows
    finally:
        db.close()

def analyze_thread(row, start, end):
    usage = Counter()
    models = Counter()
    outer = Counter()
    executed = Counter()
    statuses = Counter()
    seen_usage, seen_calls, seen_items = {}, set(), set()
    requests = 0
    anomalies = []
    failures = []
    context_sizes = []
    wait_seconds = 0.0
    waits = 0
    interrupted = 0
    parse_errors = 0
    active_in_window = False
    missing_usage_fields = Counter()
    model, effort = 'unknown', 'unknown'
    created = row.get('created_at')
    if isinstance(created, (int, float)) and created >= end.timestamp():
        return None
    path = Path(row['rollout_path']) if row.get('rollout_path') else None
    if path is None or not path.is_file():
        return {'thread_id': row['id'], 'agent': row.get('agent_path') or '/root',
                'available': False, 'reason': 'rollout_missing_window_membership_unknown'}
    with path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            try:
                event = json.loads(line)
                if not isinstance(event, dict) or not isinstance(event.get('timestamp'), str):
                    raise ValueError('Invalid event envelope')
                at = timestamp(event['timestamp'])
            except (ValueError, KeyError, TypeError):
                parse_errors += 1
                continue
            payload = event.get('payload') or {}
            if not isinstance(payload, dict):
                if start <= at < end:
                    active_in_window = True
                    anomalies.append('invalid_payload_shape')
                continue
            event_type = event.get('type')
            if event_type == 'turn_context':
                model = payload.get('model') or model
                effort = payload.get('effort') or effort
            if not start <= at < end:
                continue
            active_in_window = True
            if event_type == 'token_usage_record':
                # Only per-response usage. Never sum thread/turn cumulative totals.
                if payload.get('thread_id') != row['id']:
                    continue
                ident = payload.get('response_id')
                if not ident:
                    ident = ('line', line_number)
                    anomalies.append('usage_without_response_id')
                u = payload.get('usage') or {}
                required = FIELDS[:2] + ('output_tokens', 'total_tokens')
                if not isinstance(u, dict) or not all(type(u.get(k)) is int and u[k] >= 0 for k in required):
                    anomalies.append('invalid_usage_record')
                    continue
                if any(type(u[k]) is not int or u[k] < 0 for k in FIELDS if k in u):
                    anomalies.append('invalid_optional_usage_field')
                    continue
                if u.get('reasoning_output_tokens', 0) > u['output_tokens']:
                    anomalies.append('reasoning_exceeds_output')
                    continue
                if u['cached_input_tokens'] > u['input_tokens']:
                    anomalies.append('cached_input_exceeds_input')
                    continue
                if u['total_tokens'] != u['input_tokens'] + u['output_tokens']:
                    anomalies.append('total_token_mismatch')
                    continue
                if ident in seen_usage:
                    if seen_usage[ident] != u:
                        anomalies.append('conflicting_usage_for_response_id')
                    continue
                seen_usage[ident] = u
                for key in FIELDS:
                    if key in u:
                        usage[key] += u[key]
                    else:
                        missing_usage_fields[key] += 1
                requests += 1
                models[f'{model}/{effort}'] += 1
                context_sizes.append(u['input_tokens'])
            if event_type == 'response_item' and payload.get('type') in ('function_call', 'custom_tool_call'):
                ident = payload.get('call_id') or payload.get('id') or ('line', line_number)
                if ident not in seen_calls:
                    seen_calls.add(ident)
                    outer[payload.get('name') or 'unknown'] += 1
            if event_type == 'event_msg' and payload.get('type') == 'turn_aborted':
                interrupted += 1
            if event_type != 'event_msg' or payload.get('type') != 'item_completed':
                continue
            item = payload.get('item') or {}
            if not isinstance(item, dict):
                anomalies.append('invalid_item_shape')
                continue
            kind = item.get('type')
            ident = (kind, item.get('id') or ('line', line_number))
            if ident in seen_items:
                continue
            seen_items.add(ident)
            if kind not in ('CommandExecution', 'McpToolCall', 'CollabAgentToolCall'):
                continue
            executed[kind] += 1
            status = str(item.get('status') or 'unknown')
            statuses[f'{kind}:{status}'] += 1
            if kind == 'CollabAgentToolCall' and 'wait' in str(item.get('tool', '')).lower():
                a, b = payload.get('started_at_ms'), payload.get('completed_at_ms')
                if isinstance(a, (int, float)) and isinstance(b, (int, float)) and b >= a:
                    wait_seconds += (b-a)/1000
                    waits += 1
            if kind == 'CommandExecution':
                code = item.get('exit_code')
                if (code is not None and code != 0) or status.lower() in ('failed', 'declined', 'interrupted'):
                    # Inspect locally; never export raw command, stdout/stderr or arguments.
                    raw = '\n'.join(str(item.get(k) or '') for k in ('stdout','stderr','aggregated_output','formatted_output'))
                    category = 'command_nonzero_or_failed'
                    if re.search(r'EPERM|EACCES|permission denied|operation not permitted', raw, re.I): category = 'permission_or_sandbox'
                    elif re.search(r'ENOTFOUND|ECONNREFUSED|ETIMEDOUT|could not resolve|connection.*failed', raw, re.I): category = 'connection'
                    elif re.search(r'Unable to acquire lock|another instance.*next|\.next/lock', raw, re.I): category = 'build_lock'
                    elif re.search(r'error TS\d+', raw): category = 'typescript'
                    failures.append({'timestamp': iso(at), 'category': category, 'status': status,
                                     'exit_code': code, 'command_execution_seconds': duration(item.get('duration'))})
    if not active_in_window:
        return None  # Descendant outside this session, not a missing zero-cost worker.
    result = {'thread_id': row['id'], 'agent': row.get('agent_path') or '/root',
              'nickname': row.get('agent_nickname'), 'available': True,
              'models_and_efforts': dict(models), 'model_requests': requests if requests else None,
              'tokens': {k: (None if missing_usage_fields[k] else usage[k]) for k in FIELDS} if requests else None,
              'missing_usage_fields': dict(missing_usage_fields),
              'outer_tool_calls': dict(outer), 'executed_items': dict(executed),
              'executed_item_statuses': dict(statuses), 'command_failures': failures,
              'collaboration_wait_seconds_sum': round(wait_seconds, 3),
              'collaboration_wait_samples': waits, 'interrupted_turns': interrupted,
              'max_input_tokens_per_request': max(context_sizes) if context_sizes else None,
              'mean_input_tokens_per_request': round(sum(context_sizes)/len(context_sizes), 1) if context_sizes else None,
              'malformed_log_lines': parse_errors, 'anomalies': dict(Counter(anomalies))}
    if requests:
        result['tokens']['uncached_input_tokens'] = usage['input_tokens'] - usage['cached_input_tokens']
    return result

def collect(args):
    start, end = timestamp(args.since), timestamp(args.until)
    if end <= start:
        raise ValueError('--until must be after --since')
    warnings = []
    agents = []
    try:
        rows = read_threads(args.database, args.root_thread)
    except (sqlite3.Error, ValueError) as error:
        rows = []
        warnings.append('Thread index unavailable or unsupported; token and tool metrics unavailable: ' + type(error).__name__)
    for row in rows:
        try:
            result = analyze_thread(row, start, end)
        except OSError:
            result = {'thread_id': row['id'], 'agent': row.get('agent_path') or '/root',
                      'available': False, 'reason': 'rollout_unreadable_window_membership_unknown'}
        if result:
            agents.append(result)
    totals = Counter()
    outer = Counter()
    executed = Counter()
    requests = 0
    counted = 0
    missing_totals = set()
    for agent in agents:
        if not agent['available']:
            warnings.append('Missing telemetry: ' + agent['agent'])
            continue
        outer.update(agent['outer_tool_calls'])
        executed.update(agent['executed_items'])
        if agent['tokens'] is None:
            warnings.append('Per-response token records unavailable: ' + agent['agent'])
        else:
            counted += 1
            totals.update({k:v for k,v in agent['tokens'].items() if v is not None})
            missing_totals.update(k for k,v in agent['tokens'].items() if v is None)
            requests += agent['model_requests']
        if agent['anomalies'] or agent['malformed_log_lines']:
            warnings.append('Partial or anomalous log data: ' + agent['agent'])
    notes = json.loads(args.notes.read_text()) if args.notes else {}
    if not isinstance(notes, dict):
        raise ValueError('--notes must contain an object')
    return {'schema_version': 1, 'session_id': args.session_id,
            'generated_at': iso(datetime.now(timezone.utc)),
            'window': {'since_inclusive': iso(start), 'until_exclusive': iso(end),
                       'wall_seconds': (end-start).total_seconds()},
            'root_thread_id': args.root_thread, 'agents': agents,
            'totals': {'tokens': {k:(None if k in missing_totals else totals[k]) for k in sorted(set(totals) | missing_totals)} if counted else None,
                       'model_requests': requests if counted else None,
                       'agents_with_token_data': counted, 'outer_tool_calls': dict(outer),
                       'executed_items': dict(executed),
                       'cache_hit_ratio': totals['cached_input_tokens']/totals['input_tokens'] if totals['input_tokens'] else None},
            'warnings': warnings, 'coordinator_notes': notes,
            'measurement_rules': [
                'Source: local Codex SQLite read-only and JSONL. No network, no raw prompts/commands/output copied.',
                'Tokens: sum usage once per response_id and thread, within [since, until). Cached input is a subset of input; reasoning is a subset of output. Cache writes are not added again to total.',
                'Model requests count recorded responses with valid usage, not HTTP attempts/retries or billing.',
                'Outer tool calls and nested executed items are separate views; do not add them together.',
                'Nonzero command exits include ordinary search misses and expected failures, not only product bugs.',
                'Wait sum includes full durations of operations completed within the window, not clipped overlap. Waits may overlap across agents and useful work; their sum is not session idle time. Malformed-line counts cover whole source files because unreadable events cannot be dated.',
                'Coordinator notes are attributed observations, not inferred telemetry. Token cost, quota consumption and per-task attribution are unavailable.',
                'Report is a snapshot; generation and subsequent messages after until are excluded. Missing metrics are null/explicitly partial, not invented zeros.'
            ]}

def number(n):
    return 'brak danych' if n is None else f'{n:,}'.replace(',', ' ')

def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')

def markdown(report):
    totals = report['totals']; tokens = totals['tokens'] or {}; window = report['window']
    lines = [f"# Raven Pilot — raport sesji {report['session_id']}", '',
             f"Okno UTC: {window['since_inclusive']} → {window['until_exclusive']} ({window['wall_seconds']/60:.2f} min).", '',
             f"Wywołania modelu z usage: **{number(totals['model_requests'])}**. Tokeny: **{number(tokens.get('total_tokens'))}**.",
             f"Wejście poza cache: {number(tokens.get('uncached_input_tokens'))}; cache: {number(tokens.get('cached_input_tokens'))}; wyjście: {number(tokens.get('output_tokens'))}.", '',
             '| Agent | Model/effort (liczba odpowiedzi) | Wywołania | Wejście bez cache | Cache | Wyjście | Razem |',
             '| --- | --- | ---: | ---: | ---: | ---: | ---: |']
    for a in report['agents']:
        t=a.get('tokens') or {}
        models=', '.join(f'{k}: {v}' for k,v in a.get('models_and_efforts',{}).items()) or 'brak danych'
        lines.append('| '+ ' | '.join([cell(a['agent']),cell(models),number(a.get('model_requests')),number(t.get('uncached_input_tokens')),number(t.get('cached_input_tokens')),number(t.get('output_tokens')),number(t.get('total_tokens'))])+' |')
    lines += ['', '## Wywołania narzędzi', '', 'Wywołania zewnętrzne modelu; exec może zawierać kilka operacji. Nie sumować z wykonanymi operacjami poniżej.', '', '| Narzędzie | Liczba |', '| --- | ---: |']
    for k,v in sorted(totals['outer_tool_calls'].items(),key=lambda x:-x[1]):lines.append(f'| {cell(k)} | {v} |')
    lines += ['', 'Operacje zakończone widoczne wewnątrz narzędzi:', '']
    for k,v in totals['executed_items'].items():lines.append(f'- {k}: {v}.')
    errors=Counter(f['category'] for a in report['agents'] for f in a.get('command_failures',[]))
    lines += ['', '## Trudności widoczne w logach', '', 'Niezerowy exit nie musi oznaczać błędu produktu — np. rg bez dopasowania zwraca 1.', '']
    for k,v in errors.items():lines.append(f'- {k}: {v} zdarzeń.')
    for a in report['agents']:
        if a.get('available'):
            lines.append(f"- {a['agent']}: przerwane tury {a['interrupted_turns']}; suma wait zakończonych w oknie {a['collaboration_wait_seconds_sum']:.1f} s; maks. wejście pojedynczego requestu {number(a['max_input_tokens_per_request'])} tokenów.")
    lines += ['', '## Wynik, blockery i poprawki — zapis koordynatora', '']
    notes=report['coordinator_notes']
    if not notes:lines.append('Brak notatek koordynatora; nie wywnioskowano ich z treści rozmów.')
    else:
        for key,value in notes.items():
            lines.append(f'### {cell(key)}');lines.append('')
            if isinstance(value,list):
                for item in value:
                    if isinstance(item, dict):
                        label = item.get('id') or item.get('task') or ''
                        summary = item.get('summary') or item.get('issues') or ''
                        lines.append('- '+(f"**{cell(label)}** — " if label else '')+cell(summary))
                        details = [f"{cell(k)}: {cell(v)}" for k,v in item.items() if k not in ('id','task','summary','issues')]
                        if details:lines.append('  '+ '; '.join(details)+'.')
                    else:lines.append('- '+cell(item))
            elif isinstance(value,dict):
                for k,v in value.items():lines.append(f'- {cell(k)}: {cell(v)}')
            else:lines.append(cell(value))
            lines.append('')
    lines += ['## Ograniczenia pomiaru', '']
    lines += ['- '+s for s in report['measurement_rules']]
    if report['warnings']:lines += ['', 'Ostrzeżenia:', '']+['- '+w for w in report['warnings']]
    return '\n'.join(lines)+'\n'

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database',type=Path,default=Path.home()/'.codex/state_5.sqlite')
    parser.add_argument('--root-thread',required=True)
    parser.add_argument('--since',required=True,help='inclusive ISO8601 with timezone')
    parser.add_argument('--until',required=True,help='exclusive ISO8601 with timezone')
    parser.add_argument('--session-id',required=True)
    parser.add_argument('--notes',type=Path,help='Reviewed non-secret coordinator observations, JSON object')
    parser.add_argument('--output-dir',required=True,type=Path)
    args=parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*',args.session_id):parser.error('Unsafe session ID')
    out=args.output_dir.resolve()
    if any(part in ('archive','archives') for part in out.parts):parser.error('Archives are immutable')
    try:report=collect(args)
    except (OSError,ValueError) as error:parser.error(str(error))
    out.mkdir(parents=True,exist_ok=True)
    targets=[out/'metrics.json',out/'report.md']
    if any(target.exists() or target.is_symlink() for target in targets):parser.error('Output already exists; use a new snapshot directory')
    for target,value in zip(targets,[json.dumps(report,ensure_ascii=False,indent=2)+'\n',markdown(report)]):
        # Exclusive creation: do not overwrite another run or follow output-file symlinks.
        with target.open('x') as stream:stream.write(value)
    print(json.dumps({'output_dir':str(out),'model_requests':report['totals']['model_requests'],
                      'tokens':report['totals']['tokens'],'warnings':report['warnings']},ensure_ascii=False))

if __name__=='__main__':main()
