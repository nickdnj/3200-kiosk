# Warehouse Salvage Recon — Shopping List

> **Status: CONCEPT / v1 recon.** Salvage-first is the standing policy
> ([architecture §9](../docs/02-architecture.md)): reuse what the warehouse has,
> buy new only what can't be scavenged. This is the field list — what to look
> for, how to judge it, and what to write down.

**Reads with:** [`bom.md`](bom.md) ·
[`../mechanical/dimensions-assumed.md`](../mechanical/dimensions-assumed.md) ·
[`../mechanical/measurement-checklist.md`](../mechanical/measurement-checklist.md)

**Ground rule:** *anything you're unsure about, photograph the label plate.* A
model number costs two seconds now and saves an hour later.

---

## Priority order

| | Item | Why this rank |
|---|---|---|
| **1** | **Monitor / LCD panel** | Sets the door geometry. Everything mechanical waits on it. |
| **2** | Momentary buttons | Sets the button plate and the door's minimum depth. |
| 3 | Rack hardware (cage nuts, screws, 19″ blanks) | A 19″ blank panel *is* the frame stock. |
| 4 | Sheet stock (tan or paintable) | Door + frame material. |
| 5 | Hinge / stay / catch hardware | Continuous hinge ≥ 24″ is the hard one to find. |
| 6 | 5 V PSU + USB-C cabling | Cheap to buy new; grab if free. |
| 7 | Pi 4 / SD cards / spares | Have one; spares are welcome. |
| 8 | AC timer or switched relay | Museum-hours scheduling (EL-4). |

---

## 1 · Monitors — the headline item

### Target

> ⚠️ **Retargeted 2026-08-27 — see [`../mechanical/monitor-selection.md`](../mechanical/monitor-selection.md).**
> The carrier panel replaces the cabinet's 24.3″-wide outer door, not a 14.5″
> door in a 19″ opening. A 24″ panel is now **undersized**.

**~27″ 16:9 IPS, 2560×1440, matte, run in portrait.** Active area 23.5″ × 13.2″
→ 13.2″ W × 23.5″ H portrait. 24″ is an acceptable fallback; 32″ a stretch.

### Acceptance criteria — in order of importance

| # | Criterion | Accept | Reject |
|---|---|---|---|
| 1 | **Screen diagonal** | **27″ preferred**; 24″ acceptable | < 21.5″; 32″ only if IPS |
| 2 | **Digital input** | HDMI, DisplayPort, or DVI | **VGA-only** — no |
| 3 | **Native resolution** | **2560×1440** preferred, 1920×1080 min | 1366×768; 4K (Pi 4 rotates it poorly) |
| 3b | **Panel type** | **IPS** — visitors approach off-axis | VA, TN |
| 3c | **Surface** | **Matte / anti-glare** | Glossy — mirrors museum lighting |
| 3d | **Powers on after a mains cut** | **Comes back by itself** | Wakes into standby — ✖ go/no-go, exhibit is on an AC timer |
| 4 | **Backlight type** | LED edge-lit (post ~2012), thin | **CCFL** — thick, dim, needs an inverter |
| 5 | **Panel condition** | Clean, even backlight | Cracks, dead columns/lines, dark corners, yellowing |
| 6 | **Controller board** | Separate small PCB on a ribbon | Board bonded into a big chassis — hard to relocate |
| 7 | **Bezel construction** | Clipped / screwed | Glued or ultrasonically welded — de-casing will kill it |
| 8 | Panel thickness (de-cased) | ≤ 0.7″ | > 1.0″ blows the depth budget |
| 9 | VESA 100×100 holes | Bonus — easy bench mounting | — |

### ⚠ Test it powered before you take it

The de-casing plan (A8.4 / EL-5) is one-way. A panel that turns out to have a bad
backlight after you've stripped the housing is a dead panel.

- [ ] Plugged in, powers on, backlight even across the whole screen
- [ ] Image over HDMI (bring a laptop + cable, or a Pi)
- [ ] No dead columns, no pressure marks, no bright/dark bands
- [ ] Left on for 10 minutes — no flicker, no thermal shutdown

### Take two

**Grab a second acceptable panel if one exists.** De-casing is the single
highest-risk step in the electronics track; the backup costs nothing but a trip.

### Record for every candidate

```
Make / model:            ____________________
Label plate photo:       ☐
Diagonal:                ______″     Native res: ____________
Inputs:                  ☐ HDMI  ☐ DP  ☐ DVI  ☐ VGA
Backlight:               ☐ LED  ☐ CCFL  ☐ unknown
Powers on / image OK:    ☐ yes  ☐ no  ☐ untested
Thinnest depth (calipers): ______″
Bezel: ☐ clipped ☐ screwed ☐ glued
Power input: ☐ internal AC  ☐ external brick ____V ____A
PSU brick present:       ☐ yes  ☐ no      VESA holes: ☐ yes ☐ no
Condition notes:         ____________________
```

### 27″ decision

A 27″ panel (13.2″ × 23.5″ portrait) grows the door to ~15.9″ × 32.7″. **Only
take it if the measured clear opening is ≥ 21″** — at a 19″ opening it leaves
1.5″ of viewing window per side and loses the concept's framed-screen look. It's
also heavier on the hinge. If you find a great 27″ and nothing else, take it and
we re-run the geometry.

### If nothing is salvageable

Buy new: a 24″ 1080p IPS monitor is cheap, and a brand-new one de-cases just as
well as a scavenged one. Note it and move on — don't force a bad panel.

---

## 2 · Buttons

**Need: 3 in use + 2 spares provisioned = 5 matching.** Spares are wired but
unmapped in v1 (ER3 / SW-C3).

| Want | Notes |
|---|---|
| **30 mm arcade** (1.12″ / 28.5 mm mounting hole) | First choice — big, forgiving, public-abuse rated |
| **24 mm arcade** (~1.1″ deep body) | Use if the C1 clearance measures tight — buys 0.3″ of door depth |
| **22 mm industrial panel-mount** | Also fine; more "instrument" than "arcade" |

- Must be **momentary**, not latching.
- Microswitch-actuated preferred (clean edge, long life).
- Illumination is a nice-to-have, not required — v1 doesn't drive LEDs.
- **All five identical.** Mismatched buttons look like a repair, not a design.

Hunting grounds: arcade cabinets, test equipment front panels, industrial
control panels, old lab gear.

- [ ] Count found: ______  Type: ______________  Depth behind panel: ______″

---

## 3 · Rack hardware

The preferred mount (candidate A) turns the fixed frame into a **19″ rack
panel** — so rack stock is directly useful, not just fasteners.

- [ ] **19″ blank rack panels** — any U height; tall ones (8U+) are gold
- [ ] Cage nuts + rack screws (10-32, M6 — grab a mixed handful of each)
- [ ] Rack ears / L-brackets / angle stock
- [ ] Rail sections, if any loose ones exist

> Bring a **cage nut and rack screw** with you to test-fit the 3280's rails —
> that single test decides the mounting method (checklist §B4).

---

## 4 · Sheet stock & mechanical

| Item | Looking for |
|---|---|
| Sheet for door + frame | Aluminum 0.050–0.080″, or ABS/HDPE. Tan or paintable. ~4 sq ft total. |
| **Continuous (piano) hinge** | ≥ 24″ long — the hardest item on this list to find |
| Friction / detent hinges | Alternative to a stay for hold-open (MR6) |
| Small gas struts | Laptop-lid or cabinet-lid size, for a ~12 lb door |
| Magnetic or ball-detent catches | Holds the door closed |
| Nylon / felt pads, grommets | **Required** at every contact point with the artifact |
| Standoffs (M2.5 for the Pi, M3 general), nylon washers | |
| Split loom / spiral wrap | Hinge service loop dressing |

- [ ] **Tan scrap panel for paint matching** — a removable offcut in the 3280's
      finish, taken to a paint store, closes MR13 cheaply. Highest-value small win
      on this list.

---

## 5 · Power & compute

- [ ] 5 V 3–4 A PSU (USB-C preferred, barrel acceptable) — or a good USB-C charger
- [ ] USB-C cable, 3–6 ft
- [ ] IEC cords, a decent power strip
- [ ] **AC timer or switched relay** for museum-hours scheduling (EL-4)
- [ ] Raspberry Pi 4 / 5, PSUs, heatsinks — spares welcome
- [ ] Micro HDMI → HDMI adapters/cables (Pi 4 needs micro)
- [ ] SD cards — **buy new**, don't salvage. Reliability item (NFR4).

---

## 6 · Things NOT to take

- CCFL-backlit or VGA-only monitors — dead ends
- Anything requiring a hole in the 3280 to use
- Adhesive-mount hardware intended for original surfaces
- Latching (non-momentary) switches
- Salvaged SD cards or salvaged mains wiring

---

## After the trip

1. Fill in the record blocks above and commit this file.
2. Update [`bom.md`](bom.md): move salvaged items to **Have**, leave the rest as **Buy**.
3. If a panel came home: measure its real outline and thickness, and update
   [`dimensions-assumed.md`](../mechanical/dimensions-assumed.md) §D3.
4. Comment on [EL-1](https://github.com/nickdnj/3200-kiosk/issues/20) and
   [EL-5](https://github.com/nickdnj/3200-kiosk/issues/24) with what turned up.
