#!/usr/bin/env python3
"""Validate snapshot envelope and hash exact contract JSON; never mutates GitHub."""
import argparse
import hashlib
import json
from pathlib import Path


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate JSON key: {key}')
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f'Non-JSON numeric constant: {value}')


def fingerprint(raw):
    value = json.loads(raw, object_pairs_hook=unique_object, parse_constant=reject_constant)
    if not isinstance(value, dict) or set(value) != {'requirements', 'plan', 'phases'}:
        raise ValueError('Expected exactly requirements, plan, phases; exclude status/progress/evidence')
    if not isinstance(value['requirements'], str) or not isinstance(value['plan'], str):
        raise ValueError('requirements and plan must contain exact contract text')
    if not isinstance(value['phases'], list) or any(not isinstance(p, dict) for p in value['phases']):
        raise ValueError('phases must be an ordered array of contract objects')
    canonical = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)
    return hashlib.sha256(canonical.encode('utf-8')).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('snapshot', type=Path)
    parser.add_argument('--expect', help='Compare against an existing fingerprint')
    args = parser.parse_args()
    try:
        actual = fingerprint(args.snapshot.read_text(encoding='utf-8'))
    except (ValueError, OSError) as error:
        parser.exit(2, f'{error}\n')
    print(actual)
    if args.expect and actual != args.expect:
        parser.exit(1, 'Fingerprint mismatch; review does not cover the changed contract\n')


if __name__ == '__main__':
    main()
