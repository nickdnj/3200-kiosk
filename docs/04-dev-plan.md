# 3280 Kiosk — Development Plan

> **Historical — the Rev 1 plan (2026-08-22).** This is the work breakdown
> the 39 GitHub issues were cut from. Rev 3 (2026-09-03) removed the buttons,
> the GPIO controller, the Pi image, the hinge and the enclosure; the issues
> were closed or re-scoped accordingly on 2026-09-15. **The issue tracker is
> authoritative now, not this document.** What still holds: the milestone
> names, the integration track, and the software hardening stories (read-only
> root, watchdog, golden image, usage logging). See `05-status-report.md` §7.

**Reads with:** `01-prd.md`, `02-architecture.md`, `03-ux.md`. Each story cites the
PRD/architecture IDs it satisfies.

---

## 1. Tracks & milestones

Four tracks run largely in parallel; integration pulls them together.

- **SW — Software** (kiosk app + Pi controller + OS provisioning)
- **EL — Electronics** (Pi, monitor, buttons, power) — builder's high-confidence domain
- **ME — Mechanical** (frame, hinged enclosed door, mounting) — **highest risk / critical path**
- **IN — Integration** (install, soak test, handoff)

**Milestones** (PRD §14):

| M | Milestone | Gate / definition of done | Tracks |
|---|---|---|---|
| **M1** | Content lock | App runs fullscreen on a plain monitor, button/key driven, content-complete, idle-reset + local counts working | SW |
| **M2** | Machine measured | Real cabinet/opening dimensions captured; panel size + mount method confirmed | ME |
| **M3** | Electronics bring-up | Pi + monitor + buttons on the bench; boots to kiosk, watchdog, power-safe, buttons drive the app | EL, SW |
| **M4** | Mechanical build | Fixed frame + enclosed hinged door built, finished, bench-fitted | ME, EL |
| **M5** | Integration & install | Installed in the 3280, soak-tested, docent-ready, VCF sign-off | IN |

**Sequencing.** M1 (software) and M2 (measure) run **in parallel from day one** —
software is off the critical path. **M2 gates M4** (can't build the door without
dimensions + confirmed panel). M3 needs the Pi in hand (have it) and can overlap
M4; **M4's door build (ME-3) needs the confirmed panel (M2) and the electronics
package (M3).** Then M5.

```
day 0 ─┬─ M1 Content lock (SW) ───────────────┐
       └─ M2 Measure (ME) ─┬─ M3 Bring-up (EL+SW) ─┐
                           └─ M4 Mechanical build ─┴─ M5 Install & soak ─▶ done
   Critical path:  M2 ─▶ M4 ─▶ M5   (measure → door → install)
```

---

## 2. SOFTWARE track (SW)

### Epic SW-A — Content restructure & build
| ID | Story | Acceptance | Trace |
|---|---|---|---|
| SW-A1 | Split screen deck/copy into a `content.{js,json}` data file consumed by `build-app.py` | Editing a bullet/headline requires touching only the data file; `build-app.py` still emits one `index.html` | A5.1, FR6 |
| SW-A2 | Encode the 8-screen deck (UX §4) in the data file with per-screen graphic + bullets + optional `more` slot | All 8 screens render from data; matches Rick-approved content | UX §4, CR1–CR6 |
| SW-A3 | Deploy step: build output written to the USB content layout (label `KIOSK`) | A `make deploy` / script produces the USB tree; runs read-only in operation | A2.5, A5.1 |

### Epic SW-B — Kiosk runtime & interaction
| ID | Story | Acceptance | Trace |
|---|---|---|---|
| SW-B1 | Fullscreen, no OS/browser chrome; remove review-app tap-to-enlarge | No cursor, scrollbars, gestures, context menu; screen is full-size | FR1, FR2, A5.4 |
| SW-B2 | `KIOSK` JS nav interface: `next/back/home/more` from key events; boundary dim/inert | Keys drive nav; ends dim + inert, no dead presses | FR2, UX §1 |
| SW-B3 | Idle → Home reset (~75 s, configurable) with attract pulse on Home | After timeout returns to Home; any key resets timer | FR3, UX §6 |
| SW-B4 | "More detail" scaffolding: content slots + reserved key mapping, **inert in v1** | `more()` and hint exist but are disabled; enabling later is data + one mapping | FR5, UX §5 |

### Epic SW-C — Controller (Pi)
| ID | Story | Acceptance | Trace |
|---|---|---|---|
| SW-C1 | GPIO service reads 3 buttons, debounced (~30–50 ms), `Restart=always` | Presses register once, no bounce; service auto-restarts | FR9, ER2, A4.1 |
| SW-C2 | Map buttons → synthetic keys via `uinput` (Back→←, Home→Home, Next→→) | Physical presses navigate the app under Wayland/X11 | A4.2, FR2 |
| SW-C3 | Provision spare button(s) in service + wiring map, unmapped in v1 | Adding a button later = config only, no rewrite | ER3, A4.3 |

### Epic SW-D — OS image & provisioning
| ID | Story | Acceptance | Trace |
|---|---|---|---|
| SW-D1 | Raspberry Pi OS Lite image; boot-to-kiosk (autologin → compositor → server → Chromium) | Cold boot reaches Home with nothing else visible | FR8, A3 |
| SW-D2 | Overlay read-only root + boot RO; journaled ext4 `/data` logs partition | Survives abrupt power-off with no corruption | FR11, NFR2, A2.3, A2.6 |
| SW-D3 | USB content mount-by-label (RO) + "content drive not found" fallback screen | Any `KIOSK`-labeled stick mounts at the fixed point; missing stick shows the error screen | A2.5, A2.7 |
| SW-D4 | Watchdog: systemd `Restart=always` for server + browser; HW watchdog reboot on hang | Killing Chromium returns to Home; full hang reboots | FR10, NFR1, A3.4 |
| SW-D5 | Dev/prod Wi-Fi toggle (dev: SSH/rsync; prod: offline) documented + scripted | One flag flips network on/off; prod image is offline | A2.8 |
| SW-D6 | Golden SD image + documented re-image procedure | Spare card boots identically; procedure written | NFR4, A2.4 |

### Epic SW-E — Usage logging
| ID | Story | Acceptance | Trace |
|---|---|---|---|
| SW-E1 | Append-only button-event log to `/data/usage/` (fsync, power-safe) | Presses logged with timestamps; truncated tail tolerated | FR4, A6.1, P1 |
| SW-E2 | Summary script → counts/sessions; review over dev Wi-Fi or card | Produces per-button counts + idle-gap sessions | A6.3, P2 |

---

## 3. ELECTRONICS track (EL) — builder's domain, specified lightly

| ID | Story | Acceptance | Trace |
|---|---|---|---|
| EL-1 | Bench bring-up: Pi 4 (from drawer) + salvaged monitor over HDMI, powered | Pi drives the panel at native portrait res | ER1, A2.1 |
| EL-2 | Wire 3 buttons to GPIO (pull-ups/debounce) + provision spare lines | 3 buttons read cleanly; spare lines terminated/labeled | ER2, ER3 |
| EL-3 | Power: PSU in fixed cabinet, USB-C 5 V across the hinge (service loop) | Door powered by one low-voltage line; loop rated for travel | A7.2, MR10 |
| EL-4 | AC scheduling (salvaged timer/relay or exhibit switch) for museum hours | Powers on during hours; abrupt off is safe (SW-D2) | ER4, A7.1, NFR2 |
| EL-5 | De-case the salvaged monitor to bare panel + controller board | Panel + board mount flat/shallow for the low-profile door | A8.4, MR12, MR19 |
| EL-6 | BOM (salvage-first) + wiring/pinout + assembly/test notes under `electronics/` | `bom.md` + wiring diagram + test note committed | ER6, §9 |

---

## 4. MECHANICAL track (ME) — critical path

| ID | Story | Acceptance | Trace |
|---|---|---|---|
| **ME-1** | **Measure the real machine** — cabinet, front opening, rack rails, mount points; datum drawing | Dimensioned sketch committed; confirms panel size (24″ vs 27″) + mount method | MR1, PRD Q1/Q2 |
| ME-2 | Reversible mounting method (clamp rails / existing holes / straddle) — no drilling | Mock-up holds load; removal leaves cabinet as-found; documented in `mounting.md` | MR2, A8.1 |
| ME-3 | Fixed front frame (tan) spanning the opening, sized to preserve viewing area | Frame mounts per ME-2; door opening located upper-middle | MR3, A8.1 |
| ME-4 | Enclosed hinged door: bezel + badge + de-cased panel + **vented low-profile rear shroud** (Pi inside) | Door encloses panel/Pi/button-backs; minimal depth; shroud vented + service-removable | MR5,8,12,13,14,18,19 |
| ME-5 | Hinge + hold-open (stay/detent) + closed catch + hard over-travel stop | Left-hinge; self-holds open; won't drift closed; stop protects boards | MR5,6,7, A8.3 |
| ME-6 | Cable service loop across the hinge (power only) | USB-C loop survives full travel; no pinch/tension at extremes | MR10, A7.2 |
| ME-7 | Button plate on the door, labeled, at ADA-reachable height (fallback: low plate) | Buttons meet reach range or fallback plate specced | MR11, A1, A8.5 |
| ME-8 | Finish: tan color-match to the machine (fallback clean modern) | Door/frame finished; reads as belonging to the piece | MR13 |
| ME-9 | CAD + drawings + `mounting.md` committed to `mechanical/` | Source + STEP + drawings; reproducible build | MR17 |
| ME-10 | **(Deferred)** Plexiglass board-protection panel behind the opening | Later add-on; not in initial build | MR4, PRD §11 |

---

## 5. INTEGRATION track (IN)

| ID | Story | Acceptance | Trace |
|---|---|---|---|
| IN-1 | Assemble subsystems into the 3280; fit check | Door swings/holds; screen + buttons work in place; reversible mount verified | §14 phase 5 |
| IN-2 | Reliability soak: power-cycle, crash-recovery, full unattended day | Recovers from crashes/power cuts; runs a day untouched | NFR1, NFR2 |
| IN-3 | Content-swap runbook + log-collection runbook + re-image doc | A non-author can update content and pull logs from the docs | NFR4, A6.3 |
| IN-4 | Docent walkthrough + handoff (ownership transfer to museum) | Docents operate it; ownership transferred | PRD §4, "transfer ownership" |
| IN-5 | Safety + reversibility sign-off with VCF | No pinch/tip/sharp hazards; mount reversible; exposed-board plan accepted | MR2, MR7, MR15, §11 |

---

## 6. GitHub setup (proposed)

- **Milestones:** `M1 Content lock`, `M2 Measure`, `M3 Bring-up`, `M4 Mechanical`,
  `M5 Install`.
- **Labels:** `track:software` `track:electronics` `track:mechanical`
  `track:integration`; `type:epic` `type:story`; `priority:critical-path`
  `deferred`.
- **Issues:** one per story above (≈31), grouped under epics, assigned to a
  milestone, labeled by track. Critical-path (ME-1, ME-4, ME-5, IN-1) flagged.
- **Board (optional):** columns Backlog → Ready → In progress → Done.

**Created 2026-08-22** — all 39 story issues, 5 milestones and the track labels are
live at [nickdnj/3280-kiosk/issues](https://github.com/nickdnj/3280-kiosk/issues).

---

## 7. Risks & critical path

| Risk | Impact | Mitigation |
|---|---|---|
| Measurements wrong / cabinet differs from renders | Door/frame won't fit | **ME-1 first**; build nothing mechanical until measured |
| Salvaged monitor odd size/depth | Door design churn | Confirm panel in ME-1/EL-5 before ME-4; 24″ target keeps margin |
| De-casing a salvaged monitor damages it | Lose the panel | Test panel powered before committing; keep a backup panel candidate |
| Reversible mount can't grab the cabinet cleanly | Mounting redesign | ME-2 mock-up early; multiple candidate methods |
| Hinge load/hold-open with door weight | Sag / won't stay open | Keep door light (24″, de-cased); size hinge + stay in ME-5 |
| Exposed boards touched by visitors | Artifact wear | Signage/docent interim; plexiglass later (ME-10) |

**Critical path:** ME-1 → ME-4 → ME-5 → IN-1 → IN-2. Software (SW) and most
electronics can proceed alongside and are low-risk.

---

## 8. First actions

1. **ME-1 — measure the machine.** Unblocks the whole mechanical critical path and
   confirms panel size + mount method. *Do this first.*
2. **SW-A1/A2 — content data file + deck.** Off critical path, safe to start now;
   turns the concept app into the maintainable v1 base.
3. **EL-1 — bench bring-up** on the drawer Pi 4, in parallel.

**In flight:** ME-1 field materials are published ahead of the site visit —
[`mechanical/dimensions-assumed.md`](../mechanical/dimensions-assumed.md),
[`mechanical/measurement-checklist.md`](../mechanical/measurement-checklist.md),
[`mechanical/drawings/`](../mechanical/drawings/), and the warehouse shopping list
at [`electronics/salvage-recon.md`](../electronics/salvage-recon.md).

---

*This completes the PRD → Architecture → UX → Dev-plan flow. From here it's
execution: measure, build, integrate.*
