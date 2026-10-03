#!/usr/bin/python3
"""Display the sudo sprite with a joke, without changing terminal input modes."""
import base64
import fcntl
import hashlib
import os
from pathlib import Path
import struct
import subprocess
import sys
import termios
import textwrap

ASSET = Path(__file__).with_name('chuck-norris.png')
TAGLINE = "Chuck Norris doesn't sudo. The root user asks him for permission."


def protocol():
    override = os.environ.get('SUDO_CHUCK_PROTOCOL')
    if override in ('sixel', 'kitty', 'text'):
        return override
    if os.environ.get('TMUX') or os.environ.get('STY'):
        return 'text'
    term = os.environ.get('TERM', '')
    if os.environ.get('KITTY_WINDOW_ID') or term in ('xterm-kitty', 'xterm-ghostty'):
        return 'kitty'
    if term.startswith(('foot', 'xterm-sixel')):
        return 'sixel'
    # Foot is configured with TERM=xterm-256color here. Identify the actual
    # terminal ancestor instead of sending images to every xterm-like terminal.
    pid = os.getppid()
    for _ in range(24):
        try:
            name = Path(f'/proc/{pid}/comm').read_text().strip()
            if name in ('foot', 'footclient', 'foot-server'):
                return 'sixel'
            status = Path(f'/proc/{pid}/status').read_text().splitlines()
            pid = int(next(s.split()[1] for s in status if s.startswith('PPid:')))
            if pid <= 1:
                break
        except (OSError, ValueError, StopIteration):
            break
    return 'text'


def image_bytes(mode, width, height):
    stamp = ASSET.stat().st_mtime_ns
    key = hashlib.sha256(f'{stamp}:{mode}:{width}:{height}'.encode()).hexdigest()[:20]
    cache = Path(os.environ.get('XDG_CACHE_HOME', Path.home() / '.cache')) / 'sudo-chuck-check'
    target = cache / (key + ('.sixel' if mode == 'sixel' else '.png'))
    try:
        return target.read_bytes()
    except OSError:
        pass
    # Nearest-neighbor sampling keeps the sprite's pixels crisp at display size.
    command = ['magick', str(ASSET), '-sample', f'{width}x{height}']
    command += ['-colors', '128', 'sixel:-'] if mode == 'sixel' else ['png:-']
    data = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                          timeout=3, check=True).stdout
    try:
        cache.mkdir(parents=True, exist_ok=True)
        temporary = target.with_name(target.name + f'.{os.getpid()}.tmp')
        temporary.write_bytes(data)
        temporary.replace(target)
    except OSError:
        pass
    return data


def main():
    joke = sys.argv[1] if len(sys.argv) > 1 else 'Chuck Norris can divide by zero.'
    out = sys.stderr
    rows, cols, xpixels, ypixels = 24, 80, 0, 0
    mode = 'text'
    if out.isatty():
        try:
            rows, cols, xpixels, ypixels = struct.unpack(
                'HHHH', fcntl.ioctl(out.fileno(), termios.TIOCGWINSZ, b'\0' * 8))
        except OSError:
            pass
        rows, cols = rows or 24, cols or 80
        mode = protocol()
    cell_w = xpixels / cols if xpixels else 8
    cell_h = ypixels / rows if ypixels else 16
    image_cols = min(28, max(12, cols // 3))
    image_rows = min(16, max(1, rows - 5))
    pixel_w, pixel_h = int(image_cols * cell_w), int(image_rows * cell_h)
    data = None
    if cols >= 32 and rows >= 10 and mode != 'text':
        try:
            data = image_bytes(mode, pixel_w, pixel_h)
        except (OSError, subprocess.SubprocessError):
            pass
    beside = data is not None and cols >= 60
    text_col = image_cols + 4 if beside else 1
    width = max(1, min(72, cols - text_col - 1))
    lines = textwrap.wrap(joke, width) + [''] + textwrap.wrap(TAGLINE, width)
    # Reserve the entire image rectangle first, so painting it never scrolls
    # its own anchor or leaves the password prompt inside the image.
    if data:
        if beside:
            offset = max(0, (image_rows - len(lines)) // 2)
            lines = [''] * offset + lines
            lines += [''] * max(0, image_rows - len(lines))
        else:
            lines = [''] * image_rows + lines
        # A very short terminal cannot hold the image plus this particular joke.
        if len(lines) > rows - 3:
            data = None
            text_col = 1
            width = max(1, min(72, cols - 2))
            lines = textwrap.wrap(joke, width) + [''] + textwrap.wrap(TAGLINE, width)
    color = '\033[38;5;117m' if out.isatty() and not os.environ.get('NO_COLOR') else ''
    reset = '\033[0m' if color else ''
    out.write('\n')
    for line in lines:
        out.write((' ' * text_col + color + line + reset if line else '') + '\n')
    if data:
        out.write(f'\0337\033[{len(lines)}A\033[2G')
        out.flush()
        if mode == 'sixel':
            out.buffer.write(data)
        else:
            encoded = base64.b64encode(data)
            for start in range(0, len(encoded), 4096):
                chunk = encoded[start:start + 4096]
                more = int(start + 4096 < len(encoded))
                control = f'a=T,f=100,q=2,C=1,m={more}' if start == 0 else f'm={more}'
                out.buffer.write(b'\033_G' + control.encode() + b';' + chunk + b'\033\\')
        out.buffer.flush()
        out.write('\0338')
    out.write('\n')
    out.flush()


if __name__ == '__main__':
    main()
