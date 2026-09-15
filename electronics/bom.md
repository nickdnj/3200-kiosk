# Bill of Materials — v0 (pre-recon)

> **Superseded 2026-09-15.** Written for the Raspberry Pi and three-button
> design. Rev 3 runs on a donated Dell OptiPlex 9020M and Acer T232HL
> touchscreen with no buttons, no GPIO and no hinge. The Rev 3 BOM is issue
> #25; until it lands, only the power-strip and cable lines below still apply.

> **Status: CONCEPT / v0.** Salvage-first per
> [architecture §9](../docs/02-architecture.md). Quantities and sizes assume the
> 24″ panel baseline in
> [`../mechanical/dimensions-assumed.md`](../mechanical/dimensions-assumed.md) —
> both change if the measured opening or the salvaged panel differ. Prices are
> rough placeholders for the buy-new fallback; budget is not a constraint (PRD §15).

**Status key:** ✅ Have · 🔍 Salvage target · 🛒 Buy new · ⏸ Deferred

---

## Compute & storage

| Item | Qty | Status | Spec / note |
|---|---|---|---|
| Raspberry Pi 4 | 1 | ✅ Have | From the drawer. Mounts inside the door shroud (MR18) |
| Pi 4 PSU (USB-C 5 V 3 A) | 1 | 🔍 → 🛒 | Or the exhibit's own 5 V supply (see Power) |
| microSD card, primary | 1 | 🛒 Buy | 32 GB A2 endurance. **Do not salvage** (NFR4) |
| microSD card, golden spare | 1 | 🛒 Buy | Identical to primary; SW-D6 |
| Micro-HDMI → HDMI cable | 1 | 🔍 → 🛒 | Short, 1–2 ft; Pi 4 uses micro-HDMI |
| Heatsink / passive cooling | 1 | 🔍 → 🛒 | Enclosed vented shroud — passive preferred (MR14) |

## Display

| Item | Qty | Status | Spec / note |
|---|---|---|---|
| LCD panel, ~24″ 16:9 | 1 | 🔍 **Salvage — priority 1** | De-cased to bare panel + controller board (EL-5, A8.4) |
| LCD panel, backup | 1 | 🔍 Salvage | De-casing is one-way; a spare de-risks it |
| Panel controller board | 1 | — | Comes with the panel; relocate on standoffs |
| Panel power supply | 1 | 🔍 → 🛒 | Whatever the salvaged panel's board wants |

See [`salvage-recon.md`](salvage-recon.md) §1 for acceptance criteria and the
powered test to run **before** committing to a panel.

## Buttons & input

| Item | Qty | Status | Spec / note |
|---|---|---|---|
| Momentary pushbutton, 30 mm arcade | 5 | 🔍 → 🛒 | 3 mapped (BACK/HOME/NEXT) + 2 spare (ER3). All identical |
| Button harness wire | — | 🔍 → 🛒 | 22 AWG stranded, 5 colours + common |
| Crimp terminals (0.187″ spade) | 12 | 🛒 Buy | Standard arcade microswitch terminals |
| GPIO ribbon / connector | 1 | 🔍 → 🛒 | Pi header → button harness |

> 24 mm bodies (~1.1″ deep) instead of 30 mm (~1.4″) if the measured C1 clearance
> is tight — see `dimensions-assumed.md` §5.

## Power

| Item | Qty | Status | Spec / note |
|---|---|---|---|
| Mains PSU, 5 V 3–4 A | 1 | 🔍 → 🛒 | **Lives in the fixed cabinet**, not the door (A7.2) |
| USB-C cable, 3–6 ft | 1 | 🔍 → 🛒 | The only conductor crossing the hinge (MR10) |
| Strain relief grommets | 2 | 🛒 Buy | Both ends of the hinge service loop |
| Split loom / spiral wrap | 1 | 🔍 → 🛒 | Dress the service loop |
| AC timer or switched relay | 1 | 🔍 → 🛒 | Museum-hours scheduling (EL-4, NFR2) |
| IEC cord / power strip | 1 | 🔍 → 🛒 | |

## Mounting & structure *(mechanical, listed here for one-trip shopping)*

| Item | Qty | Status | Spec / note |
|---|---|---|---|
| 19″ blank rack panel | 1–2 | 🔍 Salvage | Becomes the fixed frame if mount candidate A wins |
| Cage nuts + rack screws | 12+ | 🔍 → 🛒 | Bring samples to test-fit on site (checklist §B4) |
| Sheet stock, door + frame | ~4 sq ft | 🔍 → 🛒 | Alu 0.050–0.080″ or ABS/HDPE, paintable |
| Continuous (piano) hinge | 1 | 🔍 → 🛒 | ≥ 24″. Hardest item to salvage |
| Hold-open stay or friction hinge | 1 | 🔍 → 🛒 | ~12 lb door (MR6) |
| Magnetic / ball-detent catch | 1–2 | 🔍 → 🛒 | Closed-position hold |
| Over-travel stop | 1 | — | Fabricated; protects the boards (MR7) |
| Nylon / felt contact pads | — | 🛒 Buy | **Required** at every artifact contact point (MR2) |
| Standoffs M2.5 / M3, nylon washers | — | 🔍 → 🛒 | Pi and controller board mounting |
| Tan paint + scrap for colour match | 1 | 🔍 Salvage | MR13 — grab a tan offcut if one exists |

## Deferred

| Item | Status | Note |
|---|---|---|
| Plexiglass board-protection panel | ⏸ Deferred | ME-10 / PRD §11 — later add-on |
| Spare-button LEDs + drivers | ⏸ Deferred | v1 buttons are unlit |
| WebSocket button transport | ⏸ Deferred | uinput synthetic keys chosen (A4.2) |

---

## What's actually blocking

Only two lines matter before the mechanical build can start:

1. **The panel** — its real outline, thickness and controller-board form factor
   set the door geometry. Everything in `mechanical/` waits on it.
2. **The mount hardware** — decided by what the cabinet offers (checklist §B, §E),
   not by what's in this table.

Everything else is cheap, standard, and substitutable — which is the point of the
"adaptable, standards-based parts" rule in architecture §9.

---

*Updated after each salvage run. Move items from 🔍 to ✅ as they come home, and
note make/model so a replacement can be sourced later.*
