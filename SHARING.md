# Publish and share Chuck Sudo

## Publish your GitHub repository

The prepared repository is named `chuck-sudo`. From its directory, after reviewing
its files and signing in to GitHub CLI, run:

```sh
gh repo create s3pp3ku/chuck-sudo --public --source=. --push --description "Pixel-art Chuck Norris sudo banner with offline jokes for Zsh"
```

This command creates a public repository on your account and uploads the local
commit. If you downloaded a ZIP instead of using the prepared local Git repository,
first run:

```sh
git init -b main
git add .
git commit -m "Add Chuck Sudo terminal banner"
```

You can also use https://github.com/new and upload the files through GitHub.
Once published, readers can use **Code → Download ZIP**. For a versioned download,
create a `v1.0.0` GitHub release and attach `chuck-sudo-v1.0.0.zip` and its checksum.

## Post on Omarchy Show and Tell

1. Publish the repository so the link in the draft is live.
2. Open https://github.com/omacom/omarchy/discussions/categories/show-and-tell
3. Start a new discussion and use the title and body in [SHOW-AND-TELL.md](SHOW-AND-TELL.md).
4. Attach a screenshot from `sudo_chuck_banner`, or the included sprite.

The repository URL in the draft is the intended destination. Preparing this package
does not itself publish a repository or send a discussion post.

## Share the ZIP directly

You can attach `chuck-sudo-v1.0.0.zip` without setting up GitHub. It includes the
source, sprite, offline jokes, installer, uninstaller, tests, and documentation.
Recipients extract it, enter the directory, and run `python3 install.py`.

## Compatibility

This is an independent Zsh add-on. Neither the Omarchy Chuck Norris plugin nor
Oh My Zsh is required. Python 3 is required; ImageMagick enables pictures.

The [Omarchy marketplace publishing guide](https://plugins.omarchy.org/publish.html)
requires a manifest and QML entry points. This package is distributed as a terminal
customization through GitHub and community posts.
