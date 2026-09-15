# Electronics — what carries a volt in the kiosk

> **Concept.** Nothing here is installed in the museum.

**Rev 3 deleted most of this subsystem.** The donated hardware — a Dell
OptiPlex 9020M and an Acer T232HL touchscreen — replaced the Raspberry Pi,
the three buttons, the GPIO harness, the de-cased panel and the 5 V line
across a hinge that no longer exists. The kiosk is now two off-the-shelf
appliances, an HDMI cable, a USB cable for touch, and mains power. See the ADR
in [`../docs/02-architecture.md`](../docs/02-architecture.md) §15.

## What is left in scope

- **Power.** One mains entry, a power strip, and the two behaviours that
  decide whether the exhibit is dark in the morning: the OptiPlex BIOS must
  be set to *Restore on AC Power Loss → Power On*, and the monitor must wake
  to picture rather than standby after a cut (**Gate 1, untested**). AC
  scheduling for museum hours is #23.
- **Cabling.** HDMI and USB from the OptiPlex to the screen, routed along
  the spine. Where the OptiPlex physically sits (cabinet floor, behind the
  spine) is a mechanical question, but the cable run is ours.
- **The BOM.** Rev 3 is short: OptiPlex, screen, arm, conduit and brackets,
  power strip, cables. #25 owns it.

## What's here now

- **[`bom.md`](bom.md)** — the v0 salvage-first BOM for the Pi-and-buttons
  design. **Superseded.** Kept until the Rev 3 BOM replaces it.
- **[`salvage-recon.md`](salvage-recon.md)** — the warehouse shopping list
  written before the donation. The monitor acceptance criteria and the
  powered power-cut test are still the right test for Gate 1; the rest is
  historical.

## Deliverables still to produce

- `bom.md` rewritten for Rev 3 with real part numbers.
- A one-page cable and power note: what plugs into what, and the BIOS setting.

`wiring/` and `schematics/` were planned for the button harness and are no
longer needed.
