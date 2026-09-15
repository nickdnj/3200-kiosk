# Mechanical — how the screen stands in front of the machine

> **Concept.** Rev 3 is a drawn concept with a load argument and five open
> gates. No parts have been bought, nothing has been calipered, nothing has
> been drawn to build from. Read this page before touching anything else in
> this folder: **most of it is superseded.**

**Rev 3: doors off, touchscreen on a conduit spine.** Both factory doors lift
off their pins and go into storage. A length of 1¼″ EMT stands on the cabinet
floor, captured at two padded points ~40″ apart, and a monitor arm hangs a
23″ portrait touchscreen off it with the card cage open behind. The three
commands are on-screen targets at **38″ AFF — the ADA §308 datum that has not
moved through three revisions.**

The 3280 is not opened beyond its own doors, not drilled, not modified.

## Start here

- **[`rev3-touch-concept.html`](rev3-touch-concept.html)** — the Rev 3
  concept page. The interface, the cabinet drawn to scale with doors on and
  off, the site photographs, the Rev 2 → Rev 3 comparison, the load argument
  for the spine, and the five gates. Open it locally.
- **[`me1-findings.md`](me1-findings.md)** — the 2026-08-26 site visit. The
  machine has **two doors, not an open card cage**. Still the governing field
  record.
- **[`photos/`](photos/)** — site photographs. The Rev 3 page is drawn from
  these, not from renders.

## Why a spine and not the arm's own clamp

A 20 lb screen reaching 15″ out is a 300 in-lb overturning moment. A desk
clamp has to swallow that across a two-inch jaw — about 150 lb of bite, and
there is nothing on this machine we are willing to bite. Capture the same
conduit at two points 40″ apart and the identical moment becomes a couple of
about 7.5 lb at each end: a felt-faced foot and a padded top bracket. Twenty
times gentler, and the hinge pins never see any of it.

The spine goes on the left, the side the doors hinge from. Which side the
power-supply modules sit on is still unconfirmed.

## The five gates — before anyone buys anything

| Gate | Question | Status |
|---|---|---|
| 1 | Does the monitor come back after a power cut, or wake into standby? | **Not tested.** Go/no-go |
| 2 | Does Linux see the touch, and does it rotate with the screen? | **Closed 2026-09-14.** See `../src/controller/` |
| 3 | Does the arm's collar fit 1¼″ EMT? (1.510″ OD; arm poles run ~Ø38 mm) | No arm bought. Caliper the supplied pole first, err small, shim |
| 4 | How tall is the door opening? The conduit is cut to this | The ~48″ site reading has no note of what it spanned. **Tape it** |
| 5 | Will the museum expose the boards? | **Curatorial.** Alternative: polycarbonate in the aperture (#1) |

## Reference — what the machine actually is

| | | Provenance |
|---|---|---|
| Cabinet overall | 71″ H × 24″ W × 34″ D | OEM 50-045R00 |
| Cabinet box, less feet | 67-7/8″ | measured, ME-1 |
| Feet | 3-1/8″ | derived |
| Front opening, clear width | 18½–19¾″ | measured |
| Outer door | ≈ 24.3″ W × 68.2″ H, on two lift-off pins | 3230 drawing + derived + photographed |
| Inner panel | Perforated zinc-plated steel on a piano hinge | photographed |
| Factory paint | P.E. #464 textured | 3230 drawing |

- **[`cabinet-spec-oem.md`](cabinet-spec-oem.md)** — Concurrent's published spec.
- **[`cabinet-drawings-3230.md`](cabinet-drawings-3230.md)** — Perkin-Elmer's
  mechanical drawings for the sibling 3230. Family evidence, not gospel.
- **[`measurement-checklist.md`](measurement-checklist.md)** — the ME-1 field
  sheet. Mostly satisfied; Gate 4 is what is left.

## Still to produce

- A **parts list**: conduit, arm, foot, top bracket, padding, screen mount.
- **Drawings** of the spine, foot and top bracket, and `mounting.md` — how it
  goes in, how it comes out, what it touches (#34).
- A **bench mock-up** that holds the load before it goes near the cabinet (#27).

## The sequence

1. **Gate 4.** Tape the door opening height. Nothing is cut before this.
2. Buy the arm. **Gate 3:** caliper its collar against the conduit.
3. Cut the spine, build the foot and top bracket, mock up on the bench with
   the real screen. Confirm the touch row lands at 38″.
4. **Gate 1** on the real screen with a power strip.
5. Museum team answers **Gate 5** and accepts the touchscreen trade-off (see
   `../docs/02-architecture.md` §15).
6. Doors off, spine in, fit check (#35). Then the soak (#36).

## Superseded — kept for provenance

Rev 1 and Rev 2 designed the kiosk as a **self-contained box** (a 24″ panel
behind a cut face plate, three 30 mm switches, a Pi inside) hung on the outer
door's hinge pins. Both were finished, checked and buildable. Rev 3 threw
them away on 2026-09-03: a cased touchscreen on an arm needs no enclosure, and
a donated screen made the face-plate window moot. **Do not build from any of
this.**

- Rev 2 box: [`rev1-standalone-kiosk.md`](rev1-standalone-kiosk.md),
  [`rev1-design-study.html`](rev1-design-study.html), [`fab-rev1/`](fab-rev1/)
  (the P1 face plate, never released), [`cutlist/`](cutlist/),
  [`build-kit/`](build-kit/), [`ikea-build/`](ikea-build/),
  [`render-prompts.md`](render-prompts.md).
- Earlier replacement-door concept:
  [`monitor-selection.md`](monitor-selection.md) — *its go/no-go monitor
  criteria still apply, especially power-cut recovery* —
  [`display-approach-options.md`](display-approach-options.md),
  [`door-construction.md`](door-construction.md), [`fab/`](fab/),
  [`drawings/`](drawings/), [`dwg/`](dwg/).
- Pre-measurement guesses: [`dimensions-assumed.md`](dimensions-assumed.md),
  [`enclosure-buy-vs-build.md`](enclosure-buy-vs-build.md),
  [`drawings/superseded/`](drawings/superseded/).

One finding from the box era outlives it: ADA §307.2 allows 4″ of projection
from a wall-mounted object, and no off-the-shelf shallow cabinet exists that
is both shallow enough and stiff enough. Rev 3 sidesteps it — the screen is
on a floor-standing spine, not on the wall of the machine.
