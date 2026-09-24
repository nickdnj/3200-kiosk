# Door Construction — ME-4 Spec

> ## ⛔ SUPERSEDED FOR REV 1
> The kiosk is no longer a replacement door integrated into the cabinet. It is a
> **self-contained enclosure surface-mounted on the closed factory door** — see
> [`rev1-standalone-kiosk.md`](rev1-standalone-kiosk.md) and the
> [interactive design study](rev1-design-study.html).
> This document describes the **Rev 2** concept and is kept for provenance.
> Don't build from it.

> **Status: CONCEPT / spec.** Material and method are decided (2026-08-22);
> final geometry is not. The dimensions here inherit from
> [`dimensions-assumed.md`](dimensions-assumed.md) and are **assumed until ME-1
> and the salvaged panel land.** Do not order parts against this yet — see §9.

**Decision:** the door face, rear shroud and button plate are **laser-cut 5052
aluminum, outsourced to a job shop**. Small parts are 3D printed. Finishing and
assembly happen locally.

**Reads with:** [`dimensions-assumed.md`](dimensions-assumed.md) ·
[`../docs/01-prd.md`](../docs/01-prd.md) §9 (MR5, MR8, MR12–MR19) ·
[`../docs/02-architecture.md`](../docs/02-architecture.md) §8

---

## 1. The governing idea: the door is a box

A 14.5″ × 30″ sheet of anything thin is floppy. Rigidity comes from the **closed
box section** formed when the face and the rear shroud are joined around the
perimeter — not from either part alone.

**Consequence:** the shroud is a structural member, not a cover. It gets designed
and toleranced with the face, and the two are never considered separately. A door
assembled face-first with the shroud "added later" will sag and rack.

---

## 2. Why aluminum, and why outsourced

**Why aluminum**

- **It matches the artifact.** The 3280's cabinet is painted sheet metal. An
  aluminum door has the same sheen, edge quality and sound. Wood and plastic read
  wrong at the distance a docent stands.
- **It solves the thermal problem** (§5). A Pi 4 *and* an LCD backlight inside a
  sealed 2.5″ box is a real risk. Aluminum gives a conduction path; plastic and
  wood do not.
- **It's light enough.** 5052 at these gauges lands the door around 14.5 lb —
  fine for a continuous hinge.
- **Fire behaviour** is a non-issue in an exhibit enclosure.

**Why outsourced**

Mechanical is the highest-risk track and it isn't the builder's strong domain —
electronics is. Outsourcing the sheet metal converts the hardest fabrication step
into a **CAD step**. "Cut a clean 11.8″ × 20.9″ window in aluminum by hand"
becomes "check a drawing." That is the largest single risk reduction available on
ME-4.

This does not conflict with salvage-first (architecture §9): that policy governs
*parts* — monitors, buttons, hardware. Budget is explicitly not a constraint
(PRD §15). Fabricating the one component that has to look right is a different
question from buying a monitor that could have been scavenged.

**Rejected:** steel (~16 lb, too heavy for the hinge) · acrylic (cracks at
fastener holes under public abuse) · HDPE (won't take paint — kills MR13) ·
3D-printed face (5× any consumer bed; tiling means visible seams and warp).

---

## 3. Parts

### Outsourced — laser cut

| # | Part | Material | Operations | Finish as ordered |
|---|---|---|---|---|
| **P1** | Door face | 5052-H32, **0.080″** | Cut outline, screen window, button holes, badge recess, perimeter mounting holes | Raw, deburred — painted locally |
| **P2** | Rear shroud | 5052-H32, **0.063″** | Cut flat blank + vent pattern, then **bent** to a shallow tray | Raw, deburred |
| **P3** | Button plate | 5052-H32, **0.080″** | Cut outline + 5 button holes (3 used, 2 blanked) | **Black anodized** |
| **P4** | Panel retention brackets | 5052, 0.063″ | Cut + bent L-brackets, slotted holes | Raw |

**P3 is deliberately a separate part.** Spares can be re-drilled or the plate
swapped without touching the painted tan face. It also gets a crisper black from
anodizing than from paint.

### 3D printed

| # | Part | Note |
|---|---|---|
| S1 | LCD panel retention clips | Clamp the panel chassis edge on foam |
| S2 | Pi 4 mount / standoff carrier | Positions the Pi against the shroud for thermal contact |
| S3 | Controller-board standoff carrier | |
| S4 | Hinge spacers / shims | Set the door's standoff from the frame |
| S5 | **Over-travel stop** | MR7 — protects the boards. Print in PETG, not PLA |
| S6 | Button-plate backing / light block | |

### Bought

Perimeter joining angle or standoffs, M3 fasteners, closed-cell foam gasket tape,
thermal pad, nylon washers, self-etching primer, tan topcoat, satin black.

---

## 4. The stack — front to back

| Depth | Layer |
|---|---|
| 0.080″ | **P1 face**, tan, with the screen window |
| — | Satin-black bezel band, painted on P1 around the window |
| ~0.03″ | Foam gasket — light seal + compliance against the panel glass |
| ~0.60″ | **De-cased LCD panel** |
| ~0.40″ | Standoff / air gap |
| ~1.00″ | Controller board + Pi 4 on standoffs |
| 0.063″ | **P2 rear shroud**, vented, screwed on — removable for service (MR16) |
| **2.50″** | **Total target** |

**Window sizing.** The cut window is **0.06″ smaller than the active area
overall** (0.03″ overlap per side) so the bezel hides the panel's edge transition
and any backlight leak. Cutting the window exactly to the active area leaves a
visible seam.

**Panel retention — read this before touching a de-cased panel.** A bare LCD is
held in a thin metal chassis frame and the glass is fragile. **Never screw into
the panel** unless it has factory mounting tabs. Retain it by clamping the
*chassis edges* between the face and the P4 brackets, on foam. Use **slotted
holes** in P4 — the salvaged panel's real outline is the biggest unknown in this
design and the brackets have to absorb that variation.

---

## 5. Thermal

A Pi 4 and an LCD backlight in a sealed 2.5″ enclosure is the failure that shows
up three months after install, not on the bench. Two mitigations, both required:

1. **Conduction.** A thermal pad from the Pi's SoC to the P2 shroud makes the
   **entire shroud a heatsink**. This is the main reason the shroud is aluminum.
   S2 positions the Pi to hold that contact.
2. **Convection.** Vent pattern cut into P2 while it's flat — free, the laser is
   already running. **Intake low, exhaust high**, so it chimneys. As drawn
   in [`fab/`](fab/): two fields of 6 × 10 slots at 1.60″ × 0.20″ — 38.4 sq in,
   **8.8%** of the rear face, webs 0.47″. The soak test below is the real
   acceptance criterion; if it runs hot, open the fields up or add a fan.

**Verify on the bench** (part of EL-1 / IN-2): assembled and closed, run the app
for two hours and log `vcgencmd measure_temp`. Sustained temps under 70 °C are
fine; anything approaching 80 °C means more open area or an active fan.

---

## 6. Finish

Order the parts **raw and deburred, not powder coated** — job shops can't
custom-match a 1980s tan from a standard powder palette.

1. Degrease.
2. **Self-etching primer** — mandatory on aluminum; ordinary primer will peel.
3. **Tan topcoat**, matched from the scavenged scrap panel (salvage-recon §4).
   Automotive rattle can or airbrush; several light coats.
4. **Satin black** bezel band around the window, masked.
5. Clear coat if the exhibit gets handled hard — optional.
6. **CONCURRENT badge** in the recess (MR13).

P3 arrives black anodized and needs no finishing.

---

## 7. Weight

| Item | lb |
|---|---|
| P1 face, 0.080″ alu, less window | 3.4 |
| P2 shroud, 0.063″ alu | 4.0 |
| De-cased panel + controller board | 4.5 |
| Pi 4 + wiring | 0.5 |
| Buttons + P3 plate | 1.0 |
| Fasteners, angle, brackets | 1.0 |
| **Total** | **~14.5 lb** |

Supersedes the ~12 lb figure in drawing 02. CG sits roughly 7″ from the hinge
line → **~100 in-lb** moment. A continuous (piano) hinge handles this comfortably;
two butt hinges would be marginal and would let the free edge sag over time.
**Spec the continuous hinge.**

---

## 8. Working with the job shop

Candidates: SendCutSend, OSH Cut, Ponoko. All cut 5052, bend, tap, countersink,
deburr and anodize.

**File requirements**

- **DXF, one part per file**, units in inches.
- Closed vector paths, no overlapping or duplicate lines, no construction
  geometry, no dimensions or text in the cut layer.
- Bend lines on a separate layer, with the bend direction called out.
- Minimum hole diameter ≥ material thickness — all our holes clear this easily.
- Inside bend radius ≈ material thickness for 5052; include **bend relief** at
  the corners of P2 or it will tear.

**Specify on the order:** deburr all edges (public-safety, MR15) · P3 black
anodize · P1/P2/P4 raw for local paint · countersink any fastener that must sit
flush on the face.

**Tolerance reality.** Laser cut parts come in around ±0.005″ — far tighter than
anything else in this build. **The uncertainty is the salvaged panel, not the
fabrication.** That's why P4 has slotted holes and the panel is clamped on foam
rather than dropped into a tight pocket.

---

## 9. What's still blocked

Parts cannot be ordered until three things are known:

| Blocker | Source | What it fixes |
|---|---|---|
| **Real panel outline + thickness** | EL-5, after salvage | P1 window, P4 brackets, the whole depth budget |
| **Controller board footprint + cable lengths** | EL-5 | Interior layout, where the Pi sits |
| **C1 clearance** | ME-1 §C | Whether 2.5″ depth survives at all |

If C1 comes in under 2.5″, the escalation ladder in
[`dimensions-assumed.md`](dimensions-assumed.md) §5 applies and this spec is
revised before anything is cut.

---

## 10. Build sequence

1. **ME-1** — measure the machine; confirm C1 and the opening.
2. **EL-5** — salvage and power-test the panel, then de-case it. Measure the real
   outline, thickness, and controller-board footprint.
3. **Full-size cardboard mockup.** Cut the door outline from cardboard or
   hardboard and hold it in the opening. Checks ADA reach, sightlines, swing
   clearance and how much card cage stays visible — **before** spending on
   aluminum. Cheapest de-risking step in the whole project.
4. **CAD → DXF** for P1–P4.
5. **Order.** ~1 week turnaround.
6. **3D print** S1–S6 while the order is out.
7. **Finish** P1, P2, P4 — prime, tan, black bezel band, badge.
8. **Assemble** and bench-test: thermal soak, swing travel, hold-open, button feel.
9. **ME-5** hinge and stay; then **IN-1** install.

Step 3 is not optional. A cardboard door costs an hour and catches every
proportion mistake that would otherwise arrive as finished, painted metal.

---

**Fabrication package:** [`fab/`](fab/) — order sheet, DXFs, previews and the
parametric generator. Built against assumed numbers; see its §6 release gate.

*Tracks [ME-4](https://github.com/nickdnj/3200-kiosk/issues/29). Revised when
ME-1 and EL-5 data land.*
