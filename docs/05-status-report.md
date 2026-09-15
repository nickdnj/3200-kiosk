# 3280 Kiosk — Project Status Report

**As of 2026-09-15** · repo [nickdnj/3280-kiosk](https://github.com/nickdnj/3280-kiosk)
· written as a **handoff for anyone joining now**

> **Concept.** Nothing here is installed in the museum. There is a working
> kiosk on a bench. The gap between those two sentences is this document.

The previous edition of this report (2026-08-28) described a Rev 1 design:
a wooden box, a Raspberry Pi and three physical buttons hung on the 3280's
door. **That design no longer exists.** It is preserved in git history (the version of this file before
2026-09-15) and nothing in it should be acted on except the cabinet
measurements, which are repeated below.

---

## 0. Read this first

An interactive exhibit kiosk for the Vintage Computer Federation museum's
**Concurrent 3280** minicomputer. A portrait touchscreen floats in front of
the open card cage on a conduit spine. Three on-screen commands — **BACK /
HOME / NEXT** — step through a deck of screens telling the machine's story,
and a final screen lets a visitor type at a live **OS/32** system.

**Phase:** Rev 3. Software is built and running on the real hardware, on a
bench. Mechanical is a concept page and nothing else. Nothing has been
installed, soaked, or signed off.

**The three things to know:**

1. **The hardware is donated and already running.** Doug Crawford gave a
   Dell OptiPlex 9020M and an Acer T232HL 23″ touchscreen. On 2026-09-14
   they became a working kiosk over SSH: Ubuntu 24.04, X11, Chromium in
   kiosk mode, portrait rotation with the touch digitizer remapped, proven
   across a cold reboot. The Raspberry Pi, the GPIO buttons, and the whole
   electronics subsystem were deleted by that donation.
2. **The mechanical design is Rev 3: doors off, conduit spine, monitor arm.**
   Both factory doors lift off their pins and go into storage. A length of
   1¼″ EMT stands on the cabinet floor and a monitor arm hangs the screen
   off it. Nothing is cut, drilled, or fastened to the machine. This exists
   as `mechanical/rev3-touch-concept.html` and as five unanswered gates. No
   parts have been bought, measured, or drawn.
3. **The issue tracker was reconciled with Rev 3 on 2026-09-15.** Before that
   date all 39 issues described the deleted design. §7 lists what was closed
   and what was re-scoped.

---

## 1. The product

| | |
|---|---|
| Interaction | Three on-screen touch targets: BACK / HOME / NEXT. Arrow keys and `Home` drive it identically. No swipe, no gestures |
| Display | Acer T232HL, 23″ IPS touch, 1080 × 1920 portrait |
| Compute | Dell OptiPlex 9020M, Ubuntu 24.04, X11, Chromium kiosk, `file://`, offline in production |
| Content | 22 screens in `src/kiosk-app/_deck.py`, plus a live OS/32 terminal |
| Content bar | Docent-set: ~30% of web copy, 3–5 bullets/screen, big sans-serif, readable at 3–6 ft, verified facts only |
| Touch row | 38″ above finished floor, set by ADA §308. Unchanged from Rev 1 |
| Hard constraint | The 3280 is a **museum artifact**. Reversible and non-destructive, always |
| Success | Ownership transfers to the museum. "Nick-in-the-loop forever" is failure |

Exhibit review authority is the museum team (Doug Crawford), not any one
docent. The original content review that set the bar above was against Rev 1
concept art; the copy survived the pivot verbatim, the art did not.

---

## 2. What is done

### Software — on the bench, working

| Piece | State | Where |
|---|---|---|
| Deck content | 22 screens, all pass the fit check, tightest content screen 6.9% slack | `src/kiosk-app/_deck.py` |
| Panel build | Self-contained 1080 × 1920 page, fonts and images inlined, asserts no network reference survives | `build-kiosk.py` → `dist/kiosk/index.html` |
| Fit check | Renders the real build in headless Chrome and measures every screen against its box | `check-fit.py` |
| Concept review page | Same content in the cabinet mock-up, for review | `build-app.py` → `index.html` |
| Kiosk runtime | agetty autologin → startx → loop → `kiosk.sh`. Chromium dies, back in 3 s. X dies, back via agetty. Cold-reboot proven | `src/controller/` |
| Portrait + touch | `rotate.sh` rotates the picture and applies the digitizer matrix. Diagnostics panel: hold the top-left corner 3 s | `src/controller/rotate.sh` |
| OS/32 emulator | Real OS/32 on a SIMH Interdata-32, websocket bridge, touch terminal with on-screen keyboard, one-tap Fortran / Pascal / C demos, nightly clean reset | `src/emulator/` + three systemd units |
| Idle reset | 75 s to Home, suppressed while a video slide plays | built in |
| Team page clearance | Cleared for public by Ruth Yeager, 2026-09-15 | commit `ec6b33f` |

### The deck, as of today

| # | Section | Screen |
|---|---|---|
| 1 | Home | The Concurrent 3280 was made in New Jersey |
| 2 | What it did | One machine, many jobs |
| 3 | · weather | Behind the nation's storm radar (NOAA NEXRAD footage, public domain) |
| 4 | · space | It trained the Shuttle crews |
| 5 | · finance | Built to never drop a trade |
| 6 | Under the hood | Big iron, built by hand |
| 7 | · the system | Four boards, one bus (block diagram: processor, S-bus, memory, I/O) |
| 8 | · the processor | One processor, four boards (FET / VAT / ALU / MPY + the four-stage pipeline) |
| 9–12 | · FET · VAT · ALU · MPY | One screen per board: what it does, a diagram, who built it |
| 13 | Where it was born | Made in Monmouth County |
| 14 | · lineage | Sixty years, one New Jersey lab |
| 15 | Who built it | Built by a small team |
| 16 | The team | Sixteen engineers, one lab (the Cruncher 2 roster) |
| 17 | Bring-up | Cruncher lives (1985–86, with the CRUNCHER LIVES illustration) |
| 18 | A quiet first | The line that set Unix free |
| 19 | Just down the room | Two machines, one designer (cross-link to the SGI Onyx) |
| 20–22 | Open it up | Three full-bleed photographs of the card cage, processor, memory and control |
| 23 | Try it yourself | The OS/32 terminal |

The six architecture screens (added 2026-09-15) are sourced from Concurrent's
own manuals on bitsavers. *System Bus Theory* 63-002 R00 (1987) Fig. 1-1 names
the four processor boards **VAT / FET / ALU / MPY**; the *Product Overview*
50-045R00 (1989) pp.29–35 gives the four-board processor, the pipeline stages,
caches, prefetch, multiplier and register sets. This corrects the wiki's
earlier inference that the boards were FETCH / DECODE / ALU / WRITE-BACK; the
wiki has not yet been updated.

Two slides were removed on purpose: the multiprocessor slide (the museum's
unit is a 3280, not the 3280E MPS) and the Defense slide (at Nick's request).

### Mechanical — measured, then redesigned twice

The cabinet numbers from the 2026-08-26 site visit are still the governing
field record and still correct:

| Dimension | Value | Provenance |
|---|---|---|
| Cabinet overall | 71″ H × 24″ W × 34″ D | OEM 50-045R00, confirmed by tape |
| Cabinet box, less feet | 67-7/8″ | measured |
| Feet | 3-1/8″ | derived, reconciles exactly |
| Front opening, clear width | 18½–19¾″ | measured |
| Outer door | ≈ 24.3″ W × 68.2″ H | 3230 drawing + derived |
| Behind the doors | Louvered outer door on two pins, perforated zinc inner panel on a piano hinge, card cage and Concurrent PSU modules behind | photographed |

Rev 1 (box on the door hinges) and Rev 2 (pine box, ACM face plate, cut list,
build kit) were both finished and buildable. Rev 3 threw them away on
2026-09-03 because a cased touchscreen on an arm needs no enclosure at all,
and because a donated screen made the face-plate window moot. Everything under
`mechanical/` except `rev3-touch-concept.html`, `me1-findings.md`, the OEM and
3230 references and `photos/` is now provenance, not plan.

---

## 3. What is not done

### Mechanical Rev 3 — the critical path

Rev 3 is a drawn concept with a load argument (a 20 lb screen 15″ out is a
300 in-lb moment; captured at two points 40″ apart on the spine that is ~7.5 lb
at each padded contact, versus ~150 lb in a desk-clamp jaw). It has no parts.

Five gates, one closed:

| Gate | Question | Status |
|---|---|---|
| 1 | Does the monitor come back after a power cut, or wake into standby? | **Not tested.** Go/no-go for the exhibit |
| 2 | Does Linux see the touch, and does it rotate with the screen? | **Closed.** Both proven 2026-09-14 |
| 3 | Does the arm's collar fit 1¼″ EMT (1.510″ OD, poles run ~Ø38 mm)? | No arm bought, nothing calipered |
| 4 | How tall is the door opening? The conduit is cut to this | The ~48″ tape reading from the site visit has no note of what it spanned. **Needs a tape** |
| 5 | Will the museum expose the boards? | **Curatorial.** The alternative is polycarbonate in the aperture |

Then: parts list, spine and bracket drawings, `mounting.md`, a bench mock-up
that holds the load, and a fit check in the cabinet.

### Software — hardening, not features

- **Read-only root.** The OptiPlex has a writable disk and the exhibit will be
  power-cut nightly. The emulator writes to `os32.dsk`. Nothing has been done
  about either.
- **Golden image and re-image procedure** for the OptiPlex. Today the machine
  is the only copy of itself.
- **Network posture.** The websocket bridge listens on a port. In production
  the machine should be inbound-locked, SSH only.
- **Panel diagonal.** `build-kiosk.py` defaults to a 23.8″ panel. The T232HL
  is a 23″ panel. Re-run with `--panel 23` and re-read the legibility checks.
- **Watchdog for a full hang.** The loop restarts Chromium; nothing reboots a
  frozen machine.
- **Content data file.** Copy lives in Python. A non-developer cannot edit it.
- **Usage counts.** A museum-team ask. Needs a privacy decision first.
- **Attract loop.** If the still Home screen does not pull people in.
- **Reliability soak.** A week on the bench, unattended, before it goes near
  the cabinet. Not started.

### Decisions the museum team owns

- **Expose the card cage** (Gate 5). What makes the exhibit worth looking at is
  also what removes forty years of finger protection.
- **Accept the touchscreen accessibility trade-off.** Three physical buttons
  at 38″ were tactile, findable without sight, and ADA-compliant by
  construction. A touchscreen is none of those. Large targets mitigate. The
  team should accept this deliberately, not discover it. See the ADR in
  `02-architecture.md` §15.
- **Body type at 6 ft.** Bullets subtend 13.6 arcmin at 6 ft against a 16
  arcmin comfort line. Fine at arm's length, where you stand to touch. Cutting
  one bullet per screen buys ~29% more type. Content call, not engineering.

---

## 4. The two machines

| | Bench kiosk (exists) | Museum kiosk (target) |
|---|---|---|
| Where | On a bench, reachable over SSH | In front of the 3280 |
| Network | Wi-Fi on, for updates | Offline, inbound-locked |
| Disk | Writable Ubuntu install | Read-only overlay, `/data` for logs |
| Power | Plugged in | AC timer, BIOS restore-on-power |
| Mount | Desk stand | Conduit spine + arm, doors stored |
| Emulator | Running | Running, bridge on loopback only |

The whole of §3 is the right-hand column.

---

## 5. Repo map — what is current

| Path | State |
|---|---|
| `docs/00-project-brief.md` | Origin and content spec. Still the reason the project exists |
| `docs/01-prd.md`, `03-ux.md` | Written for Rev 1. Requirements and screen flow still hold; button and enclosure sections do not |
| `docs/02-architecture.md` | §1–14 describe the software runtime accurately. **§15 is the Rev 3 ADR — read it** |
| `docs/04-dev-plan.md` | The Rev 1 work breakdown the issues were cut from. Historical; the issue tracker is now authoritative |
| `src/kiosk-app/` | **Current.** `_deck.py` is the single source of truth |
| `src/controller/` | **Current.** Deployed on the OptiPlex |
| `src/emulator/` | **Current.** Deployed on the OptiPlex |
| `electronics/` | Written for the Pi and buttons. Superseded; its README says what survives |
| `mechanical/rev3-touch-concept.html` | **Current.** The Rev 3 concept page |
| `mechanical/me1-findings.md`, `photos/`, OEM and 3230 references | **Current.** Field record |
| Everything else under `mechanical/` | Rev 1 and Rev 2. Provenance only |

---

## 6. Traps

Things that already cost us time. Still true.

1. **The early AI concept renders were wrong about the machine.** They showed
   an open card cage that does not exist and drove real design decisions for
   days. Rev 3 shows the site photographs and says so.
2. **A measurement can be right and still mislead.** 67-7/8″ looked like it
   contradicted the OEM's 71″. One was the box, one included the feet. Always
   ask what was measured, not just the number. The ~48″ reading is the live
   example: nobody wrote down what it spanned, and Gate 4 waits on it.
3. **Rotating the picture does not rotate the touch.** Two devices, two
   settings. `rotate.sh` does both; do not do one by hand.
4. **A page that is perfect on a laptop reflows in the museum.** The kiosk has
   no network. `build-kiosk.py` refuses to emit an external reference, and
   `check-fit.py` measures real reflow. Run it after any copy change.
5. **Snap Chromium cannot read `/opt`.** On Ubuntu, the app comes up blank
   until you install the .deb. `install.sh` says so.

---

## 7. Issue tracker reconciliation — 2026-09-15

The 39 issues were cut from the Rev 1 dev plan on 2026-08-22. On 2026-09-15
they were reconciled with Rev 3:

- **Closed, done:** ME-1 measure (#26), SW-A2 deck encoded (#3), SW-B1
  fullscreen (#5), SW-B2 nav (#6), SW-B3 idle reset (#7), SW-D1 boot-to-kiosk
  (#12), EL-1 bench bring-up (#20, on the OptiPlex rather than a Pi).
- **Closed, obsolete under Rev 3:** everything about buttons, GPIO, uinput,
  the hinge, the door, the frame, the de-cased monitor, and USB content
  sticks: #8, #9, #10, #11, #14, #21, #22, #24, #28, #29, #30, #31, #32.
- **Re-scoped for Rev 3:** #1 (polycarbonate in the aperture, still
  deferred), #2 content data file, #4 deploy script, #13 read-only root, #15
  watchdog, #16 network posture, #17 golden image, #18–19 usage counts, #23
  power-cut recovery, #25 Rev 3 BOM, #27 conduit spine mount, #33 finish, #34
  drawings and `mounting.md`, #35–39 integration.
- **New:** #40 the three museum-team decisions in §3, #41 emulator
  hardening, #42 attract loop.

Milestone M2 Measure is closed. M3 Bring-up now means the OptiPlex.

---

## 8. Work available in parallel

- **Mechanical Rev 3**, all of it, blocked only on a tape measure and a
  monitor arm. Gate 4 first.
- **Software hardening** (#13, #15, #16, #17) needs the OptiPlex or a
  throwaway Ubuntu VM. No collision with content work.
- **Content** lives in `_deck.py` and is being actively edited. Coordinate
  before touching it. Always run `check-fit.py` afterwards.
- **The museum decisions** (#40) need a conversation with Doug Crawford, not code.

### Conventions that matter

- **Commit only files you changed.** `git add <paths>`, never `git add -A`
- Everything is labelled **concept** until built and installed
- No demo fallback: show error states, not demo data
- Authoritative knowledge base is the wiki at `~/Workspaces/wiki/`
  (`projects/concurrent-3280-museum/`); propose changes via wiki-ingest

---

## 9. Sources

- Concurrent, *3280 and Micro3200 Families Product Overview*, 50-045R00, Aug 1989 —
  [bitsavers](https://bitsavers.org/pdf/interdata/32bit/3280/50-045R00_3280_ProdOverview_1989.pdf)
- Perkin-Elmer, *Model 3230 Processor Installation and Maintenance Manual*,
  47-004 R21, 1982 —
  [bitsavers](https://bitsavers.org/pdf/interdata/32bit/3230/47-004R21_3230_Maint_1982.pdf)
- Datapro, *Concurrent Computer Corporation Supermini Systems*, M11-230-101, Feb 1986 —
  [bitsavers](http://bitsavers.org/pdf/datapro/datapro_reports_70s-90s/Concurrent/M11-230-10_8602_Concurrent_3200.pdf)
- OS/32 kit: [davygoat/simh-os32](https://github.com/davygoat/simh-os32) v1.2 on
  [open-simh](https://github.com/open-simh/simh)
- Site photographs, 2026-08-26 — `mechanical/photos/`
- Ken Yeager's letters, for the team and bring-up screens — cleared by Ruth Yeager

---

*Written 2026-09-15. The machine in the warehouse is the authority; where this
document and the machine disagree, the machine wins.*
