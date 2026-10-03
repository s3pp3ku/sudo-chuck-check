#!/usr/bin/env python3
"""Install or uninstall Sudo Chuck Check in the current user's Zsh configuration."""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import shlex
import shutil
import sys

ROOT = Path(__file__).resolve().parent
FILES = ('sudo-chuck-check.plugin.zsh', 'render.py', 'chuck-norris.png', 'jokes.txt',
         'LICENSE', 'NOTICE.md', 'licenses/oh-my-zsh-MIT.txt', 'image-prompt.txt',
         'install.py', 'README.md', 'HISTORY.md', 'CHANGELOG.md', 'SHARING.md', 'SHOW-AND-TELL.md',
         'preview.html', 'history/groot-original.zsh.txt',
         'docs/images/groot-banner.png', 'docs/images/sudo-chuck-check-banner.png')
START = b'\n# >>> sudo-chuck-check >>>\n'
END = b'# <<< sudo-chuck-check <<<\n'
MARKER = '.sudo-chuck-check-install.json'


def without_block(content, start_marker=START, end_marker=END):
    if start_marker not in content and end_marker not in content:
        return content
    if content.count(start_marker) != 1 or content.count(end_marker) != 1:
        raise ValueError('Ambiguous Sudo Chuck Check markers in .zshrc; leaving it untouched.')
    start = content.index(start_marker)
    end = content.index(end_marker) + len(end_marker)
    if end <= start:
        raise ValueError('Invalid Sudo Chuck Check markers; leaving .zshrc untouched.')
    return content[:start] + content[end:]


def write_config(path, content):
    if path.exists():
        if path.read_bytes() == content:
            return
        backup = path.with_name(path.name + '.bak.sudo-chuck-check-' +
                                datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
        shutil.copy2(path, backup)
        print('Config backup:', backup)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--uninstall', action='store_true')
    parser.add_argument('--prefix', type=Path, default=Path(
        os.environ.get('XDG_DATA_HOME', Path.home() / '.local/share')) / 'sudo-chuck-check')
    parser.add_argument('--zshrc', type=Path, default=Path(
        os.environ.get('ZDOTDIR', Path.home())) / '.zshrc')
    args = parser.parse_args()
    target = args.prefix.expanduser().resolve()
    config = args.zshrc.expanduser().resolve()
    marker = target / MARKER
    state = json.loads(marker.read_text()) if marker.exists() else None
    if state and (state.get('package') != 'sudo-chuck-check' or state.get('config') != str(config)):
        raise ValueError('Install location belongs to another configuration; use its original --zshrc.')
    content = config.read_bytes() if config.exists() else b''
    cleaned = without_block(content)
    if args.uninstall:
        if not state:
            print('No managed Sudo Chuck Check installation at', target)
            return
        write_config(config, cleaned)
        # Delete only files this installer owns; preserve unrelated additions.
        for name in FILES:
            path = target / name
            if path.is_file() or path.is_symlink():
                path.unlink()
        marker.unlink()
        for path in (target / 'licenses', target / 'history', target / 'docs/images',
                     target / 'docs', target):
            try:
                path.rmdir()
            except OSError:
                pass
        print('Uninstalled. Open a new terminal to unload the function.')
        return
    if not shutil.which('zsh'):
        raise ValueError('Zsh is required. This release does not integrate with Bash.')
    if target == ROOT:
        raise ValueError('Run the installer from the downloaded source directory.')
    if target.exists() and not state and any(target.iterdir()):
        raise ValueError('Install directory already contains unmanaged files; leaving it untouched.')
    for name in FILES:
        if not (ROOT / name).is_file():
            raise ValueError('Missing package file: ' + name)
    # Migrate the previous public name without loading two sudo wrappers.
    # Its old package directory stays on disk as a rollback copy.
    cleaned = without_block(cleaned, b'\n# >>> chuck-sudo >>>\n', b'# <<< chuck-sudo <<<\n')
    # Validate all inputs before making changes.
    source_line = '[[ -r {0} ]] && source {0}\n'.format(
        shlex.quote(str(target / 'sudo-chuck-check.plugin.zsh'))).encode()
    target.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        destination = target / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, destination)
    marker.write_text(json.dumps({'package': 'sudo-chuck-check', 'config': str(config)}, indent=2) + '\n')
    write_config(config, cleaned + START + source_line + END)
    print('Installed at', target)
    print('Open a new Zsh terminal, then run: sudo_chuck_banner')
    if not shutil.which('magick'):
        print('ImageMagick is missing: text works; install imagemagick for the sprite.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as error:
        print('Sudo Chuck Check:', error, file=sys.stderr)
        sys.exit(1)
