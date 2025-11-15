+++
title = "Update SteamOS packages"
date = "2025-11-14T22:23:11-06:00"

#
# description is optional
#
# description = "An optional description for SEO. If not provided, an automatically created summary will be used."

tags = ["steamos","archlinux"]
+++

To update Arch Linux system packages you usually run:

```sh
sudo pacman-key --init
sudo pacman-key --populate archlinux
```

However, for SteamOS is not enough. You will continue to get error about corrupted packages.

SteamOS packages are signed by their own GPG keys and they are need to populated too.

```sh
sudo pacman-key --populate holo
```

You're welcome!
