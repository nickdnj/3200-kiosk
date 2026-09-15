# Controller — the kiosk runtime

> **Concept.** Not installed in the museum. These scripts are **deployed and
> running on the bench kiosk** — Doug's donated Dell OptiPlex 9020M driving
> an Acer T232HL touchscreen, Ubuntu 24.04 — since 2026-09-14, and proven to
> come back on their own after a cold reboot. `BRINGUP.md` is the from-scratch
> procedure if that machine ever has to be rebuilt.

What makes the exhibit come up by itself and stay up. As of Rev 3 there are no
buttons, no GPIO and no daemon: this is display rotation, touch remapping, a
locked-down browser, and a supervision chain.

```
BRINGUP.md           The from-scratch bring-up of a fresh machine, in order.
install.sh           one-shot install onto a fresh Debian/Ubuntu machine
kiosk.sh             launches Chromium with the kiosk flag set
rotate.sh            rotates the panel AND the digitizer (they are separate)
os32.service         the OS/32 emulator (see ../emulator/)
os32-bridge.service  websocket <-> telnet bridge for the terminal screen
os32-reset.service   nightly clean restart of OS/32
```

## What is still open on the bench machine

- **Read-only root.** The disk is writable and the exhibit will be power-cut
  nightly. The emulator also writes to its disk image. #13.
- **Golden image and re-image procedure.** The OptiPlex is the only copy of
  itself. #17.
- **Network posture.** Wi-Fi is on for updates; production is offline and
  inbound-locked, and the emulator bridge should bind to loopback only. #16.
- **Full-hang watchdog.** The loop restarts Chromium; nothing reboots a frozen
  machine. #15.
- **Gate 1.** The monitor has not yet been power-cut tested. #23.

## The supervision chain

One start path, not two — a systemd unit *and* an `.xinitrc` would race each
other for the display.

```
BIOS power-on  ->  agetty autologin  ->  .bash_profile  ->  startx
                ->  .xinitrc  ->  while true  ->  kiosk.sh
```

- Chromium dies → the loop restarts it in 3 s.
- X dies → `startx` exits, agetty respawns the login, X comes back.
- The machine dies → the BIOS setting brings all of it back.

That last one is not something a script can do, and it is the single most
common way a museum kiosk ends up dark. `install.sh` says so on the way out.

## Why X11 and not Wayland

Portrait rotation plus touch remapping is one `xrandr --rotate` and one
`xinput` calibration matrix. On Wayland it is compositor-specific and has
moved between releases. An unattended exhibit that must self-recover after a
power cut is the wrong place to be clever.

## The bug this exists to prevent

The display and the digitizer are **two independent devices**. Rotating the
picture does not rotate the touch, so your finger lands 90° from where you
pressed — and it looks like a broken touchscreen rather than a config problem.
`rotate.sh` sets both, and the kiosk app has a diagnostics panel (hold the
top-left corner for 3 seconds) that reports orientation, touch points and your
last touch coordinates so you can confirm it on the glass.

## What used to be here

Rev 1/2 planned a GPIO button bridge synthesising key events through `uinput`.
Rev 3 deleted it — an entire electronics subsystem removed. If touch
disappoints on the floor, the app still answers arrow keys and `Home`, so
switches can come back without touching a line of content.
