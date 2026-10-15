#!/usr/bin/env python3
"""Connect to the existing personal Brave profile; never force quit or copy it."""
import argparse
import json
import platform
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

APP = Path('/Applications/Brave Browser.app')
BINARY = str(APP / 'Contents/MacOS/Brave Browser')
ENDPOINT = 'http://127.0.0.1:9222'
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def ready():
    try:
        with OPENER.open(ENDPOINT + '/json/version', timeout=1) as response:
            data = json.load(response)
        return isinstance(data, dict) and bool(data.get('webSocketDebuggerUrl'))
    except (OSError, ValueError, urllib.error.URLError):
        return False


def running():
    result = subprocess.run(['ps', '-axo', 'comm='], capture_output=True, text=True, check=True)
    return any(line.strip() == BINARY for line in result.stdout.splitlines())


def wait_until(predicate, seconds):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.5)
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--restart', action='store_true', help='Allow graceful restart of running Brave if CDP is unavailable')
    parser.add_argument('--check', action='store_true', help='Check CDP only; never launch or restart Brave')
    args = parser.parse_args()
    if ready():
        print('CDP ready at ' + ENDPOINT + '; browser unchanged. Verify MCP browser_tabs next.')
        return 0
    if args.check:
        print('CDP unavailable at ' + ENDPOINT, file=sys.stderr)
        return 1
    if platform.system() != 'Darwin' or not APP.is_dir():
        print('Expected Brave Browser at /Applications on macOS.', file=sys.stderr)
        return 1
    if running():
        if not args.restart:
            print('Brave is running without CDP. Reuse existing restart authorization or obtain it, then use --restart.', file=sys.stderr)
            return 2
        subprocess.run(['osascript', '-e', 'tell application "Brave Browser" to quit'], check=True, timeout=20)
        if not wait_until(lambda: not running(), 15):
            print('Brave did not quit. Resolve any unsaved-work dialog manually; no force quit attempted.', file=sys.stderr)
            return 3
    subprocess.run(['open', '-a', str(APP), '-n', '--args', '--remote-debugging-address=127.0.0.1', '--remote-debugging-port=9222'], check=True, timeout=10)
    if not wait_until(ready, 15):
        print('Brave launched but CDP is unavailable. Inspect launch flags/profile restrictions; do not repeat restarts or replace the profile.', file=sys.stderr)
        return 4
    print('CDP ready at ' + ENDPOINT + ' using the existing Brave profile. Verify MCP browser_tabs next.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (subprocess.SubprocessError, OSError) as error:
        print('Browser setup failed: ' + str(error), file=sys.stderr)
        sys.exit(1)
