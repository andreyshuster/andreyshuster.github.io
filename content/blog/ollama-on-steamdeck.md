+++
title = "Running Ollama on a Steam Deck"
date = "2026-05-29T10:00:00-05:00"
draft = false
#
# description is optional
#
# description = "An optional description for SEO. If not provided, an automatically created summary will be used."

tags = ["steamos","ollama","llm","ai","steamdeck"]
+++

I use my Steam Deck in Desktop Mode more than I use it for games. It just sits docked on my desk, and recently I thought - it has 16 GB of RAM and a half-decent GPU, why not run a local model on it?

So I installed Ollama. It mostly worked. A couple of SteamOS-specific things tripped me up, so I am writing it down.

## The /usr problem

First mistake: I ran the official install script. It puts the `ollama` binary in `/usr/local/bin` and drops a systemd unit in `/etc/systemd/system`. Both work fine - until the next SteamOS update wipes them. `/usr` on SteamOS is read-only and gets replaced on every update. Anything you put there is temporary.

So everything has to live under `$HOME`.

## Install into your home dir

```sh
mkdir -p ~/.local/bin
cd /tmp
curl -L https://ollama.com/download/ollama-linux-amd64.tgz -o ollama.tgz
tar -xzf ollama.tgz -C ~/.local
```

The tarball ships `bin/ollama` and some libs, all extracted under `~/.local`. Add it to `PATH` if you do not already have it:

```sh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
ollama --version
```

## GPU

The Steam Deck APU is RDNA 2, reported as `gfx1033`. The ROCm builds inside Ollama do not officially support `gfx1033`, but they do support `gfx1030`, which is close enough to work. You just need to tell ROCm to pretend:

```sh
export HSA_OVERRIDE_GFX_VERSION=10.3.0
```

Without it, Ollama falls back to CPU. It still works, just slower.

## User systemd service

System services live in `/etc/systemd/system`, which is on the read-only partition. User services live in `~/.config/systemd/user/` and survive updates. That is what we want.

```sh
mkdir -p ~/.config/systemd/user
```

Then create `~/.config/systemd/user/ollama.service`:

```ini
[Unit]
Description=Ollama
After=network-online.target

[Service]
ExecStart=%h/.local/bin/ollama serve
Environment="HSA_OVERRIDE_GFX_VERSION=10.3.0"
Restart=on-failure

[Install]
WantedBy=default.target
```

Enable it:

```sh
systemctl --user daemon-reload
systemctl --user enable --now ollama
systemctl --user status ollama
```

If you want it to keep running after you log out of the Plasma session (for example, you SSH in from a laptop later):

```sh
sudo loginctl enable-linger deck
```

## Pulling a model

I started with `llama3.2:3b`. It is around 2 GB and fast enough to feel interactive on the iGPU. Bigger models do load, but anything past 7B starts to feel painful and eats into the memory KDE is also using.

```sh
ollama pull llama3.2:3b
ollama run llama3.2:3b
```

First prompt takes a few seconds to warm up. After that, generation is maybe 15-20 tokens per second on a 3B model. Not fast, but usable for short questions.

For code stuff I switched to `qwen2.5-coder:7b`. Slower, but the answers are noticeably better.

## Move models to the SD card

The internal storage on the Deck fills up surprisingly fast, especially the 64 GB model. Models are big, so put them on the SD card.

```sh
systemctl --user edit ollama.service
```

Add this in the override:

```ini
[Service]
Environment="OLLAMA_MODELS=/run/media/mmcblk0p1/ollama-models"
```

Create the directory first, otherwise Ollama will fail silently and you will be confused for ten minutes like I was. Then:

```sh
systemctl --user restart ollama
```

The SD card is slower than the eMMC, so model load time goes up a bit, but once a model is in VRAM/RAM it does not matter.

## A UI

The terminal gets old fast. I tried two things:

1. The Page Assist browser extension. Talks directly to `http://localhost:11434`, opens a side panel in Firefox. Cheapest setup, instantly useful.
2. Open WebUI in Docker. Heavier, but if you want to use the model from your phone or another machine on the LAN, this is the way.

I am using Page Assist most of the time because it is right there in the browser I already have open.

## What I learned

SteamOS punishes you for installing things the normal Linux way. Once you accept that everything needs to be in `$HOME`, life gets easier. User systemd units are underrated - they survive updates, they do not need sudo, and they are basically the right answer for anything you want to run as a background service on the Deck.

The model is fine. It is not Claude. But for "what is the awk for this", "rephrase this paragraph", "explain this error", a small local model on a handheld is genuinely useful, and the privacy is nice.

*P.S. If a SteamOS update ever does break this, check `~/.local/bin` and `~/.config/systemd/user/` first - they should still be there. The only thing that usually needs re-doing is `systemctl --user daemon-reload`.*
