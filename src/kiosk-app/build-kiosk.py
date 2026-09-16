#!/usr/bin/env python3
"""Build the DEPLOYABLE kiosk - the thing Chromium actually loads on the panel.

Not the concept page. This target is full-bleed portrait, touch-driven, with no
masthead, no cabinet render and no modal: the deck IS the screen.

    python3 build-kiosk.py            -> dist/kiosk/index.html
    python3 build-kiosk.py --panel 27 -> same, sized for a 27" panel

Content comes from _deck.py, shared byte-for-byte with the concept page, so
the docent-approved copy can never drift between the two.

The one transform applied here: the deck's type was laid out for a 230:529 box
(the concept page's screen). A real 16:9 panel in portrait is 9:16 - propor-
tionally shorter - and a nav bar takes a further bite. So every cqw value is
scaled by S, computed below from the actual remaining box. Clamps are dropped
entirely: they existed to keep a 470 px thumbnail legible and would otherwise
pin every size to its maximum on a 1080 px panel.
"""
import argparse, math, pathlib, re, sys
import _deck

ap = argparse.ArgumentParser()
ap.add_argument("--panel", type=float, default=23.8, help="panel diagonal, inches")
ap.add_argument("--nav",   type=float, default=1.85, help="nav bar height, inches")
ap.add_argument("--idle",  type=int,   default=75,   help="idle reset, seconds")
ap.add_argument("--fit",   type=float, default=1.00, help="extra fit factor on S")
A = ap.parse_args()

# ---- panel geometry -------------------------------------------------------
NAT_W, NAT_H = 1080, 1920                 # portrait pixels
K            = math.hypot(16, 9)          # 18.3576
PANEL_W      = A.panel * 9  / K           # short edge = portrait WIDTH
PANEL_H      = A.panel * 16 / K
PPI          = NAT_W / PANEL_W

NAV_PX   = round(A.nav * PPI)
PROG_PX  = 10                             # the progress strip is screen too
DECK_PX  = NAT_H - NAV_PX - PROG_PX
PAD_PX   = math.ceil(0.25 * PPI)          # 1/4" gutters + edge margins (never round DOWN
                                          # past the requirement)
TGT_W    = (NAT_W - 4 * PAD_PX) / 3
TGT_H    = NAV_PX - 2 * PAD_PX * 0.55

# the deck was authored for this box; S makes it fit the real one
DESIGN_ASPECT = 529 / 230                 # content height, in container widths
DECK_ASPECT   = DECK_PX / NAT_W
S             = DECK_ASPECT / DESIGN_ASPECT * A.fit

# ---- self-checks ----------------------------------------------------------
FAIL = []
def ok(label, cond, detail):
    print(f"  {'ok  ' if cond else 'FAIL'}  {label:<46} {detail}")
    if not cond: FAIL.append(label)

def arcmin(inches, ft):                   # visual angle subtended
    return math.degrees(2 * math.atan(inches / 2 / (ft * 12))) * 60

XH = 0.52                                 # Archivo x-height / em
def cap_in(cqw):                          # rendered cap height, inches
    return cqw * S * NAT_W / 100 / PPI

BULLET_IN = cap_in(6.7)                   # .blist li - read at touch distance
HEAD_IN   = cap_in(9.4)                   # .ccard h2  - read across the room
REACH_IN  = 30                            # you must stand this close to touch it

print(f"\npanel {A.panel}\" -> {PANEL_W:.3f} x {PANEL_H:.3f} in, {PPI:.1f} ppi, S = {S:.4f}\n")
ok("touch target >= 1.5 in", TGT_H / PPI >= 1.5, f"{TGT_H/PPI:.2f} in tall x {TGT_W/PPI:.2f} wide")
ok("dead space >= 1/4 in",   PAD_PX / PPI >= 0.25, f"{PAD_PX/PPI:.3f} in")
ok("nav under 12% of screen", NAV_PX / NAT_H < 0.12, f"{NAV_PX/NAT_H*100:.1f}%  ({NAV_PX} px)")
# Rick's bar is "readable at 3-6 ft". Touch splits that bar in two: you cannot
# reach a target from 6 ft, so the HEADLINE is what has to carry across the
# room and the BULLETS are read from where your hand already is. 16 arcmin is
# the comfortable-reading threshold; ~5 is bare legibility.
ok("headline carries at 6 ft", arcmin(HEAD_IN * XH, 6) >= 16,
   f"{arcmin(HEAD_IN*XH,6):.1f}' - cap {HEAD_IN:.2f} in")
ok("bullets comfortable at arm's length", arcmin(BULLET_IN * XH, REACH_IN/12) >= 16,
   f"{arcmin(BULLET_IN*XH,REACH_IN/12):.1f}' at {REACH_IN}\" - cap {BULLET_IN:.2f} in")
ok("bullets still legible at 6 ft", arcmin(BULLET_IN * XH, 6) >= 10,
   f"{arcmin(BULLET_IN*XH,6):.1f}' - below the 16' comfort line, see NOTE")
ok("deck + prog + nav = the panel", DECK_PX + PROG_PX + NAV_PX == NAT_H,
   f"{DECK_PX} + {PROG_PX} + {NAV_PX} = {NAT_H}")
ok("23 deck screens", _deck.N_CARDS == 23, f"{_deck.N_CARDS} cards")
ok("idle reset in the 60-90 s band", 60 <= A.idle <= 90, f"{A.idle} s")

# ---- scale the deck CSS ---------------------------------------------------
def rescale(css, s):
    """Collapse clamp(min, N cqw, max) -> N*s cqw, then scale every bare cqw."""
    css = re.sub(r'clamp\(\s*[^,()]+,\s*(-?[\d.]+)cqw\s*,\s*[^,()]+\)',
                 lambda m: f"{float(m.group(1))*s:.4g}cqwZ", css)
    css = re.sub(r'(?<![\w.])(-?[\d.]+)cqw(?!Z)',
                 lambda m: f"{float(m.group(1))*s:.4g}cqw", css)
    return css.replace("cqwZ", "cqw")

DECK_CSS = rescale(_deck.SCREEN_CSS, S)
assert "clamp(" not in DECK_CSS, "a clamp survived rescaling"
assert "cqwZ" not in DECK_CSS

# The launch screen. A kiosk-only card: the concept page has no emulator.
# The mock session is the real output format of this OS/32 image (2026-09-16).
EMU_CARD = r""",
  {cls:"ccard emu", html:`<div class="ek">Try it yourself</div>
    <h2>Step up and type</h2>
    <div class="emu-term"><div class="emu-tag">OS/32 &middot; live emulation</div><pre>*type hello.ftn
      PROGRAM HELLO
      TYPE *, 'HELLO FROM THE 3280'
      END
*forclg hello
HELLO        NO  ERROR(S)
 HELLO FROM THE 3280
*<span class="cur"></span></pre></div>
    <ul class="blist">
      <li>No mouse, no windows: <b>you type, it answers</b></li>
      <li>Real <b>OS/32</b>, the operating system this machine ran</li>
      <li>Three short lessons &mdash; one <b>writes and runs your own program</b></li>
    </ul>
    <a href="emulator.html" class="emu-launch">Step up and type &#8594;</a>
    <div class="emu-note">Fortran, Pascal and C compilers from the 1980s, on the 3280&rsquo;s ancestor architecture (SIMH Interdata 32). Nothing you type is permanent.</div>`}"""

CARDS_JS = _deck.CARDS_JS.rstrip()
assert CARDS_JS.endswith("];"), "deck did not end as expected"
CARDS_JS = CARDS_JS[:-2].rstrip()
if CARDS_JS.endswith(","):          # the deck's trailing comma + our leading one = an
    CARDS_JS = CARDS_JS[:-1]        # array hole = a blank screen before the emulator
CARDS_JS = CARDS_JS + EMU_CARD + "\n];"
assert not re.search(r"\},\s*,", CARDS_JS), "array hole in CARDS - a blank screen"

HTML = r"""<title>Concurrent 3280</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<style>
/*__FONTS__*/
/* The panel has one look. No theme switching - a museum exhibit is not a
   website, and the paper palette is matched to the cabinet it sits in. */
:root{
  --screen:#E9E2D0; --screen-ink:#282419; --screen-mut:#6f6753;
  --screen-accent:#123A6b; --screen-gold:#8f6413; --screen-line:#cdbf9f;
  --bar:#1B1915; --bar2:#262320; --bar-ink:#EFE8D8; --bar-mut:#8C8375;
  --bar-line:#3A352E; --hot:#D7A94E;
  --nav:__NAV__px; --pad:__PAD__px;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0;height:100%;width:100%;overflow:hidden;
  background:var(--bar);position:fixed;inset:0;
  -webkit-user-select:none;user-select:none;-webkit-touch-callout:none;
  -webkit-tap-highlight-color:transparent;touch-action:none;cursor:none}
body{display:flex;flex-direction:column;font-family:"Newsreader",Georgia,serif}

/*__DECK_CSS__*/

/* ---- the deck fills everything above the bar ---- */
/* emulator launch screen (kiosk-only). This block is NOT rescaled by S: the
   cqw values here are already at panel scale. */
.card .emu-term{position:relative;background:#000;color:#ffb838;border-radius:1.6cqw;padding:3.2cqw 3.4cqw 3cqw;margin:0 0 3.6cqw;
  box-shadow:0 1px 4px rgba(0,0,0,.25);border:1px solid #2a2417}
.card .emu-term pre{margin:0;font-family:"Space Mono",ui-monospace,monospace;font-size:2.75cqw;line-height:1.38;white-space:pre;overflow:hidden}
.card .emu-term .cur{display:inline-block;width:1.5cqw;height:2.8cqw;background:#ffb838;vertical-align:-0.4cqw;animation:blink 1.1s steps(2,jump-none) infinite}
.card .emu-tag{position:absolute;top:2.2cqw;right:3cqw;font-family:"Oswald",sans-serif;text-transform:uppercase;letter-spacing:.14em;font-size:1.7cqw;color:#8c805f}
.card.emu .blist li{font-size:4.2cqw;line-height:1.2}
.card .emu-launch{display:flex;align-items:center;justify-content:center;gap:3cqw;margin-top:auto;background:var(--screen-accent);color:#f4eede;text-decoration:none;padding:4.4cqw;border-radius:2cqw;font-family:"Archivo",sans-serif;font-weight:700;font-size:5cqw;letter-spacing:.01em}
.card .emu-note{font-size:2.5cqw;line-height:1.35;color:var(--screen-mut);font-style:italic;margin-top:2.6cqw}
.display{flex:1 1 auto;width:100%;min-height:0;background:var(--screen);
  color:var(--screen-ink);font-family:"Newsreader",Georgia,serif;line-height:1.55}

/* ---- progress: nine marks, so the visitor can see how long this is ---- */
.prog{flex:0 0 auto;display:flex;gap:4px;padding:0 var(--pad);background:var(--bar);
  height:__PROG__px;align-items:stretch}
.prog i{flex:1;background:var(--bar-line);border-radius:1px;transition:background .2s ease}
.prog i.seen{background:#5A5245} .prog i.now{background:var(--hot)}

/* ---- the bar: three targets where three switches used to be ---- */
.nav{flex:0 0 var(--nav);display:flex;gap:var(--pad);padding:calc(var(--pad)*.55) var(--pad);
  background:linear-gradient(to bottom,var(--bar2),var(--bar));
  border-top:2px solid var(--bar-line)}
.tgt{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;
  gap:.10em;border:2px solid var(--bar-line);border-radius:10px;background:#2E2A25;
  color:var(--bar-ink);font-family:"Oswald",sans-serif;padding:0;
  touch-action:manipulation;transition:none}
.tgt svg{width:__ICON__px;height:__ICON__px;fill:none;stroke:currentColor;
  stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}
.tgt .cap{font-size:__CAP__px;font-weight:600;text-transform:uppercase;letter-spacing:.14em}
.tgt.down{background:var(--hot);border-color:var(--hot);color:#1B1915}
.tgt[disabled]{opacity:.26}
.tgt.home{background:#25221E}
.tgt.home svg{fill:currentColor;stroke:none}

/* ---- attract: the screen has to say what it is from across the room ---- */
.attract{position:fixed;inset:0 0 var(--nav) 0;z-index:40;display:none;
  align-items:flex-end;justify-content:center;pointer-events:none;
  background:linear-gradient(to top,rgba(18,14,7,.92),rgba(18,14,7,0) 34%)}
body.idle .attract{display:flex}
.attract span{font-family:"Oswald",sans-serif;text-transform:uppercase;
  letter-spacing:.22em;font-weight:600;color:#F6DC8C;font-size:__ATTRACT__px;
  padding-bottom:__APAD__px;animation:pulse 2.4s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.34}}
@media (prefers-reduced-motion:reduce){
  .attract span{animation:none}
  .card{transition:none}
}

/* ---- bring-up diagnostics. Hold the top-left corner for 3 s. ---- */
#diag{position:fixed;top:0;left:0;z-index:90;display:none;max-width:78vw;
  background:rgba(10,9,7,.94);color:#9BE89B;border:1px solid #3A352E;
  font-family:"Space Mono",monospace;font-size:15px;line-height:1.7;padding:14px 18px;
  white-space:pre;pointer-events:none}
body.diag #diag{display:block}
#corner{position:fixed;top:0;left:0;width:110px;height:110px;z-index:91}
</style>

<div class="display" id="display"></div>
<div class="prog" id="prog"></div>
<nav class="nav">
  <button class="tgt back" id="tBack" aria-label="Back">
    <svg viewBox="0 0 24 24"><polyline points="15 5 8 12 15 19"/></svg><span class="cap">Back</span></button>
  <button class="tgt home" id="tHome" aria-label="Start over">
    <svg viewBox="0 0 24 24"><path d="M3 11.5 12 4l9 7.5V21a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/></svg><span class="cap">Start</span></button>
  <button class="tgt next" id="tNext" aria-label="Next">
    <svg viewBox="0 0 24 24"><polyline points="9 5 16 12 9 19"/></svg><span class="cap">Next</span></button>
</nav>
<div class="attract"><span>Touch to begin</span></div>
<div id="diag"></div><div id="corner"></div>

<script>
/*__CARDS__*/

const display=document.getElementById('display'), prog=document.getElementById('prog');
const nodes=CARDS.map(c=>{
  const el=document.createElement('div');
  el.className='card'+(c.cls?' '+c.cls:'');
  el.innerHTML=c.html;
  if(c.bg){el.style.backgroundImage=`url("${c.bg}")`;el.style.backgroundPosition=`center ${c.pos}`;}
  if(c.hl){const h=document.createElement('div');h.className='hl';
    h.style.top=c.hl.top;h.style.bottom=c.hl.bottom;el.appendChild(h);}
  display.appendChild(el);return el;
});
CARDS.forEach(()=>prog.appendChild(document.createElement('i')));
const marks=[...prog.children];
const tBack=document.getElementById('tBack'), tHome=document.getElementById('tHome'),
      tNext=document.getElementById('tNext');

let i=0;
function show(n){
  n=Math.max(0,Math.min(CARDS.length-1,n)); i=n;
  nodes.forEach((el,x)=>{el.classList.toggle('on',x===n);el.classList.toggle('prev',x<n);});
  marks.forEach((m,x)=>{m.classList.toggle('now',x===n);m.classList.toggle('seen',x<n);});
  tBack.disabled=(n===0); tNext.disabled=(n===CARDS.length-1);
}
function go(d){show(i+d);}

/* Feedback on pointerdown, not click - a kiosk must answer the finger in
   under 100 ms or the visitor presses again and skips a screen. */
function wire(btn,fn){
  btn.addEventListener('pointerdown',e=>{e.preventDefault();awake();
    if(btn.disabled)return; btn.classList.add('down');fn();},{passive:false});
  const up=()=>btn.classList.remove('down');
  btn.addEventListener('pointerup',up); btn.addEventListener('pointercancel',up);
  btn.addEventListener('pointerleave',up);
  btn.addEventListener('click',e=>e.preventDefault());
}
wire(tBack,()=>go(-1)); wire(tNext,()=>go(1)); wire(tHome,()=>show(0));

/* Idle: put it back on HOME so the next visitor starts at the start. */
const IDLE=__IDLE__*1000; let timer=null;
function idleExpired(){
  // a slide playing a video is its own attract loop - let it run until the
  // visitor navigates, rather than yanking back to Home mid-clip
  if(nodes[i] && nodes[i].querySelector('video')){ timer=setTimeout(idleExpired,IDLE); return; }
  show(0); document.body.classList.add('idle');
}
function awake(){
  document.body.classList.remove('idle');
  clearTimeout(timer);
  timer=setTimeout(idleExpired,IDLE);
}
['pointerdown','keydown'].forEach(ev=>document.addEventListener(ev,awake,{passive:true}));

/* Keys still work - a docent with a keyboard, and the buttons if we ever
   go back to switches. The app never needed to know which it was. */
document.addEventListener('keydown',e=>{
  if(e.key==='ArrowRight'||e.key==='PageDown')go(1);
  else if(e.key==='ArrowLeft'||e.key==='PageUp')go(-1);
  else if(e.key==='Home'){e.preventDefault();show(0);}
});

/* Lockdown: nothing here should behave like a web page. */
['contextmenu','dragstart','selectstart','gesturestart'].forEach(ev=>
  document.addEventListener(ev,e=>e.preventDefault()));
document.addEventListener('touchmove',e=>{if(e.touches.length>1)e.preventDefault();},{passive:false});
document.addEventListener('wheel',e=>{if(e.ctrlKey)e.preventDefault();},{passive:false});

/* Bring-up diagnostics. Hold the top-left corner 3 s. Answers Gate 2 -
   does this machine see the touch, and did it rotate with the screen. */
let hold=null, last='(none)';
const corner=document.getElementById('corner'), diag=document.getElementById('diag');
corner.addEventListener('pointerdown',()=>{hold=setTimeout(()=>{
  document.body.classList.toggle('diag');paint();},3000);});
['pointerup','pointerleave','pointercancel'].forEach(ev=>
  corner.addEventListener(ev,()=>clearTimeout(hold)));
document.addEventListener('pointerdown',e=>{
  last=`${e.pointerType} @ ${Math.round(e.clientX)},${Math.round(e.clientY)}`;
  if(document.body.classList.contains('diag'))paint();},{passive:true});
function paint(){
  const d=display.getBoundingClientRect();
  diag.textContent=
   `screen     ${screen.width} x ${screen.height}\n`+
   `viewport   ${innerWidth} x ${innerHeight}\n`+
   `deck box   ${Math.round(d.width)} x ${Math.round(d.height)}\n`+
   `dpr        ${devicePixelRatio}\n`+
   `orient     ${(screen.orientation||{}).type||'?'}\n`+
   `touch pts  ${navigator.maxTouchPoints}\n`+
   `coarse     ${matchMedia('(pointer:coarse)').matches}\n`+
   `last event ${last}\n`+
   `card       ${i+1} / ${CARDS.length}\n`+
   `scale S    __S__\n`+
   `built      __BUILT__`;
}

show(0); awake();
</script>
"""

ICON    = round(TGT_H * 0.30)
CAP     = round(TGT_H * 0.17)
ATTRACT = round(0.55 * PPI)

HTML = (HTML
    .replace("/*__FONTS__*/",   _deck.font_css())
    .replace("/*__DECK_CSS__*/", DECK_CSS)
    .replace("/*__CARDS__*/",    CARDS_JS)
    .replace("__NAV__",     str(NAV_PX))
    .replace("__PROG__",    str(PROG_PX))
    .replace("__PAD__",     str(PAD_PX))
    .replace("__ICON__",    str(ICON))
    .replace("__CAP__",     str(CAP))
    .replace("__ATTRACT__", str(ATTRACT))
    .replace("__APAD__",    str(round(0.45 * PPI)))
    .replace("__IDLE__",    str(A.idle))
    .replace("__S__",       f"{S:.4f}")
    .replace("__BUILT__",   f'{A.panel}" panel'))
HTML = _deck.inline(HTML)

out = _deck.HERE / "dist" / "kiosk" / "index.html"
out.parent.mkdir(parents=True, exist_ok=True)
assert "fonts.googleapis" not in HTML and "fonts.gstatic" not in HTML, \
    "a network font reference survived - the kiosk is offline"
assert "http://" not in HTML and "https://" not in HTML, \
    "the kiosk must not reference anything off the machine"
out.write_text(HTML, encoding="utf-8")
print(f"\nwrote {out}  ({out.stat().st_size/1024:.0f} KB)")
print(f"\nNOTE  bullets subtend {arcmin(BULLET_IN*XH,6):.1f}' at 6 ft against a 16' comfort\n"
      f"      threshold. Rick's spec said 3-6 ft; touch makes the far end moot for body\n"
      f"      copy but not for the headline. Cutting one bullet per screen would buy\n"
      f"      roughly {(1/(1-1/4.5)-1)*100:.0f}% more type. That is his call, not ours.")
if FAIL:
    print("\n*** " + str(len(FAIL)) + " CHECK(S) FAILED: " + ", ".join(FAIL) + " ***")
    sys.exit(1)
