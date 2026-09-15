# Kiosk App — the on-screen UI

> **Concept, not shipped.** Nothing here is installed in the museum. The
> panel build runs on the bench kiosk (a donated OptiPlex + Acer touchscreen)
> and nowhere else. The cabinet imagery on the concept page is AI concept art.
> Keep the "Concept" marker until the piece is built and installed.

Twenty-two screens telling the Concurrent 3280's story, plus a final one that
hands the visitor a live OS/32 terminal (see `../emulator/`). Driven by
**three commands — BACK / HOME / NEXT**. As of Rev 3 those are on-screen touch
targets rather than physical switches, but the deck itself never knew the
difference and still doesn't: arrow keys and `Home` drive it identically.

## Layout

```
_deck.py          THE CONTENT. All screens + the screen CSS + the image and
                  font inlining. Edit here; both builders read it.
build-app.py   -> index.html        the concept-review page (cabinet + screen)
build-kiosk.py -> dist/kiosk/       the deployable panel build
check-fit.py      renders the panel build for real and measures overflow
fetch-fonts.py    re-pulls the woff2 files (rarely needed)
assets/           source images, video, and the cached latin-subset fonts
```

**`_deck.py` is the single source of truth.** Two targets, one copy of the
reviewed words, so they cannot drift apart. Never hand-edit a generated
`index.html`.

## The deck

| # | Section | Screen |
|---|---|---|
| 1 | Home | The Concurrent 3280 was made in New Jersey |
| 2 | What it did | One machine, many jobs |
| 3–5 | · weather · space · finance | NEXRAD radar, Shuttle training, trading floors. Real footage, public domain or sourced |
| 6 | Under the hood | Big iron, built by hand |
| 7–8 | · the system · the processor | Inline-SVG block diagrams: S-bus, memory, I/O; the four boards and the four-stage pipeline |
| 9–12 | · FET · VAT · ALU · MPY | One screen per processor board, with a diagram of what it does and who built it |
| 13–14 | Where it was born | Monmouth County; the sixty-year lab lineage |
| 15–17 | Who built it | The small team; the Cruncher 2 roster; the 1985–86 bring-up |
| 18 | A quiet first | The line that set Unix free |
| 19 | Just down the room | Cross-link to the SGI Onyx |
| 20–22 | Open it up | Full-bleed photographs of the card cage, processor, memory and control |
| 23 | Try it yourself | The OS/32 terminal |

The architecture screens are drawn from Concurrent's own manuals on bitsavers:
*System Bus Theory* 63-002 R00 (1987), whose Fig. 1-1 names the four processor
boards **VAT / FET / ALU / MPY**, and the *3280 Product Overview* 50-045R00
(1989) pp.29–35. The manuals never say one board equals one pipeline stage,
so the deck does not either. The diagrams are inline SVG in the screen
palette, so they scale with the panel like everything else.

The team and bring-up screens draw on Ken Yeager's letters and were cleared
for public by Ruth Yeager (2026-09-15).

## Build

```bash
python3 build-app.py      # concept page   -> index.html
python3 build-kiosk.py    # the real thing -> dist/kiosk/index.html
python3 check-fit.py      # then ALWAYS this, if you touched any copy
```

`build-kiosk.py --panel <diagonal>` re-derives the geometry for a different
panel. **The default is 23.8″; the bench kiosk's Acer T232HL is a 23″ panel.**
Pass `--panel 23` and re-read the legibility lines until the default is
changed. `--nav`, `--idle` and `--fit` are the other knobs. It prints its own
checks — touch-target size, dead space, type legibility at distance — and
exits non-zero if one fails.

Deploying to the bench kiosk is by hand today: copy `dist/kiosk/index.html`
to `/opt/3280-kiosk/index.html` on the OptiPlex (that is what
`../controller/install.sh` does on a fresh machine). A deploy script is
tracked as issue #4.

## Why `check-fit.py` exists

The build's arithmetic sizes the type to fit. Arithmetic cannot predict
**reflow** — a headline that wraps to three lines instead of two blows the
budget, and you only find out on the exhibit floor. So `check-fit.py` renders
the real build in headless Chrome at a true 1080×1920 and measures every
screen's content against its box. Today the tightest content screen (weather)
has 6.9% slack; the emulator screen reports 0% because it fills its box by
design.

Run it after any copy change. It is 25 seconds.

## Two things that will bite you if you forget them

- **The kiosk has no network.** Fonts are embedded as base64 woff2, images as
  data URIs, and `build-kiosk.py` asserts that no `http://` or `https://`
  survives into the output. Left pointing at Google Fonts, the page looks
  perfect on a laptop and silently reflows to fallback faces in the museum.
- **Declare the charset.** Over `file://` with no `<meta charset>`, Chrome
  falls back to windows-1252 and every `·` becomes `Â·`. Both builders emit
  the meta tag, and the deck's copy uses HTML entities as well.

## The screen, and what Rev 3 cost it

The deck's CSS is written in container-query units (`cqw`), so it is
resolution-independent — the same numbers render at 470 px on the concept page
and at 1080 px on the panel. What is *not* free is the aspect change: the
screens were laid out for a 230:529 box, a real 16:9 panel in portrait is
9:16, and the touch bar takes another 8.9%. `build-kiosk.py` computes a single
scale factor `S` (0.70 today) from the actual remaining box.

The honest consequence is in `docs/02-architecture.md` §15: body bullets now
subtend 13.6 arcmin at 6 ft against a 16 arcmin comfort threshold. At arm's
length — where you must stand to touch anything — they are at 33. The headline
still carries the room. Cutting one bullet per screen would buy ~29% more
type, and that is the museum team's call.

## Built-in behaviours worth knowing

- **Idle reset.** 75 s of no input returns to Home. Suppressed while a video
  slide is playing.
- **Diagnostics panel.** Hold the top-left corner for 3 s: screen size, device
  pixel ratio, orientation, `maxTouchPoints`, last touch coordinates. This is
  how you prove the touch matrix is right after rotating.

## Still open

- Decouple content from `_deck.py` into a data file non-devs can edit (#2).
- Anonymous screen-view counts, a museum-team ask. Needs a privacy decision first (#18, #19).
- An attract loop with motion, if the still HOME screen doesn't pull people in.

## Which 3280? (read before adding specs)

The museum's machine is a **Concurrent 3280** — the **single-processor**
machine, ~6 MIPS. It is **not the 3280E MPS**, the 2–12 CPU multiprocessor
(76.8 aggregate MIPS, the S-Bus dual data paths). Exhibit copy must never
attribute MPS specs to "this machine." A "Twelve brains, one machine" slide was
removed on 2026-09-15 for exactly this reason (Nick DeMarco, Concurrent alum).
