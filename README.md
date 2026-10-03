# Sudo Chuck Check

A pixel-art Chuck Norris and a rotating joke before your interactive Zsh sudo password check.

> Chuck Norris doesn't sudo. The root user asks him for permission.

![Sudo Chuck Check terminal preview](docs/images/sudo-chuck-check-banner.png)

Open [preview.html](preview.html) locally for the interactive before-and-after
preview. These images are illustrative recreations, not archival screenshots.

## How it started

I'm a computer enthusiast, not a programmer. Years ago I found a Groot sudo
signature in a Reddit thread and enjoyed using it. Seeing Paul Hocker's Chuck
Norris plugin for Omarchy gave me the idea to rework it, and I used AI tools to
help build what became **Sudo Chuck Check**.

![Recreated previous Groot sudo signature](docs/images/groot-banner.png)

The [project history](HISTORY.md) tells the story and preserves the original Groot
signature. The Reddit thread and its author are currently unknown; I'd welcome
a link so the original creator can be credited.

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

Download and extract the release ZIP, enter its `sudo-chuck-check` directory, then run:

```sh
python3 install.py
```

Open a new Zsh terminal and preview:

```zsh
sudo_chuck_banner
```

The installer copies the package into `${XDG_DATA_HOME:-~/.local/share}/sudo-chuck-check`,
backs up your `.zshrc`, and adds a marked source block. Reinstalling updates the
package without duplicating the block. `ZDOTDIR` is respected. It does not install
system packages. To add the image dependency on Arch/Omarchy:

```sh
sudo pacman -S --needed imagemagick
```

You can also try it without installing, from a fresh Zsh session:

```zsh
source ./sudo-chuck-check.plugin.zsh
sudo_chuck_banner
```

### Oh My Zsh custom plugin

As an alternative to the installer, put this entire directory at
`${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/sudo-chuck-check` and add `sudo-chuck-check`
to your `plugins=(...)` list. Choose one installation method.

### Upgrading from Chuck Sudo

Run the new installer from this release, then open a new terminal. It replaces the
old `chuck-sudo` source block with `sudo-chuck-check`. The old installation folder
is retained as a rollback copy. `sudo_chuck_banner` and the `SUDO_CHUCK_*` settings
keep their names. For a manual Oh My Zsh installation, replace the old plugin
directory and change the entry in `plugins=(...)` to `sudo-chuck-check`.

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
python3 "${XDG_DATA_HOME:-$HOME/.local/share}/sudo-chuck-check/install.py" --uninstall
```

Open a new terminal afterward. The uninstaller removes its marked source block and
owned package files, preserving other configuration and any added files. Config
backups and disposable `${XDG_CACHE_HOME:-~/.cache}/sudo-chuck-check` image caches remain.
For a manual Oh My Zsh installation, remove `sudo-chuck-check` from `plugins=(...)` and
remove its custom-plugin directory.

## Share or contribute

See [SHARING.md](SHARING.md) for community links, GitHub publishing steps, and a
ready-to-paste [Show and Tell announcement](SHOW-AND-TELL.md).

```sh
python3 -m unittest discover -s tests -v
```

New code: MIT. The historical Groot snippet has an unidentified Reddit source;
see [HISTORY.md](HISTORY.md). Bundled jokes: Oh My Zsh, with its MIT notice preserved under `licenses/`.
The sprite was generated using OpenAI's built-in image tool; its prompt is included.
See [NOTICE.md](NOTICE.md) for credits. Created with AI assistance.
