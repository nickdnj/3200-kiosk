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

## Guided lessons (`emulator.html`, the Lessons card)

A card between the terminal and the command chips, open on arrival. Three
lessons, each a handful of steps; every step explains one idea in a sentence
and has a button that **types the command into the live terminal**, character
by character, so a school kid sees it happen and can then do it themselves
on the keyboard.

| Lesson | What it types |
|---|---|
| Look around | `display time`, `display files`, `help *` |
| Run a program | `type hellof.ftn`, `forclg hellof`, `pasclg hellop` |
| Write your own | `l edit32;st`, `a`, a six-line Fortran program, an empty line, `save T####.ftn`, `end`, `display files,T####.ftn`, `forclg T####`, then `delete` of the `.ftn`, `.obj` and `.tsk` |

Every command was run against this disk image before shipping
(2026-09-16). Two things the image taught us:

- **A new file is built with `A[PPEND]`, not `INS[ERT]`.** INSERT on an empty
  buffer says `!NO TEXT`, and a Fortran `END` line typed outside insert mode
  is taken as the editor's own END command.
- **FORTRAN VII prints with `TYPE *,`**, as the kit's `hellof.ftn` does.
  `WRITE(6,*)` compiles clean and then pauses the task with `ERR 25 LU # 6`,
  because nothing is assigned to unit 6.

**Nothing is permanent.** The visitor's program gets a random name
(`T` + four digits, so three concurrent visitors never collide), and it is
deleted by the last lesson step, by the Restart button, and when the visitor
leaves the page. The walk-away path also sends an empty line, `end` twice and
`cancel` first, so a visitor who left mid-editor or with a paused task does
not strand the line. `forclg` leaves `.OBJ` and `.TSK` beside the source;
all three are deleted. (`forclg hellof`, the pre-existing chip, still leaves
`HELLOF.OBJ`/`.TSK` on the disk as it always has.)

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

## Testing without the kiosk

The whole stack runs on a Mac in a few minutes: build `id32` from open-simh,
unzip the v1.2 kit, `tail -f /dev/null | id32 os32.ini`, run `bridge.py`,
serve this folder over `http://127.0.0.1` with xterm.js in `vendor/`, and open
`emulator.html`. `bridge.py` accepts both the websockets 10.x handler
signature (Ubuntu's `python3-websockets`) and 11+.

## Not done yet

- **BASIC games** (Star Trek, Wumpus, Lunar Lander). Blocked twice: OS/32's
  `BASIC 03-00` is an undocumented dialect (its `LIST`/`RUN` verbs error), and
  loading custom source onto the disk needs either the FTP path (OS32-FTPd,
  swaps the running process — disk backed up as `os32.dsk.backup`) or the
  OS/32 COPY console-EOF, which resisted blind guessing. A focused session with
  the OS/32 COPY User Guide (bitsavers 48-101F00R00) or OS32-FTPd would unblock
  it. The **three-language compile-and-run demos** stand in for now — arguably
  more authentic, since the 3280 ran Fortran, not BASIC.
