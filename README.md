# Chuck Sudo

A pixel-art Chuck Norris and a rotating joke before your interactive Zsh sudo password check.

> Chuck Norris doesn't sudo. The root user asks him for permission.

<img src="chuck-norris.png" width="220" alt="Pixel-art Chuck Norris with raised fists in a fighting stance">

Open [preview.html](preview.html) locally for an illustrative banner preview.

## What it does

- Displays a transparent sprite to the left of the joke in sufficiently wide terminals.
- Cycles through 284 bundled Oh My Zsh jokes without repeating until the shell's collection is exhausted.
- Works offline. Paul Hocker's Omarchy plugin, Oh My Zsh, fortune, and cowsay are not required.
- Skips the banner while the usual sudo credential check succeeds.
- Offers `sudo_chuck_banner` to preview without invoking sudo.
- Preserves an existing `sudo` function or alias; in that case only the preview loads.

## Requirements

Linux, Zsh, Python 3.9+, and ImageMagick 7 (`magick`) for images.

Foot uses Sixel; Kitty and Ghostty use the Kitty graphics protocol. Other terminals,
tmux/screen, very small windows, or missing ImageMagick receive text. Protocol output
has automated coverage; the original setup was used in Foot on Omarchy.

This release integrates with **Zsh**, including Oh My Zsh. Omarchy users running
Bash can preview with `python3 render.py`, but the sudo hook requires Zsh.

## Install

Download and extract the release ZIP, enter its `chuck-sudo` directory, then run:

```sh
python3 install.py
```

Open a new Zsh terminal and preview:

```zsh
sudo_chuck_banner
```

The installer copies the package into `${XDG_DATA_HOME:-~/.local/share}/chuck-sudo`,
backs up your `.zshrc`, and adds a marked source block. Reinstalling updates the
package without duplicating the block. `ZDOTDIR` is respected. It does not install
system packages. To add the image dependency on Arch/Omarchy:

```sh
sudo pacman -S --needed imagemagick
```

You can also try it without installing, from a fresh Zsh session:

```zsh
source ./chuck-sudo.plugin.zsh
sudo_chuck_banner
```

### Oh My Zsh custom plugin

As an alternative to the installer, put this entire directory at
`${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/chuck-sudo` and add `chuck-sudo`
to your `plugins=(...)` list. Choose one installation method.

## Options

```zsh
SUDO_QUIET=1 sudo your-command      # skip this banner
export SUDO_QUIET=1                # disable automatic banners for this session
export SUDO_CHUCK_PROTOCOL=sixel   # force Sixel when auto-detection misses it
export SUDO_CHUCK_PROTOCOL=kitty   # force Kitty graphics
export SUDO_CHUCK_PROTOCOL=text    # text only
export NO_COLOR=1                 # disable text color
export SUDO_CHUCK_JOKES=/path/to/jokes.txt
```

Custom joke files use a line containing only `%` between entries. Change the file
before opening a new shell. `command sudo ...` bypasses the wrapper entirely.

The banner uses a noninteractive `sudo -n true` probe before the actual command.
It is a credential-cache heuristic: command-specific sudoers rules, passwordless
commands, and alternate target users may behave differently. Authentication remains
with the real sudo executable. Arguments and its final exit status are preserved.
Noninteractive/stdin/askpass modes and administrative/help/list/edit/shell options
bypass the banner. Output goes to stderr.

## Uninstall

From the extracted directory:

```sh
python3 install.py --uninstall
```

Or run the installed copy:

```sh
python3 "${XDG_DATA_HOME:-$HOME/.local/share}/chuck-sudo/install.py" --uninstall
```

Open a new terminal afterward. The uninstaller removes its marked source block and
owned package files, preserving other configuration and any added files. Config
backups and disposable `${XDG_CACHE_HOME:-~/.cache}/chuck-sudo` image caches remain.
For a manual Oh My Zsh installation, remove `chuck-sudo` from `plugins=(...)` and
remove its custom-plugin directory.

## Share or contribute

See [SHARING.md](SHARING.md) for community links, GitHub publishing steps, and a
ready-to-paste [Show and Tell announcement](SHOW-AND-TELL.md).

```sh
python3 -m unittest discover -s tests -v
```

Code: MIT. Bundled jokes: Oh My Zsh, with its MIT notice preserved under `licenses/`.
The sprite was generated using OpenAI's built-in image tool; its prompt is included.
See [NOTICE.md](NOTICE.md) for credits. Created with AI assistance.
