#!/usr/bin/env python3
"""Render the built kiosk at true panel resolution in headless Chrome and
measure whether every screen's content actually fits the box.

The build's arithmetic says it should. Arithmetic cannot predict reflow - a
headline that wraps to three lines instead of two blows the budget - so this
renders it for real and measures. Run it after ANY copy change.

    python3 check-fit.py               measure, and save a contact sheet
    python3 check-fit.py --shots       also save every screen full size
"""
import argparse, json, pathlib, re, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).parent
SRC  = HERE / "dist" / "kiosk" / "index.html"
SHOT = HERE / "dist" / "shots"
W, H = 1080, 1920

CHROME = next((p for p in [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    shutil.which("google-chrome") or "", shutil.which("chromium") or "",
    shutil.which("chromium-browser") or "",
] if p and pathlib.Path(p).exists()), None)

PROBE = r"""
<!-- infinite keyframes never let Chrome's virtual clock drain -->
<style>*,*::before,*::after{animation:none!important;transition:none!important}</style>
<script>
window.addEventListener('load',()=>setTimeout(()=>{
  const d=document.getElementById('display');
  const out=[...document.querySelectorAll('.card')].map((el,i)=>{
    const cs=getComputedStyle(el);
    const pad=parseFloat(cs.paddingTop)+parseFloat(cs.paddingBottom);
    let need=pad;
    for(const c of el.children){
      if(c.classList.contains('hl'))continue;
      const m=getComputedStyle(c);
      const auto_=c.matches('.prompt,.morep');   // margin-top:auto - that gap IS the slack
      need+=c.getBoundingClientRect().height+parseFloat(m.marginBottom)
           +(auto_?0:parseFloat(m.marginTop));
    }
    const bleed=el.classList.contains('img')||el.classList.contains('contain')||el.classList.contains('ppage');
    const kick=(el.querySelector('.ek,.kick,.imgcap .k')||{}).textContent||'';
    return {n:i+1,bleed,kick:kick.trim().slice(0,26),
            need:Math.round(need),have:el.clientHeight};
  });
  document.title='FIT'+JSON.stringify({vw:innerWidth,vh:innerHeight,
    deck:[Math.round(d.getBoundingClientRect().width),Math.round(d.getBoundingClientRect().height)],
    nav:Math.round(document.querySelector('.nav').getBoundingClientRect().height),cards:out});
},400));
</script>
"""

def render(html, out_png=None, wait=25, win_h=H):
    """Headless Chrome on macOS emits the DOM and then declines to exit, so we
    read what we need and kill it. --headless=old because the new one never
    produces output here at all."""
    with tempfile.TemporaryDirectory() as td:
        f = pathlib.Path(td) / "probe.html"
        f.write_text(html, encoding="utf-8")
        cmd = [CHROME, "--headless=old", "--disable-gpu", "--no-sandbox",
               "--disable-extensions", "--no-first-run", "--disable-sync",
               "--force-device-scale-factor=1", "--hide-scrollbars",
               "--virtual-time-budget=5000",   # let the probe timer fire before the dump
               f"--window-size={W},{win_h}", f"--user-data-dir={td}/u"]
        if out_png:
            pathlib.Path(out_png).parent.mkdir(parents=True, exist_ok=True)
            cmd.append(f"--screenshot={out_png}")
        cmd += ["--dump-dom", f.as_uri()]
        pr = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, text=True)
        try:
            out, _ = pr.communicate(timeout=wait)
        except subprocess.TimeoutExpired:
            pr.kill()
            out, _ = pr.communicate()
        return out or ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shots", action="store_true", help="save a PNG of every screen")
    a = ap.parse_args()

    if CHROME is None:
        sys.exit("no Chrome/Chromium found - cannot render. Install one, or skip this check.")
    if not SRC.exists():
        sys.exit(f"{SRC} missing - run build-kiosk.py first")

    base = SRC.read_text(encoding="utf-8")
    SHOT.mkdir(parents=True, exist_ok=True)

    def probe(height, png=None):
        dom = render(base + PROBE, png, win_h=height)
        m = re.search(r"<title>FIT(\{.*?\})</title>", dom, re.S)
        if not m: sys.exit("probe did not report - the page may not have loaded")
        return json.loads(m.group(1))

    # headless keeps some of the window for itself; claim the shortfall back so
    # we are measuring against the real 1920, not whatever Chrome felt like
    d = probe(H)
    if d["vh"] != H:
        d = probe(H + (H - d["vh"]), SHOT / "screen-01.png")
    else:
        d = probe(H, SHOT / "screen-01.png")
    if d["vh"] != H:
        sys.exit(f"could not get a {W}x{H} viewport (got {d['vw']}x{d['vh']})")

    print(f"\nrendered {d['vw']} x {d['vh']}   deck {d['deck'][0]} x {d['deck'][1]}   nav {d['nav']}\n")
    bad = []
    for c in d["cards"]:
        if c["bleed"]:
            print(f"  ---   {c['n']}  {c['kick']:<28} full-bleed image")
            continue
        over = c["need"] - c["have"]
        slack = -over / c["have"] * 100
        flag = "ok  " if over <= 0 else "OVER"
        if over > 0: bad.append((c["n"], c["kick"], over))
        print(f"  {flag}  {c['n']}  {c['kick']:<28} needs {c['need']:>5} of {c['have']}"
              + (f"   slack {slack:4.1f}%" if over <= 0 else f"   OVER BY {over} px"))

    WIN_H = H + (H - probe_vh) if (probe_vh := d["vh"]) != H else H
    if a.shots:
        for n in range(2, len(d["cards"]) + 1):
            jump = f"<script>window.addEventListener('load',()=>setTimeout(()=>show({n-1}),300));</script>"
            render(base + jump, SHOT / f"screen-{n:02d}.png", win_h=WIN_H)
        print(f"\n  shots -> {SHOT}")

    if bad:
        print("\n*** CONTENT OVERFLOWS " + str(len(bad)) + " SCREEN(S) ***")
        for n, k, o in bad:
            print(f"      screen {n} ({k}) clips {o} px - cut a bullet or lower --fit")
        sys.exit(1)
    tight = min((c["have"] - c["need"]) / c["have"] for c in d["cards"] if not c["bleed"])
    print(f"\n  all screens fit. tightest has {tight*100:.1f}% slack.")

main()
