"""Exercise staged-byte scanning with synthetic credentials only."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'check_credentials.py'


class CredentialGuardTests(unittest.TestCase):
    def test_staged_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def git(*args):
                subprocess.run(['git', *args], cwd=root, check=True, capture_output=True)

            def scan(*args):
                return subprocess.run(
                    [sys.executable, str(SCRIPT), *args], cwd=root, capture_output=True, check=False
                ).returncode

            git('init')
            cases = [
                ('id_ed25519.pub', 'synthetic', False),
                ('.env', 'EXAMPLE=value', False),
                ('notes.txt', '-----BEGIN ' + 'OPENSSH PRIVATE KEY-----', False),
                ('notes.txt', 'ssh-ed25519 ' + 'A' * 68, False),
                ('notes.txt', 'ghp_' + 'A' * 36, False),
                ('notes.txt', 'https://login.tailscale.com/a/' + '12345678', False),
                ('notes.txt', 'ssh-ed25519 <PUBLIC_KEY>', True),
                ('.env.example', 'TOKEN=<PLACEHOLDER>', True),
            ]
            for name, content, allowed in cases:
                with self.subTest(name=name, allowed=allowed):
                    git('read-tree', '--empty')
                    (root / name).write_text(content)
                    git('add', '--', name)
                    self.assertEqual(scan() == 0, allowed)
                    self.assertEqual(scan('--tracked') == 0, allowed)
            (root / 'notes.txt').write_text('-----BEGIN ' + 'RSA PRIVATE KEY-----')
            git('add', 'notes.txt')
            (root / 'notes.txt').write_text('clean working copy')
            self.assertEqual(scan(), 1)


if __name__ == '__main__':
    unittest.main()
