#!/usr/bin/env python3
"""Reject credential artifacts without printing their contents (stdlib only)."""
import argparse
import re
import subprocess
from pathlib import PurePosixPath


def git(*args):
    return subprocess.check_output(['git', *args])


def forbidden_path(name):
    path = PurePosixPath(name.lower())
    base = path.name
    return (
        bool(set(path.parts) & {'.ssh', '.aws', '.gnupg', '.secrets'})
        or base in {'authorized_keys', 'known_hosts', 'credentials', 'credentials.json',
                    'rustdesk.toml', 'rustdesk2.toml', 'tailscaled.state'}
        or base.startswith(('id_rsa', 'id_dsa', 'id_ecdsa', 'id_ed25519'))
        or base == '.env' or (base.startswith('.env.') and base not in {'.env.example', '.env.template'})
        or path.suffix in {'.pem', '.key', '.p12', '.pfx', '.ppk', '.pub'}
    )


PATTERNS = [
    re.compile(rb'-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----'),
    re.compile(rb'(?:ssh-(?:rsa|ed25519|dss)|ecdsa-sha2-nistp\d+)\s+[A-Za-z0-9+/]{40,}={0,3}'),
    re.compile(rb'\bgh[pousr]_[A-Za-z0-9]{30,}\b'),
    re.compile(rb'\bgithub_pat_[A-Za-z0-9_]{40,}\b'),
    re.compile(rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
    re.compile(rb'\btskey-[A-Za-z0-9_-]{20,}\b'),
    re.compile(rb'https://login\.tailscale\.com/a/[A-Za-z0-9]{6,}'),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tracked', action='store_true', help='Scan the complete Git index')
    args = parser.parse_args()
    if args.tracked:
        names = git('ls-files', '-z').split(b'\0')
    else:
        names = git('diff', '--cached', '--name-only', '--diff-filter=ACMR', '-z').split(b'\0')
    failures = []
    checked = 0
    for raw in names:
        if not raw:
            continue
        name = raw.decode('utf-8', errors='surrogateescape')
        entry = git('ls-files', '--stage', '--', name).split(b' ', 1)[0]
        if entry == b'160000':  # Submodule contents belong to their own repository.
            continue
        checked += 1
        data = git('show', ':' + name)
        if forbidden_path(name) or any(pattern.search(data) for pattern in PATTERNS):
            failures.append(name)
    if failures:
        print('BLOCKED: possible credential artifacts (contents suppressed):')
        for name in failures:
            print(' - ' + repr(name))
        print('Keep credentials outside Git or in ignored .local/. Never bypass this check to publish a key.')
        return 1
    print(f'Credential guard passed: {checked} indexed files checked.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
