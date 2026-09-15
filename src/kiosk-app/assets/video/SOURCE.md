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
  Flagged for Rick's docent review like all new exhibit copy.

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
- **Why it's here (the real link, not MASSCOMP):** NASA's **Shuttle Mission
  Simulator** (astronaut training, Singer-Link built) ran on **Perkin-Elmer
  8/32** computers per NASA JSC records. The Perkin-Elmer 8/32 is the 3280's
  direct architecture ancestor (Interdata 8/32 -> Perkin-Elmer -> 3200 series
  -> 3280), so this machine's own family trained the Shuttle crews. Flagged for
  docent review; the 8/32 is the ancestor line, not the 3280 model itself.
- **Cut:** three segments (launch, orbiter-over-Earth ×2), muted, H.264, via the
  same ffmpeg concat recipe as the NOAA loop.
