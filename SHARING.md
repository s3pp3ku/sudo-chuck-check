# Share Sudo Chuck Check

Project: https://github.com/s3pp3ku/sudo-chuck-check

## Share on Omarchy Show and Tell

Open https://github.com/omacom/omarchy/discussions/categories/show-and-tell and
start a discussion using [SHOW-AND-TELL.md](SHOW-AND-TELL.md). It includes the
project's origin story, both banner images, and installation instructions.

The PNGs are in `docs/images/`. The Groot image recreates the preserved signature;
the Chuck image is an illustrative terminal preview. The original Reddit thread
is not known. The draft says this explicitly and invites help identifying it.

The discussion draft is prepared text; it is not automatically posted.

## Share a download

Readers can use **Code → Download ZIP** on GitHub, or download an attached
`sudo-chuck-check-v1.1.0.zip`. The package includes the source, sprite, offline jokes,
project history, previews, installer, uninstaller, and tests.

Recipients extract it, enter the directory, and run `python3 install.py`.

## Publish later updates

From the Git checkout, review and commit your changes, then:

```sh
git push origin main
```

For a versioned release, create a tag and archive (substitute a new version for
future releases):

```sh
git tag v1.1.0
git push origin v1.1.0
git archive --format=zip --prefix=sudo-chuck-check/ --output=sudo-chuck-check-v1.1.0.zip v1.1.0
gh release create v1.1.0 sudo-chuck-check-v1.1.0.zip --title "Sudo Chuck Check 1.1.0" --notes-file CHANGELOG.md
```

## Rebuild the illustrations

`python3 tools/build_previews.py` generates `preview.html` from the saved Groot
signature. It runs only the banner-printing portion, never sudo. Open the HTML
for the interactive comparison. For reproducible PNGs, use Chromium:

```sh
chromium --headless --hide-scrollbars --force-device-scale-factor=1 --window-size=1100,600 --screenshot=docs/images/groot-banner.png "file://$PWD/preview.html?capture=groot"
chromium --headless --hide-scrollbars --force-device-scale-factor=1 --window-size=1100,600 --screenshot=docs/images/sudo-chuck-check-banner.png "file://$PWD/preview.html?capture=chuck"
```

## Compatibility

This is an independent Zsh add-on. Neither the Omarchy Chuck Norris plugin nor
Oh My Zsh is required. Python 3 is required; ImageMagick enables pictures.

The [Omarchy marketplace publishing guide](https://plugins.omarchy.org/publish.html)
requires a manifest and QML entry points. This package is distributed as a terminal
customization through GitHub and community posts.
