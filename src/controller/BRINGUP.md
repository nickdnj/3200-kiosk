# Bring-up — the mini PC and the panel, from scratch

> **Concept.** Nothing here is installed in the museum. This procedure **was
> run on 2026-09-14** against Doug's donated Dell OptiPlex 9020M and Acer
> T232HL: Steps 1–3 and 5 are done and the result survives a cold reboot.
> Step 4 (Gate 1, the power-cut test) has **not** been run on the monitor.
> Keep this page as the rebuild procedure and as the checklist for any second
> machine.

Doug's donation removed the two purchases that were blocking Rev 3 — a
touchscreen and a mini PC. It also replaced a *known* platform (the
architecture doc specified a Raspberry Pi 4) with an *unknown* one. Everything
below is about closing that gap cheaply, in an order where each answer is
worth having before you spend money or time on the next one.

**Known so far:** OptiPlex 9020M (Intel, SSD, Ubuntu 24.04 installed, GNOME
kept as a fallback session), Acer T232HL 23" touchscreen at a native
1920×1080, touch as a standard USB HID digitizer, rotation `right`. The
architecture doc's compute section still names the Pi; §15 is the ADR that
replaces it.

Do these on a desk with a keyboard attached. Not on a ladder.

---

## Step 0 — what did Doug actually give us?

Before deciding anything. Boot whatever is on it, or a Linux USB stick, and:

```bash
# the machine
sudo dmidecode -s system-manufacturer -s system-product-name -s bios-version
nproc; free -h; lsblk -d -o NAME,SIZE,MODEL

# the graphics, and what it can drive
lspci -nn | grep -Ei 'vga|display|3d'
ls /sys/class/drm/            # which connectors exist: HDMI-A-1, DP-1, ...

# ports actually in use
xrandr --query 2>/dev/null || DISPLAY=:0 xrandr --query
```

**What you are looking for, and why it matters**

| Finding | Why it decides something |
|---|---|
| RAM < 4 GB | Fine. This is one static HTML file, not a browser farm. 2 GB is ample. |
| eMMC rather than SSD | Fine for read-mostly, but plan the read-only overlay (arch doc A2.3) — an exhibit that power-cuts nightly will corrupt a writable eMMC eventually. |
| HDMI 1.4 only | Check it will do 1920×1080 @ 60 Hz. It will. Portrait is a rotation, not a mode. |
| No VESA-capable GPU driver | Rare on any Intel/AMD mini PC. If it happens, that machine is the wrong machine. |
| Windows licence sticker | Irrelevant to us, but **do not wipe** until Doug confirms he doesn't want it back. |

Write the answers into `docs/02-architecture.md` §15 — sections 1–14 still
say Raspberry Pi 4 and the ADR is where the real platform is recorded.

---

## Step 1 — the panel, landscape first

Plug it in. Don't rotate anything yet.

```bash
DISPLAY=:0 xrandr --query
```

Confirm the native mode is **1920×1080**. If it reports something else, stop
and tell me — the kiosk is built for a 1080×1920 portrait box and the build
takes `--panel` for the diagonal, but a non-1080 panel changes the arithmetic.

Also read the label on the back and note the **model number**. We need the
real panel size and the bezel depth for the mechanical side, and "24 inch" on
a box is not a measurement.

---

## Step 2 — does Linux see the touch? *(Gate 2, first half)*

```bash
xinput list
# expect a device with "Touch" or a digitizer name, under "slave pointer"

# confirm it is a real multitouch digitizer, not a mouse emulation
xinput list-props "<that device name>" | grep -i 'libinput\|Calibration'
libinput list-devices | grep -A6 -i touch
```

A generic USB touchscreen presents as a **USB HID digitizer** and is driven by
the in-kernel `hid-multitouch` module with no driver install at all. If it
shows up here, you are done — this is the single most likely thing to have
silently failed, and it didn't.

If it does **not** appear: `dmesg | tail -40` right after plugging the USB
cable in. Note that touch is a *separate USB cable* from the video — a panel
with only HDMI connected will show a perfect picture and no touch at all,
which looks exactly like a broken touchscreen.

---

## Step 3 — does the touch rotate with the screen? *(Gate 2, second half)*

This is the bug that bites every portrait kiosk. The display and the digitizer
are two independent devices. Rotating the picture does **not** rotate the
touch, so your finger lands 90° away from where you pressed.

```bash
sudo ./rotate.sh right     # rotates the picture AND applies the touch matrix
```

Then open the built app and **hold the top-left corner for 3 seconds** — the
kiosk has a built-in diagnostics panel for exactly this. It reports screen
size, device pixel ratio, orientation, `maxTouchPoints`, and the coordinates
of your last touch. Press each corner and watch the numbers.

- Picture upside down → use `left` instead of `right`.
- Picture right, touch mirrored → you have the right rotation and the wrong
  matrix; try the other of `left`/`right` in `rotate.sh` for the matrix only.

---

## Step 4 — does it come back by itself? *(Gate 1)*

The exhibit will lose power. Nobody will be there when it does.

1. In the BIOS, set **Restore on AC Power Loss → Power On**. Naming varies:
   "After Power Failure", "AC Back Function", "State After Power Loss".
2. Boot to the kiosk, then **pull the plug at the wall**. Not a shutdown — a
   power cut, which is what actually happens.
3. Plug back in, hands off, and time it. It must reach the exhibit screen with
   nobody touching anything.
4. Repeat for the **monitor** — some panels come back in standby and need
   their own button.

If either needs a human, it is not finished, however good it looks.

---

## Step 5 — install

```bash
cd src/controller
sudo ./install.sh
sudo reboot          # and watch the whole cold chain come up
```

Then leave it running for a **week** on the bench before it goes in the
cabinet. Unattended-uptime bugs are time bugs: memory growth, log filling,
a nightly update stealing the screen. A week on a desk is free; a week of a
dark exhibit is not.

---

## What is still unknown after all of this

- **The panel's real illuminated rectangle.** Still ungated for mechanical
  (`mechanical/fab-rev1/_p1.py` refuses to release P1 until `ACT_MEASURED`).
  Rev 3 has no face plate, so this no longer blocks the build — but it does
  set where the arm has to put the screen.
- **Whether the arm's pole matches 1¼" EMT** (Gate 3) — caliper it.
- **The door aperture height** (Gate 4) — needs the tape and the photographs.
- **Whether the museum will expose the card cage** (Gate 5) — curatorial, not
  technical, and Rick's call.
