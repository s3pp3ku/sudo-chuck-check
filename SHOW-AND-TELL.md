# Sudo Chuck Check — from a Reddit Groot signature to pixel-art Chuck Norris

I'm a computer enthusiast, not a programmer. Years ago I saw a Groot sudo
signature in a Reddit thread and enjoyed it enough to use it in my terminal.
It said “I AM (G)ROOT !” and reminded me to use sudo wisely.

![The previous Groot signature, recreated from my saved config](https://raw.githubusercontent.com/s3pp3ku/sudo-chuck-check/main/docs/images/groot-banner.png)

Seeing Paul Hocker's Chuck Norris plugin for Omarchy sparked the idea to rework
that old signature. I used AI tools to help turn the idea into working code.
After trying ASCII Chuck artwork, I settled on a pixel-art fighting stance next
to a rotating joke, with this closing line:

> Chuck Norris doesn't sudo. The root user asks him for permission.

![Illustrative terminal preview of Sudo Chuck Check](https://raw.githubusercontent.com/s3pp3ku/sudo-chuck-check/main/docs/images/sudo-chuck-check-banner.png)

Both images are recreations for the project, not archival screenshots. I no
longer have the original Reddit thread or author's name; if you recognize the
Groot signature, I'd love a link so I can credit its creator.

**Sudo Chuck Check** is standalone: neither Hocker's plugin nor Oh My Zsh needs
to be installed. It includes 284 offline jokes, the sprite, a preview command,
and an installer/uninstaller. It requires Zsh and Python 3; images also require
ImageMagick and a supported terminal such as Foot or Kitty.

Download the repository ZIP, extract it, enter the directory, and run:

```sh
python3 install.py
```

Open a new Zsh terminal and run `sudo_chuck_banner` to preview without invoking
sudo. Uninstall with `python3 install.py --uninstall`.

Source, downloads, and the full story: https://github.com/s3pp3ku/sudo-chuck-check

Code, tests, documentation, and the new sprite were made with AI assistance.
Joke credits and licenses are included. Feedback from other enthusiasts is welcome!
