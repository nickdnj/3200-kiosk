# nexrad-loop.mp4 — provenance

A 69-second silent loop for the exhibit's Weather screen.

- **Source:** "NEXRAD: Eye to the Sky", **NOAA Weather Partners** (official
  NOAA/NWS channel), published 2009-04-03.
  https://www.youtube.com/watch?v=KdKouCnhvPs
- **Rights:** US federal government (NOAA/NWS) work — **public domain**
  (17 U.S.C. §105). Credited on-screen as a courtesy.
- **Honesty note:** 2009 NEXRAD did **not** run on a Concurrent 3280 (the 3280
  is 1988; NEXRAD's compute was replaced by then). The screen frames it as
  *the system the Concurrent line helped pioneer*, not as the 3280 itself.
  flagged for museum-team review like all new exhibit copy.

## How it was made

```bash
yt-dlp -f "b[height<=480]/bv[height<=480]+ba/b" --merge-output-format mp4 \
  -o nexrad-raw.mp4 "https://www.youtube.com/watch?v=KdKouCnhvPs"
# montage of four verified segments: radome, Doppler-velocity explainer,
# forecaster workstation, historical radar antenna
ffmpeg -i nexrad-raw.mp4 -filter_complex \
 "[0:v]trim=14:31,setpts=PTS-STARTPTS[a];[0:v]trim=149:166,setpts=PTS-STARTPTS[b];\
  [0:v]trim=271:289,setpts=PTS-STARTPTS[c];[0:v]trim=389:406,setpts=PTS-STARTPTS[d];\
  [a][b][c][d]concat=n=4:v=1:a=0,scale=640:480,format=yuv420p[out]" \
 -map "[out]" -an -c:v libx264 -crf 24 -movflags +faststart nexrad-loop.mp4
```

Deployed on the kiosk at `/opt/3280-kiosk/nexrad-loop.mp4`; the page references
it by relative path. The concept page shows a still poster instead (the mp4
isn't shipped in the shareable artifact).

---

# shuttle-loop.mp4 — provenance

63-second silent loop for the Space slide.

- **Source:** "Space Shuttle Launch and Landing Highlights", **NASA**, via
  Internet Archive (`SpaceShuttleLaunchAndLandingHighlights`, 720p).
- **Rights:** NASA — **public domain**. Credited on-screen.
- **Why it's here (upgraded 2026-09-15, Yeager letters, Ruth-cleared):** the SMS first ran on 27 Interdata 8/32 processors; **three Concurrent 3280s (MPS configuration) replaced all 27.** Earlier framing below kept for history.
- **Earlier framing:** NASA's **Shuttle Mission
  Simulator** (astronaut training, Singer-Link built) ran on **Perkin-Elmer
  8/32** computers per NASA JSC records. The Perkin-Elmer 8/32 is the 3280's
  direct architecture ancestor (Interdata 8/32 -> Perkin-Elmer -> 3200 series
  -> 3280), so this machine's own family trained the Shuttle crews. Flagged for
  docent review; the 8/32 is the ancestor line, not the 3280 model itself.
- **Cut:** three segments (launch, orbiter-over-Earth ×2), muted, H.264, via the
  same ffmpeg concat recipe as the NOAA loop.

---

# f16sim-loop.mp4 — provenance

56-second silent loop, cut for a Defense slide that was **removed from the deck
on 2026-09-15 at Nick's request**. Clip retained here (public domain, documented)
in case it returns; not referenced by any screen.

- **Source:** "F-16 Simulator B-roll", **U.S. Air Force** via DVIDS (asset 723256,
  DOD_107455891). A USAF pilot in an F-16 Fighting Falcon simulator, Arlington,
  Texas, June 26, 2019 — "the simulator models all of the fighter aircraft's
  weapon systems and ordnance, supporting basic and advanced pilot mission
  training, tactics validation, and mission rehearsal."
- **Rights:** US federal (USAF) work — **public domain**. Credited on-screen.
- **Honesty note:** 2019 footage of *the kind of trainer* Concurrent's real-time
  machines drove (F-16/F-15 simulators, per FlightGlobal '96 via the wiki) —
  not a 1980s Concurrent-driven sim itself. Flagged for docent review.
- **Cut:** four segments (dome edge / HUD over city / tanker refuel / HUD over
  desert), 1024x576 source → 640x360, muted, H.264, ffmpeg concat.

---

# nyse-loop.mp4 — provenance

56-second silent loop for the Finance slide.

- **Source:** "Vista Stock Shots: New York Stock Exchange" — **Prelinger Archives**
  via Internet Archive (`0803_Vista_Stock_Shots_New_York_Stock_Exchange_13_00_55_00`),
  described as "excellent traders and floor action." Old color stock; a light
  brightness/contrast lift (eq) applied so it reads on the panel.
- **Rights:** Prelinger Archives collection — **public domain**. Credited on-screen.
- **The slide's facts:** RELIANCE = Perkin-Elmer's transaction-processing system
  (ITC + DMS/32 + COBOL) "on any of Perkin-Elmer's 32-bit minicomputers,"
  maintaining performance "under extremely heavy transaction volume," with
  transaction units, secure logging, fast recovery — *Datapro Series 3200
  report, Dec 1979*, which also sampled "a supplier of systems for banks" among
  users and cites 2,500 installed 32-bit systems. "Many operating order-routing
  systems were overwhelmed during the 1987 stock market crash" — *U.S. Office
  of Technology Assessment, 1990*. **Telerate** (the financial-data/market-feed company) is named as a 3280-line customer in Ken Yeager's letters (poster-plan.md, verified/line-cited). Beyond that, no single named NYSE/bank customer is in the public record; flagged for docent review (Nick may know one).
- **Cut:** four segments (wide floor / overhead post / crowded post / clerk's
  slips), 640x480, muted, H.264, ffmpeg concat.
