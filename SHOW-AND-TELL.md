# Chuck Sudo — pixel-art Chuck Norris and rotating jokes in your terminal

I made a standalone Zsh customization on Omarchy: before an uncached sudo password
check, a pixel-art Chuck Norris appears beside a random joke, followed by:

> Chuck Norris doesn't sudo. The root user asks him for permission.

It includes 284 offline jokes, a transparent fighting-stance sprite, and the preview
command `sudo_chuck_banner`. Neither the Omarchy Chuck Norris plugin nor Oh My Zsh
needs to be installed.

Images work through Foot/Sixel or Kitty graphics, with text fallback for other
terminals. The package has an installer that backs up your shell config and an
uninstaller. It requires Zsh and Python 3; pictures also require ImageMagick.

Download the repository ZIP, extract it, enter the directory, and run:

```sh
python3 install.py
```

Open a new Zsh terminal, then try `sudo_chuck_banner` without invoking sudo.
Uninstall with `python3 install.py --uninstall`.

Source and download: https://github.com/s3pp3ku/chuck-sudo

The code and sprite were created with AI assistance. Joke credits and licenses
are included. Feedback from other terminal setups is welcome!
