# 3200 Kiosk — Project Brief

> **Re-scoped 2026-09-24: this was the 3280 Kiosk.** The single-machine 3280
> kiosk is cancelled. This repo now tells the story of the **Concurrent
> (Perkin-Elmer) Series 3200** as a whole. The museum's machine that was
> catalogued as a "3280" is **not a 1986 3280**. It was designed in 1993 (its
> chips date from 1993 to 1995; its programmed parts carry 1996 labels, so the
> board was built in 1996 or later), and it runs on one Am29C300 processor board. Its marketing
> name is unknown. The only name on the hardware is the board's own etch,
> "COPYRIGHT 1993 CONCURRENT COMPUTER CORPORATION". Tim Coulson, a former tech
> on it, calls it "Cruncher 5". Don't call it a 3280 anywhere. There is also a
> **3210** in storage that could come to the floor. Which
> machine or machines the kiosk stands beside is an open decision. The
> software, emulator and Rev 3 hardware carry over unchanged. The deck's
> 3280-only screens become one chapter of the series story. Repo renamed
> `nickdnj/3280-kiosk` → `nickdnj/3200-kiosk`; GitHub redirects the old URL.
> The bench PC's on-device paths (`/opt/3280-kiosk`, `/var/lib/3280-kiosk`)
> are unchanged until the next redeploy.

> **Status: CONCEPT.** This brief, the seeded app, and the renders describe the
> exhibit we're driving toward — the guiding light, not a finished piece.
> Everything here is a target to build against, not a shipped deliverable.

**Project:** An interactive kiosk built into the Vintage Computer Federation
museum's **Concurrent 3280** ("Cruncher 2"). A portrait display is mounted on a
hinge over the cabinet's card cage; a docent can swing it open to reveal the
real hardware behind it. The screen tells the machine's story, driven by **three
physical buttons only — BACK / HOME / NEXT. There is no touchscreen.**

**Team:** Software Project Team (`software-project`), provisioned by
AgentArchitect. This repo spans three disciplines — software, electronics, and
mechanical — so the deliverable is a working exhibit, not just an app.

## Where this came from

The kiosk began as a **concept-review web app** built in the `vcf` workspace
(`outputs/2026-08-20-3280-kiosk-app/`) and shared with the docent team as a
clickable Artifact. The current UI, content, and 3-button interaction model all
came out of that review. That reviewed app is seeded here at
`src/kiosk-app/` as the starting point.

## Content spec (from Rick Lewis's docent review)

Rick reviewed the concept and set the bar for on-screen content. Honor it:

- Cut copy hard — roughly **30%** of what a web page would carry.
- **3–5 short bullets per screen**, one strong graphic, big **sans-serif** type.
- Readable at **3–6 feet** standing distance.
- **Contextualize technical facts** for a general audience — no jargon dumps.
- Home is a one-screen summary: *"This computer was designed and built in New
  Jersey"* — years **1981–1986**, "Deployed everywhere."
- Verified exhibit facts only. The cabinet renders are AI concept art and are
  flagged as such; do not reuse the renders' hallucinated text.
- Rick's open asks, parked for later: a "More" detail popup (tension with the
  no-touch, 3-button model — resolve in UX), and anonymous **usage tracking**
  for the real installation.

Rick's verdict on the reworked concept: *"YES YES YES. This is just the job."*

## Cross-exhibit link (verified via wiki)

One screen ties the 3280 to the museum's **SGI Onyx**: Ken Yeager, the 3280's
lead architect, later micro-architected the **MIPS R10000** at SGI — the same
chip that runs the Onyx on display, with a standalone R10000 package sitting on
top of it. Facts sourced only to public professional records / placard-approved
wiki pages.

## Repo layout

```
docs/           this brief + team outputs: PRD → architecture → UX → dev plan
src/
  kiosk-app/    the on-screen UI (seeded from the reviewed concept app)
  controller/   buttons → app bridge; kiosk-mode launcher (SBC software)
electronics/    buttons, display, compute, power, wiring, BOM, schematics
mechanical/     hinged display panel, button plate, non-destructive 3280 mounting
tests/          test suites
```

## First moves for the team

1. **PRD** — turn this brief + Rick's spec into requirements (say "let's write
   the PRD"). Capture the museum constraints: reversible mounting, unattended
   uptime, general-audience content.
2. **Architecture** — pick the compute platform and the button→browser path;
   that choice drives both `electronics/` and `mechanical/`.
3. **UX** — resolve the "More" popup within a 3-button, no-touch model.
4. Parallel hardware tracks (electronics + mechanical) once the platform is set.

## Constraints

- The 3280 is a **museum artifact** — all mounting must be reversible and
  non-destructive.
- **Wiki first:** `~/Workspaces/wiki/` (esp.
  `projects/concurrent-3280-museum/`) is authoritative. Propose updates via the
  wiki-ingest flow; never write wiki pages directly.
