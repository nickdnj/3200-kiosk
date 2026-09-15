# Kiosk App — the on-screen UI

> **Concept, not shipped.** Nothing here is installed in the museum. The
> cabinet imagery on the concept page is AI concept art; the copy is Rick
> Lewis's reviewed draft. Keep the "Concept" marker until the piece is built.

Nine screens telling the Concurrent 3280's story, driven by **three commands —
BACK / HOME / NEXT**. As of Rev 3 those are on-screen touch targets rather than
physical switches, but the deck itself never knew the difference and still
doesn't: arrow keys and `Home` drive it identically.

## Layout

```
_deck.py          THE CONTENT. Nine screens + the screen CSS + the image and
                  font inlining. Edit here; both builders read it.
build-app.py   -> index.html        the concept-review page (cabinet + screen)
build-kiosk.py -> dist/kiosk/       the deployable panel build
check-fit.py      renders the panel build for real and measures overflow
fetch-fonts.py    re-pulls the woff2 files (rarely needed)
assets/           source images and the cached latin-subset fonts
```

**`_deck.py` is the single source of truth.** Two targets, one copy of Rick's
words, so they cannot drift apart. Never hand-edit a generated `index.html`.

## Build

```bash
python3 build-app.py      # concept page   -> index.html
python3 build-kiosk.py    # the real thing -> dist/kiosk/index.html
python3 check-fit.py      # then ALWAYS this, if you touched any copy
```

`build-kiosk.py --panel 27` re-derives the geometry for a different panel;
`--nav`, `--idle` and `--fit` are the other knobs. It prints its own checks —
touch-target size, dead space, type legibility at distance — and exits
non-zero if one fails.

## Why `check-fit.py` exists

The build's arithmetic sizes the type to fit. Arithmetic cannot predict
**reflow** — a headline that wraps to three lines instead of two blows the
budget, and you only find out on the exhibit floor. So `check-fit.py` renders
the real build in headless Chrome at a true 1080×1920 and measures every
screen's content against its box. Today the tightest screen has ~6% slack.

Run it after any copy change. It is 25 seconds.

## Two things that will bite you if you forget them

- **The kiosk has no network.** Fonts are embedded as base64 woff2, images as
  data URIs, and `build-kiosk.py` asserts that no `http://` or `https://`
  survives into the output. Left pointing at Google Fonts, the page looks
  perfect on a laptop and silently reflows to fallback faces in the museum.
- **Declare the charset.** Over `file://` with no `<meta charset>`, Chrome
  falls back to windows-1252 and every `·` becomes `Â·`. Both builders now
  emit the meta tag, and the deck's copy uses HTML entities as well.

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

## Still open

- Decouple content from `_deck.py` into a data file non-devs can edit.
- Anonymous screen-view counts (a museum-team ask) — needs a privacy decision first.
- An attract loop with motion, if the still HOME screen doesn't pull people in.

## Which 3280? (read before adding specs)

The museum's machine is a **Concurrent 3280** — the **single-processor**
machine, ~6 MIPS. It is **not the 3280E MPS**, the 2–12 CPU multiprocessor
(76.8 aggregate MIPS, the S-Bus dual data paths). Exhibit copy must never
attribute MPS specs to "this machine." A "Twelve brains, one machine" slide was
removed on 2026-09-15 for exactly this reason (Nick DeMarco, Concurrent alum).
