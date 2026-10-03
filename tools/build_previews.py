#!/usr/bin/env python3
"""Rebuild preview.html from the preserved Groot signature, without running sudo.

Render PNGs with Chromium headless, using ?capture=groot or ?capture=chuck.
These are illustrative terminal recreations, not historical desktop captures.
"""
import html
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
original = (ROOT / 'history/groot-original.zsh.txt').read_text()
body = original[original.index('    local G='):original.rindex('    command sudo "$@"')]
assert 'command sudo' not in body
output = subprocess.run(['zsh', '-fc', 'groot_preview() {\n' + body + '\n}; groot_preview'],
                        capture_output=True, text=True, check=True).stdout.strip('\n')

# Convert the original SGR colors to styled spans, retaining spacing and text.
colors = {37: '#dddddd', 94: '#5c8fff'}
indexed = {112: '#87d700', 184: '#d7d700', 124: '#af0000'}
color, bold, offset = '#e6e6e6', False, 0
parts = []
for match in re.finditer(r'\x1b\[([\d;]*)m', output):
    text = output[offset:match.start()]
    if text:
        parts.append(f'<span style="color:{color};font-weight:{700 if bold else 400}">{html.escape(text)}</span>')
    values = [int(n or 0) for n in match[1].split(';')]
    i = 0
    while i < len(values):
        value = values[i]
        if value == 0:
            color, bold = '#e6e6e6', False
        elif value == 1:
            bold = True
        elif value in colors:
            color = colors[value]
        elif value == 38 and values[i+1:i+2] == [5]:
            color = indexed.get(values[i+2], '#e6e6e6')
            i += 2
        i += 1
    offset = match.end()
parts.append(html.escape(output[offset:]))
groot = ''.join(parts)
page = r'''<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sudo Chuck Check — from Groot to Chuck</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#101014;color:#eee;font:16px/1.6 ui-monospace,"DejaVu Sans Mono",monospace;padding:32px}main{max-width:1040px;margin:auto}h1{font-size:30px;font-weight:600;margin:0 0 8px}h2{font-size:18px;font-weight:500;letter-spacing:.03em;margin:0 0 14px}.intro{color:#aaa;max-width:850px;margin:0 0 36px}section{margin:0 0 38px}.terminal{background:#09090c;border:1px solid #35353c;border-radius:12px;overflow:hidden}.topbar{background:#1b1b22;border-bottom:1px solid #35353c;height:40px;display:flex;align-items:center;gap:8px;padding:0 18px}.dot{width:10px;height:10px;border-radius:50%;background:#575762}.title{color:#aaa;font-size:12px;margin-left:12px}.body{padding:20px 24px 22px;min-height:362px}.prompt{color:#eee;font-size:18px}.banner{display:flex;align-items:center;gap:32px;height:272px;margin:4px 0}.banner img{width:225px;max-height:256px;object-fit:contain;image-rendering:pixelated}.copy{max-width:630px;font-size:20px;color:#87d7ff}.copy p{margin:0 0 18px}.copy p:last-child{margin:0}.tagline{color:#ffc981}pre{font:19px/1.4 ui-monospace,"DejaVu Sans Mono",monospace;white-space:pre;margin:20px 0 15px;height:240px}.caption{font-size:13px;color:#92929e;margin:10px 0 0}.actions{margin:16px 0}button{background:#252530;border:1px solid #555;color:white;padding:8px 14px;border-radius:6px;font:inherit;cursor:pointer}a{color:#87d7ff}body[data-capture]{padding:28px;min-height:600px;display:grid;align-items:center}body[data-capture] main{width:1040px}body[data-capture] header,body[data-capture] .actions,body[data-capture] footer{display:none}body[data-capture] section{display:none;margin:0}body[data-capture=groot] #groot,body[data-capture=chuck] #chuck{display:block}@media(max-width:700px){body{padding:16px}.body{overflow:auto}.banner{min-width:680px}pre{font-size:15px}}
</style></head>
<body><main><header><h1>Sudo Chuck Check</h1><p class="intro">From a Groot signature found on Reddit years ago to a Chuck Norris rework inspired by Paul Hocker's Omarchy plugin. An enthusiast's idea, built with help from AI tools.</p></header>
<section id="groot"><h2>Before · The Groot signature</h2><div class="terminal"><div class="topbar"><i class="dot"></i><i class="dot"></i><i class="dot"></i><span class="title">Groot · preserved sudo signature</span></div><div class="body"><div class="prompt">$ sudo -v</div><pre>__GROOT__</pre><div class="prompt">[sudo] password for user: ▌</div></div></div><p class="caption">Recreated from the saved .zshrc signature. Original Reddit thread and author currently unknown.</p></section>
<section id="chuck"><h2>Now · Sudo Chuck Check</h2><div class="terminal"><div class="topbar"><i class="dot"></i><i class="dot"></i><i class="dot"></i><span class="title">Sudo Chuck Check · pixel-art terminal banner</span></div><div class="body"><div class="prompt">$ sudo -v</div><div class="banner"><img src="chuck-norris.png" alt="Pixel-art Chuck Norris in a fighting stance"><div class="copy"><p id="joke">Chuck Norris can power solar panels. At night.</p><p class="tagline">Chuck Norris doesn't sudo. The root user asks him for permission.</p></div></div><div class="prompt">[sudo] password for user: ▌</div></div></div><p class="caption">Illustrative terminal preview. Actual spacing and colors depend on your terminal.</p><p class="actions"><button id="next">Another joke</button></p></section>
<footer>Read the full story in <a href="HISTORY.md">HISTORY.md</a>. Neither preview runs sudo or requests a password.</footer>
</main><script>
const capture=new URLSearchParams(location.search).get('capture');if(['groot','chuck'].includes(capture))document.body.dataset.capture=capture;
const jokes=['Chuck Norris can power solar panels. At night.','Chuck Norris can divide by zero.','Chuck Norris counted to infinity. Twice.'];let index=0;document.getElementById('next').onclick=()=>{index=(index+1)%jokes.length;document.getElementById('joke').textContent=jokes[index]};
</script></body></html>
'''
(ROOT / 'preview.html').write_text(page.replace('__GROOT__', groot))
print('Built preview.html using the saved Groot output.')
