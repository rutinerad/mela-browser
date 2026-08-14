# Running mela-browser in Docker

`mela-browser` is a small Flask web UI (see `src/mela_browser/`) for browsing your
local Mela catalog in a browser, built on the same read-only `MelaStore` as the `mela`
CLI. This documents running it in a container — e.g. on a Mac mini via
[OrbStack](https://orbstack.dev/) — instead of natively with `uv run`.

## Why a container still needs the Mac

Mela's catalog only exists as a local Core Data SQLite store inside Mela.app's macOS
app-group container (see README.md's "Why Read-only" section). The container doesn't
need to run macOS itself, but the machine hosting it does need the real Mela.app
installed and synced — the container just needs read access to its data directory.

## Quick start

On the Mac mini, with Mela.app installed and OrbStack running:

```bash
docker compose up -d --build
```

This builds the image and starts the server on `http://<mac-mini-host>:8080`.

## How it finds your catalog

`docker-compose.yml` bind-mounts your whole `~/Library/Group Containers` directory
(read-only) into the container at the same relative path under the container user's
home. `mela`'s normal auto-discovery then finds `Curcuma.sqlite` and the external-blob
support directory on its own, the same way it does natively — no need to look up your
Mela app's team ID or pass explicit paths.

If you'd rather mount just the Mela data instead of the whole Group Containers
directory, override the volume with explicit paths and set `MELA_DB_PATH` /
`MELA_SUPPORT_DIR` directly (see README.md's Discovery section for what these point
at).

## Known limitation: LZFSE-compressed images

Some external recipe images are stored LZFSE-compressed and are normally decoded via
macOS's `compression_tool` binary (see CLAUDE.md). That binary is macOS-only and isn't
available inside the Linux container, so those specific images won't render — the
recipe page still loads, and everything else (text, other images, search, export)
works normally. Run `mela doctor` natively on the host if you want to see whether your
catalog relies on this format, or check the container logs for
`warning: skipping image for recipe ...` lines.

## Common commands

```bash
make docker-up      # build and start in the background
make docker-logs    # follow logs
make docker-down    # stop
```
