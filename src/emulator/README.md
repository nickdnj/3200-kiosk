# OS/32 Emulator — a real 1980s minicomputer OS, in the browser

> **Concept.** Runs on the bench kiosk PC (the OptiPlex). Lets a visitor sit
> down and type at **Perkin-Elmer OS/32**, the operating system from the 3280's
> own architecture family, live.

A visitor taps "Sit down at the machine" in the exhibit and gets a touch
terminal into a genuine OS/32 system — booted from bitsavers tapes on a SIMH
**Interdata 32** simulator (the 3280's ancestor architecture). They can list
files, ask the time, read the OS/32 command help, and **compile and run a real
program in Fortran, Pascal, or C** — one tap each.

## What's honest about it

It is **real OS/32**, not a mock. It is **not** a bit-exact 3280 — no such
emulator exists — it's the Interdata-32 architecture family the 3280 descends
from. Label it that way. (See `docs/02-architecture.md` §15.)

## The pieces (all on the kiosk PC under /opt/3280-kiosk)

```
simh/BIN/id32        SIMH Interdata-32 simulator, built from open-simh sources
os32/os32.dsk        the OS/32 disk image (davygoat/simh-os32 kit v1.2)
os32/os32.ini        boots OS/32, brings up MTM on telnet :1026
emu/bridge.py        WebSocket(:7682) <-> telnet(:1026) bridge, in this repo
emulator.html        the touch terminal + on-screen keyboard, in this repo
emu/vendor/          xterm.js (self-hosted, offline-safe)
```

## How it runs (systemd, all auto-start + self-heal)

- **os32.service** — runs `id32 os32.ini`. OS/32 boots, MTM listens on :1026.
- **os32-bridge.service** — runs `bridge.py`. Bridges the browser WebSocket to
  MTM's telnet, stripping telnet negotiation. Deliberately **not** dependent on
  os32.service, so an OS/32 restart never leaves it dead.
- **os32-reset.timer** — restarts OS/32 clean nightly at 05:00, so signon lines
  never exhaust. Restarts the bridge too.

## The terminal page (`emulator.html`)

- **Self-hosted xterm.js** (kiosk is offline in the museum).
- **On-screen keyboard** — conventional layout: backspace top-right (sends
  Ctrl-H, 0x08, which is what OS/32 erases with), return at the home row.
- **Self-healing sign-on** — auto-signs-on as one of fred/wilma/barney
  (account 25). Re-signs-on automatically if it ever sees "SIGNON REQUIRED",
  and rotates users on "DUPLICATE USERNAME". A **⟳ Restart** button gives a
  clean session on demand.
- **Command chips** — one-tap `display files`, `display time`, `help *`, and
  **run a program** in Fortran / Pascal / C (the `*CLG` compile-link-go verbs
  and `cc`).

## Rebuilding the OS/32 side from scratch

```bash
# on the kiosk PC
sudo apt install -y build-essential git python3-websockets ttyd
git clone https://github.com/open-simh/simh /opt/3280-kiosk/simh
cd /opt/3280-kiosk/simh && make id32
curl -fsSL -o /opt/3280-kiosk/os32/os32kit.zip \
  https://github.com/davygoat/simh-os32/releases/download/v1.2/os32kit.zip
cd /opt/3280-kiosk/os32 && unzip os32kit.zip
# then install the three unit files from ../controller and enable them
```

## Known-good OS/32 commands (verified on this image)

`signon fred,25,user1` · `display files` · `display time` · `help *` ·
`help fort` · `forclg hellof` (Fortran) · `pasclg hellop` (Pascal) ·
`cc helloc` (C).

## Not done yet

- **BASIC games** (Star Trek, Wumpus, Lunar Lander). Blocked twice: OS/32's
  `BASIC 03-00` is an undocumented dialect (its `LIST`/`RUN` verbs error), and
  loading custom source onto the disk needs either the FTP path (OS32-FTPd,
  swaps the running process — disk backed up as `os32.dsk.backup`) or the
  OS/32 COPY console-EOF, which resisted blind guessing. A focused session with
  the OS/32 COPY User Guide (bitsavers 48-101F00R00) or OS32-FTPd would unblock
  it. The **three-language compile-and-run demos** stand in for now — arguably
  more authentic, since the 3280 ran Fortran, not BASIC.
