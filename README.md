# 3200 Kiosk

> **Re-scoped 2026-09-24: this was the 3280 Kiosk.** The single-machine 3280
> kiosk is cancelled. This repo now tells the story of the **Concurrent
> (Perkin-Elmer) Series 3200** as a whole. The museum's "3280" turns out to be a
> 1993 single-board Am29C300 machine that a former tech calls "Cruncher 5," and
> there is also a **3210** in storage that could come to the floor. Which
> machine or machines the kiosk stands beside is an open decision. The
> software, emulator and Rev 3 hardware carry over unchanged. The deck's
> 3280-only screens become one chapter of the series story. Repo renamed
> `nickdnj/3280-kiosk` → `nickdnj/3200-kiosk`; GitHub redirects the old URL.
> The bench PC's on-device paths (`/opt/3280-kiosk`, `/var/lib/3280-kiosk`)
> are unchanged until the next redeploy.

An interactive exhibit kiosk for the Vintage Computer Federation museum's
**Concurrent Series 3200** machines. (The Rev 3 hardware below was designed
around the "3280" cabinet.) A portrait touchscreen floats in front of the machine's
open card cage on a conduit spine. Three on-screen commands — **BACK / HOME /
NEXT** — step through the machine's story, and a final screen lets a visitor
type at a live OS/32 system.

**Rev 3: doors off, touchscreen on a spine.** Both factory doors lift off
their pins and go into storage. Nothing is cut, drilled, or fastened to the
machine. → **[Rev 3 concept page](mechanical/rev3-touch-concept.html)** ·
**[the ADR](docs/02-architecture.md#15-adr--rev-3-platform-change-2026-09-13)**

> ⚠️ **This is a concept — our guiding light, not a shipped product.** A
> working kiosk exists on a bench: the software runs on the donated hardware
> and survives a cold reboot. Nothing is installed in the museum, nothing has
> been soaked, nothing has been signed off. Treat every artifact as "the
> target" until the museum team says otherwise.

**Where things stand:** [`docs/05-status-report.md`](docs/05-status-report.md)
— the handoff document, kept current.

This repo spans three disciplines:

| Area | Path | Status |
|---|---|---|
| On-screen app | `src/kiosk-app/` | **Working.** 16 screens, single-source content, fit-checked, deployed to the bench kiosk |
| Kiosk runtime | `src/controller/` | **Working.** Ubuntu 24.04 + X11 + Chromium kiosk on a Dell OptiPlex 9020M, portrait + touch proven across a cold reboot |
| OS/32 emulator | `src/emulator/` | **Working.** Real OS/32 on SIMH, touch terminal, one-tap Fortran / Pascal / C |
| Electronics | `electronics/` | Superseded by the donated hardware. README says what survives |
| Mechanical | `mechanical/` | **Rev 3 concept only.** Five gates open, no parts bought, nothing drawn to build from |

Team: **Software Project Team**, provisioned by AgentArchitect (2026-08-22).

## Going to the museum or the warehouse?

- **[Rev 3 concept page](mechanical/rev3-touch-concept.html)** — the design,
  the site photographs, and the five gates. **Gate 4 needs a tape measure:**
  the height of the door opening, and what the ~48″ reading from the site
  visit actually spanned.
- **[Site findings](mechanical/me1-findings.md)** — what is actually behind
  the doors. Two doors, not an open card cage.
- **[Measurement field sheet](mechanical/measurement-checklist.md)** — the
  original ME-1 checklist, mostly satisfied.

> The cabinet is measured (71 × 24 × 34, box 67-7/8″). The screen and the
> mini PC are real and on a bench. The conduit, the arm and the brackets are
> not bought and not drawn.

## Planning docs

`docs/00-project-brief.md` → `01-prd.md` → `02-architecture.md` →
`03-ux.md` → `04-dev-plan.md` → `05-status-report.md`. The PRD, UX and dev
plan were written for Rev 1; the architecture doc's §15 records the Rev 3
change. Work is tracked as
[GitHub issues](https://github.com/nickdnj/3200-kiosk/issues), reconciled
with Rev 3 on 2026-09-15.

## Start

```bash
claude
```

New here? Read `docs/05-status-report.md`, then `docs/00-project-brief.md`.

## Run the app locally

```bash
cd src/kiosk-app
python3 build-app.py          # concept-review page -> index.html
open index.html
python3 build-kiosk.py        # the deployable 1080x1920 panel build -> dist/kiosk/
python3 check-fit.py          # always, after any copy change
```
