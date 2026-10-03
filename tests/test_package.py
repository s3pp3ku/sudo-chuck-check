import fcntl
import os
from pathlib import Path
import pty
import struct
import subprocess
import sys
import tempfile
import termios
import threading
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'sudo-chuck-check.plugin.zsh'


class PackageTests(unittest.TestCase):
    def test_migrates_previous_project_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            config = base / '.zshrc'
            original = b'# keep my settings\n'
            config.write_bytes(original + b'\n# >>> chuck-sudo >>>\nsource /old/chuck-sudo.plugin.zsh\n# <<< chuck-sudo <<<\n')
            prefix = base / 'sudo-chuck-check'
            args = [sys.executable, str(ROOT / 'install.py'), '--prefix', str(prefix),
                    '--zshrc', str(config)]
            subprocess.run(args, check=True, capture_output=True)
            self.assertNotIn(b'# >>> chuck-sudo >>>', config.read_bytes())
            self.assertEqual(config.read_bytes().count(b'# >>> sudo-chuck-check >>>'), 1)
            subprocess.run(args + ['--uninstall'], check=True, capture_output=True)
            self.assertEqual(config.read_bytes(), original)

    def test_install_update_uninstall_preserves_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            prefix = base / "files with spaces ' and quotes"
            config = base / '.zshrc'
            original = b'# existing configuration\nalias hello="echo hello"'
            config.write_bytes(original)
            args = [sys.executable, str(ROOT / 'install.py'), '--prefix', str(prefix),
                    '--zshrc', str(config)]
            subprocess.run(args, check=True, capture_output=True)
            installed = config.read_bytes()
            subprocess.run(args, check=True, capture_output=True)
            self.assertEqual(config.read_bytes(), installed)
            self.assertEqual(installed.count(b'# >>> sudo-chuck-check >>>'), 1)
            self.assertTrue(list(base.glob('.zshrc.bak.sudo-chuck-check-*')))
            preview = subprocess.run(['zsh', '-fc', 'source "$1"; sudo_chuck_banner',
                                      'test', str(config)], capture_output=True)
            self.assertEqual(preview.returncode, 0, preview.stderr)
            self.assertIn(b"Chuck Norris doesn't sudo.", preview.stderr)
            self.assertEqual(preview.stdout, b'')
            (prefix / 'keep-me.txt').write_text('added by user')
            subprocess.run(args + ['--uninstall'], check=True, capture_output=True)
            self.assertEqual(config.read_bytes(), original)
            self.assertEqual((prefix / 'keep-me.txt').read_text(), 'added by user')
            self.assertFalse((prefix / 'sudo-chuck-check.plugin.zsh').exists())

    def test_joke_cycle_and_reload(self):
        script = '''source "$1"
source "$1"
_sudo_chuck_pick_joke
count=$(( ${#_SUDO_CHUCK_POOL} + 1 ))
[[ $count == 284 ]] || exit 1
typeset -A seen
seen[$_SUDO_CHUCK_LAST]=1
for (( i=1; i<count; i++ )); do
    _sudo_chuck_pick_joke
    [[ -z ${seen[$_SUDO_CHUCK_LAST]-} ]] || exit 2
    seen[$_SUDO_CHUCK_LAST]=1
done
[[ ${#_SUDO_CHUCK_POOL} == 0 ]] || exit 3
previous=$_SUDO_CHUCK_LAST
_sudo_chuck_pick_joke
[[ $_SUDO_CHUCK_LAST != $previous ]] || exit 4
'''
        result = subprocess.run(['zsh', '-fc', script, 'test', str(PLUGIN)], capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_preserves_existing_sudo(self):
        for definition in ('sudo() { print existing; }', "alias sudo='print existing'"):
            script = definition + '\nsource "$1"\neval sudo'
            result = subprocess.run(['zsh', '-fc', script, 'test', str(PLUGIN)], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, b'existing\n')

    def test_sudo_forwarding_and_bypass_modes(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / 'sudo'
            fake.write_text('''#!/bin/sh
if [ "$#" = 2 ] && [ "$1" = -n ] && [ "$2" = true ]; then
    exit "${PROBE_RESULT:-1}"
fi
printf '%s\\0' "$@"
exit 37
''')
            fake.chmod(0o700)
            cases = [(['-v'], {}, True), (['--validate'], {}, True),
                     (['-H', '-v'], {}, True), (['-v'], {'PROBE_RESULT': '0'}, False),
                     (['-v'], {'SUDO_QUIET': '1'}, False), (['-nv'], {}, False),
                     (['-Sk', 'id'], {}, False), (['--stdin', 'id'], {}, False),
                     (['-k'], {}, False), (['--help'], {}, False),
                     (['-u', 'admin', '-n', 'id'], {}, False),
                     (['-uadmin', '-v'], {}, True),
                     (['echo', 'two words', '*.txt'], {}, True)]
            for args, extra, should_show in cases:
                with self.subTest(args=args, env=extra):
                    master, slave = pty.openpty()
                    chunks = []
                    def read():
                        try:
                            while True:
                                data = os.read(master, 65536)
                                if not data:
                                    break
                                chunks.append(data)
                        except OSError:
                            pass
                    reader = threading.Thread(target=read)
                    reader.start()
                    env = dict(os.environ, PATH=tmp + ':' + os.environ['PATH'], **extra)
                    script = 'source "$1"; shift; sudo_chuck_banner() { print -u2 BANNER; }; sudo "$@"'
                    try:
                        result = subprocess.run(['zsh', '-fc', script, 'test', str(PLUGIN), *args],
                                                stdin=slave, stderr=slave, stdout=subprocess.PIPE,
                                                env=env, timeout=5)
                    finally:
                        os.close(slave)
                        reader.join(timeout=3)
                        os.close(master)
                    self.assertEqual(result.returncode, 37)
                    self.assertEqual(result.stdout, b''.join(a.encode() + b'\0' for a in args))
                    self.assertEqual(b'BANNER' in b''.join(chunks), should_show)

    def test_renderer_text_and_sixel(self):
        for mode, width in [('text', 80), ('sixel', 80), ('sixel', 40), ('kitty', 80)]:
            with self.subTest(mode=mode, width=width):
                master, slave = pty.openpty()
                fcntl.ioctl(slave, termios.TIOCSWINSZ,
                            struct.pack('HHHH', 30, width, width * 8, 480))
                chunks = []
                def read():
                    try:
                        while True:
                            data = os.read(master, 65536)
                            if not data:
                                break
                            chunks.append(data)
                    except OSError:
                        pass
                reader = threading.Thread(target=read)
                reader.start()
                with tempfile.TemporaryDirectory() as cache:
                    env = dict(os.environ, SUDO_CHUCK_PROTOCOL=mode, NO_COLOR='1',
                               XDG_CACHE_HOME=cache)
                    try:
                        result = subprocess.run([sys.executable, str(ROOT / 'render.py'),
                                                 'Chuck Norris can divide by zero.'],
                                                stdout=subprocess.PIPE, stderr=slave,
                                                env=env, timeout=8)
                    finally:
                        os.close(slave)
                        reader.join(timeout=3)
                        os.close(master)
                output = b''.join(chunks)
                self.assertEqual(result.returncode, 0)
                self.assertEqual(result.stdout, b'')
                text = output.split(b'\x1b7')[0]
                self.assertIn(b'root user asks him for permission.', b' '.join(text.split()))
                self.assertTrue(all(len(line) < width for line in text.splitlines()))
                if mode == 'sixel':
                    self.assertIn(b'\x1bP0;1;0q', output)
                    self.assertIn(b'\x1b8', output)
                elif mode == 'kitty':
                    self.assertIn(b'\x1b_Ga=T,f=100', output)
                else:
                    self.assertNotIn(b'\x1b', output)


if __name__ == '__main__':
    unittest.main()
