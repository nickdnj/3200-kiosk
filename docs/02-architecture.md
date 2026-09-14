# 3280 Kiosk — Architecture

> **SUPERSEDED IN PART BY REV 3 — see §15 at the bottom before trusting any
> hardware decision on this page.** Rev 3 removed the doors, moved the UI to a
> touchscreen, and replaced the Raspberry Pi with a donated x86 mini PC.
> Sections 1–14 still describe the *software* runtime accurately; the compute
> platform, the button path, the hinge, and the de-cased monitor do not exist
> any more.

> **Status: CONCEPT / v1 architecture.** The technical approach we're building
> toward. Decisions here are recommendations with rationale and alternatives, not
> frozen specs — revise as the machine is measured and parts are salvaged.

**Reads with:** `01-prd.md` (requirements). Every decision below cites the PRD
IDs it satisfies (FR = software, ER = electronics, MR = mechanical, NFR =
reliability, A = accessibility, P = privacy).

**Guiding constraints (from the PRD):** offline/standalone, silent, no
touchscreen, three (+ spare) buttons, unattended & power-cycle-safe, museum
artifact (reversible mounting), and **salvage-first** — most parts come out of
the VCF warehouse, so favor adaptable, standards-based choices over any specific
new SKU.

---

## 1. System overview

The kiosk is one self-contained appliance built into the 3280's front. Six
subsystems:

```
                    ┌─────────────────────────── THE HINGED DOOR (enclosed, MR18) ───────────┐
   AC mains          │                                                                        │
 (fixed cabinet)     │   ┌──────────┐    HDMI     ┌──────────────┐                            │
     │               │   │ Monitor  │◄────────────│              │                            │
  ┌──┴───┐  USB-C 5V │   │ (salvaged│             │ Raspberry Pi │  reads GPIO   ┌──────────┐ │
  │ PSU  │───────────┼──►│ de-cased)│             │  (in shroud) │◄──────────────│ Buttons  │ │
  │(fixed)│  across  │   └──────────┘             │              │   (on door)   │ B/H/N +sp│ │
  └──────┘  hinge    │        ▲                   └──────┬───────┘               └──────────┘ │
   (MR10)            │        │ fullscreen               │                                    │
                     │        │ Chromium kiosk    reads │        │ writes logs               │
                     │   ┌────┴─────────┐    ┌─────────▼──────┐ ┌───▼──────────────┐          │
                     │   │  Kiosk App   │◄───│ USB (KIOSK):   │ │ SD /data (ext4): │          │
                     │   │ (local HTTP) │    │ content, RO    │ │ usage logs, RW   │          │
                     │   └──────────────┘    └────────────────┘ └──────────────────┘          │
                     └───────────────────────────────────────────────────────────────────────┘
   SD = read-only overlay core (OS/Chromium/controller, stable) + small RW /data partition (logs)
   USB = content, mounted read-only, swappable · Compute + input + display all ride the door
```

- **Display** — a salvaged monitor, de-cased to a bare panel for low profile (MR19).
- **Compute** — Raspberry Pi 4, mounted inside the door's rear shroud (MR18).
- **Storage** — stable core + a small writable `/data` logs partition on the SD
  card; content on a **swappable, read-only USB drive** (A2.5–A2.6).
- **Input** — three active buttons (+ wired spares) on GPIO (ER1–ER3).
- **Power** — PSU in the fixed cabinet; low-voltage across the hinge (MR10).
- **Software** — a locked-down Chromium kiosk showing the local app; a GPIO
  service turns button presses into app navigation.
- **Enclosure** — fixed front frame + enclosed hinged door, reversibly mounted.

Everything electronic rides the door, so **only power crosses the hinge.**

---

## 2. Compute & operating system

- **A2.1 — Raspberry Pi 4 (on hand).** The build targets a **Pi 4 already in the
  drawer** — has the **USB-A ports** the content drive needs (A2.5). 2 GB+ is
  ample for a static local site. A Pi 5 would work; a Pi 3B+ is the floor. *(ER1)*
- **A2.2 — Raspberry Pi OS (64-bit, Bookworm), Lite base.** Minimal image; add
  only the compositor + browser we need. No desktop, no extra services.
- **A2.3 — Power-safe core filesystem.** The SD card holds the **stable core** —
  OS, Chromium, the controller — run as **read-only root via overlayfs**
  (`raspi-config` → Overlay FS) with the boot partition read-only. This is what
  makes the daily power cut and abrupt outages non-destructive. **The core is
  designed not to change**; content does not live here. *(FR11, NFR2)*
- **A2.4 — Keep a golden SD image.** Because the core is stable, one golden image
  is the fastest field recovery — keep a spare card flashed and documented; content
  is separate (A2.5), so re-imaging never touches it. *(NFR4)*

### Storage model — stable core + logs on SD, content on USB
- **A2.5 — Content lives on a removable USB drive, read-only at runtime.** The
  kiosk-app build (and its data file, A5.1) is deployed to a **USB flash drive**
  mounted **by filesystem LABEL** (e.g. `KIOSK`) at a fixed point (e.g.
  `/media/kiosk`) so any correctly-labeled stick lands deterministically.
  **Mounted read-only in operation** — content only changes offline, when the stick
  is swapped/edited — which all but eliminates USB wear and power-cut corruption.
  Updating content = edit/swap the stick; never re-image the SD. *(FR6, NFR4)*
- **A2.6 — Usage logs on a small writable SD partition (chosen: option B).** A
  dedicated **journaled ext4 partition mounted at `/data`**, separate from the
  overlay root, holds the append-only usage logs. Journaling + append + `fsync`
  keeps it power-cut-safe, and it keeps continuous small writes **off** the
  content USB (which stays read-only). *(FR4, FR11, NFR2)*
- **A2.7 — Graceful "no content" state.** If the USB drive is **missing or
  unreadable** at boot, the kiosk shows a clear **"content drive not found"** screen
  (served from a tiny fallback baked into the core), not a blank screen or a crash —
  no demo fallback. *(FR1, PRD "no demo fallback")*
- **A2.8 — Wi-Fi is a development convenience, off in production.** During bring-up
  and bench work, **enable Wi-Fi** for easy updates (SSH/`scp`/`rsync`, `git pull`,
  log collection) — far quicker than pulling cards or sticks. It is **not** part of
  the exhibit's operation: the installed kiosk runs **offline** (PRD constraint),
  and the app never depends on the network. Make it a **toggle** (a documented
  `raspi-config`/`nmcli` step or a `dev`-vs-`prod` flag in provisioning) so the
  same image ships either way. If Wi-Fi is left on for maintenance convenience on
  the floor, it must stay **inbound-locked** (SSH only, no listening services, no
  cloud) and is a maintenance path only — see §11. *(dev tooling; preserves PRD
  offline/standalone)*

---

## 3. Kiosk runtime (how the app gets on screen)

- **A3.1 — Chromium in kiosk mode.** Proven, matches how the app already renders.
  Launch fullscreen with crash/UI suppression:
  `chromium-browser --kiosk --incognito --noerrdialogs --disable-infobars
  --disable-session-crashed-bubble --check-for-update-interval=31536000
  --app=http://localhost:8080/`. *(FR1, FR2)*
- **A3.2 — Serve the app over loopback, not `file://`.** A tiny static HTTP
  server (systemd unit, Python `http.server` or `busybox httpd`) serves the
  **content from the USB mount** (A2.5, e.g. `/media/kiosk`) at
  `http://localhost:8080`; if the mount is absent it serves the core fallback
  (A2.7). A real origin makes `localStorage`/`fetch` behave and avoids `file://`
  quirks; loopback-only keeps it offline. *(FR1)*
- **A3.3 — No idle chrome.** Disable screen blanking/DPMS and hide the cursor
  (compositor config; `unclutter`/`--kiosk` and `wlr`/`xset` equivalents). No
  scrollbars, gestures, or context menu (also enforced in-app, FR2).
- **A3.4 — Watchdog / auto-restart.** Both the HTTP server and Chromium run as
  **systemd services with `Restart=always`**; enable the **Pi hardware watchdog**
  to reboot on a full hang. Result: any crash returns to Home unattended.
  *(FR8, FR10, NFR1)*
- **A3.5 — Boot straight to kiosk.** Autologin to a minimal session that starts
  the compositor → server → browser; nothing else visible at any point. *(FR8)*

> **Display-server note:** synthetic input (below) is injected at the kernel
> (evdev/uinput) layer, so A3 works the same whether the session is Wayland
> (Bookworm default) or X11. We are not blocked by that choice.

---

## 4. Buttons → app transport

The decision that ties electronics to software.

- **A4.1 — GPIO service (`src/controller/`).** A small Python service
  (`gpiozero`/`lgpio`) reads the buttons, **debounces** (~30–50 ms), and emits
  events. Runs as a `Restart=always` systemd service. *(FR9, ER2)*
- **A4.2 — Deliver as synthetic key events (chosen).** The service maps buttons
  to the **keys the app already listens for** and injects them via **`uinput`**:
  `BACK → ArrowLeft`, `HOME → Home`, `NEXT → ArrowRight` (spare/`MORE →` a
  reserved key, inert in v1). *(FR2, FR5)*
  - *Why:* dead simple, no app↔service protocol, survives app reloads, reuses the
    existing keyboard handler, and works under both Wayland and X11.
  - *Alternative (deferred):* a loopback **WebSocket** for richer two-way signaling
    (e.g., service-driven attract, per-event acks). Adopt only if we outgrow keys.
- **A4.3 — Spare buttons.** The service and wiring support additional buttons with
  no rewrite; **three active in v1**, spares wired but unmapped (MORE reserved for
  the later deep-dive). *(ER3, FR5, MR11)*

---

## 5. Application architecture (`src/kiosk-app/`)

- **A5.1 — Keep the single-file build; split out content.** `build-app.py` still
  emits one `index.html` (keeps parity with the shareable concept artifact), but
  **move the screen deck/copy into a separate content file** (`content.js` or
  `content.json`) that the builder consumes. Content edits stop touching layout
  code — satisfies "edit + rebuild" while improving maintainability. *(FR6, CR1–CR6)*
  The build output is **deployed to the USB content drive** (A2.5), not baked into
  the SD image — so a content refresh never rebuilds the core.
- **A5.2 — Runtime `KIOSK` interface.** A small JS module exposing `next()`,
  `back()`, `home()`, `more()` (inert v1), driven by the injected keys. Single
  source of truth for navigation. *(FR2)*
- **A5.3 — Idle → Home.** An in-app timer returns to Home after a configurable
  idle timeout; any key/button resets it. Config lives with content. *(FR3)*
- **A5.4 — On-device screen size independence.** Layout targets the installed
  portrait panel; **remove the review-app tap-to-enlarge** (physical screen is
  already full size). *(§5 of PRD)*
- **A5.5 — Concept marker** stays until installed (CR6).

---

## 6. Usage counts (local, offline, anonymous)

- **A6.1 — The GPIO service owns the log, written to the SD `/data` partition.**
  Every button event is appended (with a monotonic timestamp) to `/data/usage/`
  on the dedicated writable partition (A2.6) — kept off the read-only content USB.
  Append-only, line-based, `fsync`'d, and tolerant of a truncated last line from a
  power-cut. Button counts ≈ screen transitions; sessions by idle-gap. *(FR4, P1)*
- **A6.2 — Optional per-screen views.** If we want true per-screen counts, the app
  POSTs `screen_view` to a **loopback-only** endpoint the service exposes; still
  offline, still anonymous. Enhancement, not v1-blocking. *(FR4, P1)*
- **A6.3 — Review path.** A small summary script turns the logs into counts; the
  maintainer copies `/data/usage/` off during a service visit — over the
  development Wi-Fi (A2.8) if enabled, else by reading the card. Content is
  refreshed separately by swapping the USB. No cloud, no personal data, no cameras.
  *(P1, P2)*

---

## 7. Power & lifecycle

- **A7.1 — AC timer energizes the exhibit during museum hours (chosen).** A
  salvaged AC timer/relay (or the museum's exhibit switch) powers the outlet on a
  schedule; the Pi boots on power. Abrupt power-off at close is safe because of the
  overlay FS (A2.3). *(NFR2, FR11)*
  - *Nicety:* a cron `shutdown` a minute before the scheduled cut for a graceful
    stop — optional, since overlay FS already covers hard cuts.
  - *Alternative:* Pi always powered, panel sleeps/wakes on schedule (DPMS/CEC).
    More moving parts; only worth it if power cycling proves troublesome.
- **A7.2 — PSU in the fixed cabinet; low-voltage across the hinge.** Put the mains
  PSU in the stationary cabinet and run **USB-C / 5 V DC across the hinge** to the
  door — thinner, safer, and more flex-durable than mains at the hinge. A single
  conductor on a service loop. *(MR10, MR18)*

---

## 8. Mechanical architecture (approach-level; detail in `mechanical/`)

Realizes MR2–MR19; exact geometry waits on measuring the machine (MR1).

- **A8.1 — Fixed front frame, reversibly mounted.** A tan frame spans the front
  opening; the smaller kiosk door lives in it (MR3). **Mount candidates (confirm on
  measure, salvage the hardware):** clamp to the **19″ rack rails**, reuse existing
  **door-hinge / fastener points**, or **straddle brackets** on the cabinet frame
  lip — all **no-drill, reversible** (MR2).
- **A8.2 — Enclosed hinged door.** Left hinge (MR5); door = tan front bezel +
  black screen bezel + CONCURRENT badge (MR13), the **de-cased salvaged panel**
  (MR12), the button plate below it (MR11), and a **vented low-profile rear shroud**
  enclosing the panel, Pi, and button backs (MR18–19, MR14).
- **A8.3 — Hold-open + stop.** Friction/detent hinge or a stay to self-hold open
  (MR6); hard **over-travel stop** protects the boards (MR7); friction/magnetic
  catch holds it closed (MR6).
- **A8.4 — Go low-profile by de-casing the salvaged monitor.** Mount the bare LCD
  panel + its controller board directly in the door instead of the consumer
  housing; this is the biggest lever on depth (MR19) and pairs with salvage-first.
- **A8.5 — Buttons.** Salvaged momentary/arcade buttons on the door plate, labeled
  to match the screen, with blanks for spares; height resolved against ADA reach
  (A1) — separate low plate is the fallback if the door position can't satisfy reach.
- **A8.6 — Board protection is deferred.** A **plexiglass panel behind the opening**
  is a later, low-cost add-on (PRD §11); the initial build ships with open framing +
  signage/docent guidance.

---

## 9. Bill-of-materials strategy (salvage-first)

| Subsystem | Salvage from warehouse | Buy new only if needed |
|---|---|---|
| Monitor / LCD panel | ✅ primary plan (de-case it) | a shallow panel if none salvageable |
| Compute (Pi) | ✅ if available | a Pi 4 otherwise (cheap) |
| Buttons | ✅ arcade/industrial momentary | 3–5 momentary buttons |
| Mounting (rack ears, brackets, fasteners) | ✅ preferred | brackets/clamps as needed |
| Panel/sheet stock for frame + door | ✅ preferred | sheet + tan paint |
| Hinge + stay/catch | possibly | hinge + gas-stay/detent |
| PSU + USB-C cabling | possibly | small PSU + USB-C |
| SD cards (primary + golden spare) | — | buy new (reliability) |
| Plexiglass (deferred) | — | later |

Rule: adaptable, standards-based parts so a salvaged substitute drops in.

---

## 10. Failure modes & recovery

| Failure | Mitigation | PRD |
|---|---|---|
| App/browser crash | systemd `Restart=always` → back to Home | FR10, NFR1 |
| Full system hang | Pi hardware watchdog reboots | NFR1 |
| Power cut at close / outage | overlay read-only root; logs on separate partition | FR11, NFR2 |
| SD corruption/wear | read-only root; golden spare image; logs isolated | NFR4 |
| Button stuck/spam | debounce + rate-limit in the GPIO service | FR9, NFR3 |
| Input can't reach OS | kiosk browser always focused; no OS chrome exposed | FR2, NFR3 |
| Door forced/over-swung | hard stop + hold-open; catch resists drift | MR6, MR7 |

---

## 11. Security & privacy

- **Offline in production** — the app serves only over loopback; no cloud, no
  remote management, no dependence on the network. **Wi-Fi is a development/
  maintenance convenience (A2.8), off for exhibit operation.** If left on for
  maintenance, keep it inbound-locked (SSH only, no listening services). *(PRD non-goals)*
- **No personal data, no cameras.** Only anonymous local counts (§6). *(P1)*
- **Physical:** enclosed door (MR18) means no exposed wiring/electronics to a
  visitor's hand; reversible mount protects the artifact (MR2).

---

## 12. Repo mapping

```
src/kiosk-app/     app + build-app.py + content.{js,json}; build output is
                   deployed to the USB drive, not the SD image (A5, A2.5)
src/controller/    GPIO service, uinput mapping, systemd units, provisioning
                   scripts (overlay-FS core, /data logs partition, USB
                   mount-by-label, autostart, watchdog, content-drive fallback,
                   dev/prod Wi-Fi toggle) (A2,A3,A4,A6,A7)
electronics/       BOM, button wiring/pinout, PSU + hinge cabling notes (§9, A7)
mechanical/        CAD/drawings for frame, door, shroud, mount; mounting.md (§8)
docs/              this doc, PRD, and downstream UX/dev-plan
```

---

## 13. Decisions (confirmed 2026-08-22)

All six branch points accepted as recommended:

1. ✅ **Chromium kiosk + loopback static server** as the runtime stack (A3).
2. ✅ **Synthetic keys via `uinput`** for buttons (A4.2); WebSocket deferred.
3. ✅ **Overlay read-only root + `/data` partition** for power-safety (A2.3).
4. ✅ **De-case the salvaged monitor** for low profile (A8.4).
5. ✅ **Low-voltage (USB-C 5 V) across the hinge**, PSU in the fixed cabinet (A7.2).
6. ✅ **Split content into a data file** now (A5.1).

---

## 14. Traceability (PRD → architecture)

- **FR1–FR3, FR6, FR7** → §3, §5 · **FR4** → §6 · **FR5** → §4.3, §5.2 ·
  **FR8–FR11** → §2, §3.4, §4.1, §10
- **ER1–ER5** → §2, §4, §7, §9 · **CR1–CR6** → §5
- **MR1–MR19** → §8 (and §7.2 for MR10, §2/§8 for reversibility)
- **NFR1–NFR4** → §3.4, §2.3, §10 · **A1–A4** → §8.5 · **P1–P2** → §6, §11

---

*Next in the flow: UX (`docs/03-ux.md`) — the screen deck, the button interaction
model, idle/attract behavior, and the "More detail" path on a spare button. Say
"let's do the UX" when ready.*

---

## 15. ADR — Rev 3 platform change (2026-09-13)

**Context.** Doug donated a 24" touchscreen and a mini PC. That removed the two
purchases blocking Rev 3, and simultaneously invalidated four decisions above.

**What changed, and what it costs**

| §  | Was | Now | Why |
|----|-----|-----|-----|
| A2.1 | Raspberry Pi 4 (ARM) | donated x86 mini PC | it exists, it is free, and it is faster than the job needs. Specifics unknown until bring-up — see `src/controller/BRINGUP.md` §0. |
| A2.2 | Raspberry Pi OS Lite | Debian/Ubuntu + X11, no desktop | X11 on purpose: portrait rotation plus touch remapping is one `xrandr` call and one `xinput` matrix. On Wayland it is compositor-specific and moves between releases. An exhibit that must self-recover after a power cut is the wrong place to be clever. |
| A3.2 | Chromium + loopback static server | Chromium on `file://` | the app is one self-contained file — no `fetch`, no modules, no external reference (`build-kiosk.py` asserts this). A server would be one more thing to die unattended at no benefit. |
| A4.2 | GPIO buttons → `uinput` synthetic keys | on-screen touch targets | no buttons, no GPIO, no `uinput`, no controller daemon. The largest simplification in the project: an entire electronics subsystem deleted. |
| A8.4 | de-case the salvaged monitor | cased monitor on an arm | there is no face plate to sit behind any more. |

**What did not change, and this is the point.** The app still speaks exactly
three commands. `build-kiosk.py` emits a page that answers touch, arrow keys
and `Home` identically, because the deck never knew what was driving it. If
touch disappoints on the floor, three switches can come back without a content
change.

**Consequences accepted**

- **Accessibility regressed and we are choosing it.** Three physical buttons at
  38" with a light press were tactile, findable without sight, and compliant by
  construction (ADA §309.4, §308). A touchscreen is none of those. Large
  targets mitigate; they do not erase. Rick should accept this deliberately,
  not discover it.
- **ADA reach stops being a property of the design.** The arm is adjustable, so
  compliance becomes a property of where somebody last left the screen. Set the
  height once, lock it, and treat articulation as a *service* feature.
- **Type got smaller.** Measured, not guessed: the deck was laid out for a
  230:529 box; a real panel in portrait is 9:16, and the touch bar takes 8.9%
  more. Body bullets land at 13.6 arcmin at 6 ft against a 16 arcmin comfort
  threshold — fine at arm's length (33 arcmin), short of Rick's "3–6 ft" bar at
  the far end. The headline still carries at 6 ft (19 arcmin). Cutting one
  bullet per screen would buy ~29% more type. That is a content decision.
- **Read-only overlay root (A2.3) still stands** and matters more, not less: an
  exhibit that power-cycles nightly will eventually corrupt a writable eMMC.

**Open, and blocking nothing yet:** Gates 1–5 in `BRINGUP.md`.
