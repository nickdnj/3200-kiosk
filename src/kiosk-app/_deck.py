#!/usr/bin/env python3
"""The deck — single source of truth for what the kiosk says and how a screen
looks. Two builders consume it:

  build-app.py    -> index.html      the concept-review page (cabinet + screen)
  build-kiosk.py  -> dist/kiosk/     the deployable 1080x1920 portrait kiosk

Content is docent-approved (Rick Lewis). Edit it HERE, nowhere else, and
rebuild both targets. Never hand-edit a generated index.html.
"""
import base64, mimetypes, pathlib

HERE = pathlib.Path(__file__).parent
A = HERE / "assets"

def uri(rel):
    p = A / rel
    mime = mimetypes.guess_type(p.name)[0] or "image/jpeg"
    b64 = base64.b64encode(p.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"

IMG = {
    "__SHELL__":    uri("renders/shell.jpg"),
    "__MACHINE__":  uri("renders/machine.jpg"),
    "__INTERIOR__": uri("renders/interior-open.jpg"),
    "__KIOSK__":    uri("renders/kiosk-concept.jpg"),
    "__RADAR__":    uri("renders/radar.jpg"),
    "__NJPLANT__":  uri("renders/njplant.jpg"),
    "__YEAGER__":   uri("renders/yeager.jpg"),
    "__R10000__":   uri("renders/r10000.jpg"),
    "__M_WEATHER__":uri("mont/weather.jpg"),
    "__M_SPACE__":  uri("mont/space.jpg"),
    "__M_DEFENSE__":uri("mont/defense.jpg"),
    "__M_FINANCE__":uri("mont/finance.jpg"),
    "__LOGO__":     uri("renders/vcf-logo.png"),
}

def inline(html):
    """Replace every __TOKEN__ with its base64 data URI."""
    for k, v in IMG.items():
        html = html.replace(k, v)
    return html

FAMILY = {"Archivo": "Archivo", "Newsreader": "Newsreader",
          "Oswald": "Oswald", "SpaceMono": "Space Mono"}

def font_css():
    """Self-hosted @font-face rules, woff2 inlined as data URIs.

    The kiosk has no network. Left on fonts.googleapis.com it would silently
    fall back to system faces in the field - different metrics, different line
    breaks, and every screen reflowed away from what was signed off. Latin
    subset only; the exhibit copy is English.
    """
    out = []
    for f in sorted((A / "fonts").glob("*.woff2")):
        stem, _, _ = f.stem.partition(".")
        fam, _, wt = stem.rpartition("-")
        italic = wt.endswith("i")
        b64 = base64.b64encode(f.read_bytes()).decode()
        out.append(
            "@font-face{font-family:'%s';font-style:%s;font-weight:%s;"
            "font-display:block;src:url(data:font/woff2;base64,%s) format('woff2')}"
            % (FAMILY[fam], "italic" if italic else "normal",
               wt.rstrip("i"), b64))
    if not out:
        raise SystemExit("no fonts in assets/fonts - run fetch-fonts.py")
    return "\n".join(out)

# ---- how a screen looks. Container-query units (cqw) throughout, so the deck
# ---- is resolution independent: it renders at 470 px in the concept page and
# ---- at 1080 px on the panel from the same numbers.
SCREEN_CSS = r""".display{position:relative;container-type:inline-size;overflow:hidden;
  background:var(--screen);color:var(--screen-ink);border-radius:2px;
  font-family:"Archivo",-apple-system,BlinkMacSystemFont,sans-serif}
.install .display{position:absolute;left:30.9%;top:19.2%;width:38.5%;height:41.7%;
  cursor:zoom-in;box-shadow:0 0 0 1px rgba(0,0,0,.12) inset}
.zoomtag{position:absolute;top:3.2cqw;right:3.2cqw;z-index:8;width:8.4cqw;height:8.4cqw;
  border-radius:50%;background:rgba(20,16,9,.5);display:grid;place-items:center;pointer-events:none}
.zoomtag svg{width:5cqw;height:5cqw;stroke:#f2ecda;stroke-width:2.2;fill:none;stroke-linecap:round}
.counter{position:absolute;right:4.5cqw;bottom:3.4cqw;font-family:"Space Mono",monospace;
  font-size:clamp(8px,3.1cqw,11px);color:var(--screen-mut);letter-spacing:.04em;z-index:6}

.card{position:absolute;inset:0;padding:6cqw 5.5cqw;display:flex;flex-direction:column;
  opacity:0;transform:translateX(4cqw);pointer-events:none;
  transition:opacity .34s ease,transform .34s ease}
.card.on{opacity:1;transform:none;pointer-events:auto}
.card.prev{transform:translateX(-4cqw)}
.card.img,.card.contain{padding:0}
.card.img img{width:100%;height:100%;object-fit:cover;display:block}
.card.contain{background:#e7e0cd}
.card.contain img{width:100%;height:100%;object-fit:contain;display:block}
.imgcap{position:absolute;left:0;right:0;bottom:0;padding:16cqw 5cqw 5.5cqw;z-index:5;
  background:linear-gradient(to top,rgba(12,9,3,.95),rgba(12,9,3,.6) 46%,rgba(12,9,3,0));color:#f3ecda}
.imgcap .k{font-family:"Oswald",sans-serif;text-transform:uppercase;letter-spacing:.11em;
  font-size:clamp(13px,6.4cqw,26px);font-weight:700;color:#f6dc8c;display:block;margin-bottom:2.4cqw;
  text-shadow:0 2px 8px rgba(0,0,0,.9),0 0 2px rgba(0,0,0,.7);line-height:1.02}
.imgcap p{margin:0;font-size:clamp(8px,3.7cqw,12px);line-height:1.35;text-shadow:0 1px 4px rgba(0,0,0,.8)} .imgcap b{color:#fff}
.hl{position:absolute;left:5%;right:5%;border:2px solid #d7a94e;border-radius:3px;
  box-shadow:0 0 0 2000px rgba(16,12,6,.4);z-index:3}

/* paginated tall content (posters fill the display, stepped vertically) */
.card.ppage{padding:0;background-size:100% auto;background-repeat:no-repeat;background-color:#e7e0cd}
.plabel{position:absolute;top:0;left:0;right:0;z-index:5;display:flex;justify-content:space-between;
  align-items:center;gap:2cqw;padding:3.2cqw 4cqw 7cqw;
  background:linear-gradient(to bottom,rgba(18,14,7,.82),rgba(18,14,7,0))}
.plabel .pn{font-family:"Oswald",sans-serif;text-transform:uppercase;letter-spacing:.13em;
  font-size:clamp(7px,3.2cqw,11px);font-weight:600;color:var(--gold)}
.plabel .pp{font-family:"Space Mono",monospace;font-size:clamp(7px,2.9cqw,10px);color:#e7dcc0}
.pintro{position:absolute;left:0;right:0;bottom:0;z-index:5;text-align:center;padding:8cqw 4cqw 4cqw;
  background:linear-gradient(to top,rgba(18,14,7,.85),rgba(18,14,7,0));
  font-family:"Oswald",sans-serif;text-transform:uppercase;letter-spacing:.11em;
  font-size:clamp(8px,3.4cqw,12px);color:#f3ecda}

.card .kick{font-family:"Oswald",sans-serif;text-transform:uppercase;letter-spacing:.18em;
  font-size:clamp(7px,3.2cqw,11px);font-weight:600;color:var(--screen-accent);margin-bottom:3cqw}
.card h2{font-family:"Newsreader",serif;font-weight:600;font-size:clamp(15px,7.6cqw,27px);
  line-height:1.05;letter-spacing:-.01em;margin:0 0 3cqw;text-wrap:balance}
.card p{margin:0 0 2.6cqw;font-size:clamp(9px,4.55cqw,15px);line-height:1.42;color:var(--screen-ink)}
.card .lede{font-size:clamp(10px,5cqw,16px)} .card .sub{color:var(--screen-mut);font-size:clamp(8px,4.1cqw,13px)}
.hero-title{margin-top:6cqw} .home-img{margin:4cqw 0;border-radius:2px;overflow:hidden;background:#ddd6c4}
.home-img img{width:100%;display:block;aspect-ratio:16/10;object-fit:cover}
.prompt{margin-top:auto;font-family:"Oswald",sans-serif;text-transform:uppercase;letter-spacing:.12em;
  font-size:clamp(8px,3.7cqw,12px);font-weight:600;color:var(--screen-accent);display:flex;align-items:center;gap:2cqw}
.prompt .dot{width:2.4cqw;height:2.4cqw;border-radius:50%;background:var(--screen-gold);
  animation:blink 1.6s steps(2,jump-none) infinite}
@keyframes blink{50%{opacity:.25}}

.stats{display:flex;border-top:1px solid var(--screen-line);border-bottom:1px solid var(--screen-line);margin:1cqw 0 3.5cqw}
.stats div{flex:1;padding:2.6cqw 1cqw;text-align:center;border-left:1px solid var(--screen-line)}
.stats div:first-child{border-left:0}
.stats .n{font-family:"Space Mono",monospace;font-weight:700;font-size:clamp(11px,5cqw,17px);color:var(--screen-ink);display:block}
.stats .l{font-family:"Oswald",sans-serif;text-transform:uppercase;letter-spacing:.06em;
  font-size:clamp(6px,2.5cqw,9px);color:var(--screen-mut);margin-top:1cqw;display:block}
.chain{display:flex;flex-wrap:wrap;gap:1.4cqw 1.8cqw;align-items:center;margin:1cqw 0 3.5cqw}
.chain span{font-family:"Oswald",sans-serif;font-size:clamp(7px,3.4cqw,11px);letter-spacing:.01em;
  background:#ddd4bd;color:var(--screen-ink);padding:1.2cqw 2.4cqw;border-radius:2px}
.chain span.hot{background:var(--screen-accent);color:#f2ecda}
.chain i{color:var(--screen-gold);font-style:normal;font-weight:700;font-size:3.6cqw}

.roster{display:flex;flex-direction:column;gap:2.6cqw;margin:1cqw 0 2cqw;padding:0}
.roster li{list-style:none;display:block;font-size:clamp(8px,4.1cqw,13px);line-height:1.28}
.roster .nm{font-family:"Oswald",sans-serif;font-weight:600;color:var(--screen-ink)}
.roster .rl{color:var(--screen-mut)}
.roster .cr{display:block;font-style:italic;color:#877c60;font-size:clamp(8px,3.8cqw,12px)}
.roster .dt{display:block;color:var(--screen-accent);font-size:clamp(8px,3.8cqw,12px)}
.morep{font-size:clamp(8px,3.7cqw,12px);color:var(--screen-mut);font-style:italic;margin-top:auto}

/* Rick's format: headline + graphic + a few big bullets */
.card.ccard{padding:6.5cqw 6cqw;gap:0;justify-content:flex-start}
.ccard .ek{font-family:"Oswald",sans-serif;text-transform:uppercase;letter-spacing:.16em;
  font-size:clamp(8px,3.5cqw,13px);font-weight:600;color:var(--screen-gold);margin-bottom:2cqw}
.ccard h2{font-family:"Archivo",sans-serif;font-weight:700;font-size:clamp(19px,9.4cqw,38px);
  line-height:1.03;letter-spacing:-.02em;margin:0 0 4cqw;text-wrap:balance}
.ccard h2 .h2sub{display:block;font-size:.56em;font-weight:600;color:var(--screen-mut);margin-top:1.4cqw}
.cimg{width:100%;aspect-ratio:16/10;border-radius:3px;overflow:hidden;background:#d9d1bd;margin:0 0 4.5cqw;
  box-shadow:0 1px 4px rgba(0,0,0,.18)}
.cimg img{width:100%;height:100%;object-fit:cover;display:block}
/* four-panel montage (the poster hero) */
.mont4{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:.8cqw;width:100%;
  aspect-ratio:4/3;border-radius:3px;overflow:hidden;background:#cbc2ac;margin:0 0 4.5cqw;
  box-shadow:0 1px 4px rgba(0,0,0,.18)}
.mp{position:relative;background-size:cover;background-position:center}
.mp .tag{position:absolute;left:1.6cqw;bottom:1.4cqw;font-family:"Oswald",sans-serif;text-transform:uppercase;
  letter-spacing:.09em;font-size:clamp(6px,2.7cqw,10px);font-weight:600;color:#fff;
  background:rgba(16,12,6,.62);padding:.5cqw 1.4cqw;border-radius:2px}
.cimcap{font-family:"Oswald",sans-serif;text-transform:uppercase;letter-spacing:.1em;font-weight:600;
  font-size:clamp(7px,3.1cqw,12px);color:var(--screen-mut);margin:-3cqw 0 4.5cqw}
.blist{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:3.6cqw}
.blist li{position:relative;padding-left:6cqw;font-size:clamp(14px,6.7cqw,27px);line-height:1.22;
  font-family:"Archivo",sans-serif;font-weight:500;color:var(--screen-ink)}
.blist li::before{content:"";position:absolute;left:0;top:.5em;width:2.8cqw;height:2.8cqw;
  background:var(--screen-accent);border-radius:1px;transform:rotate(45deg)}
.blist b{color:var(--screen-accent)}
/* animated NEXRAD-style Doppler scope - CSS only, loops forever */
.radar-wrap{display:flex;flex-direction:column;align-items:center;gap:3cqw;margin:1cqw 0 4cqw}
.radar{position:relative;width:70cqw;height:70cqw;border-radius:50%;
  background:radial-gradient(circle,#0a1f12 0%,#061308 70%,#041006 100%);
  border:2px solid #1c4a2c;overflow:hidden}
.radar::before{content:"";position:absolute;inset:0;border-radius:50%;
  background:repeating-radial-gradient(circle at 50% 50%,transparent 0,transparent calc(11.6cqw - 1px),rgba(60,180,110,.26) 11.6cqw)}
.radar::after{content:"";position:absolute;inset:0;border-radius:50%;transform-origin:50% 50%;
  background:conic-gradient(from 0deg,rgba(70,230,140,.55),rgba(70,230,140,.14) 24deg,transparent 64deg,transparent 360deg);
  animation:radar-sweep 4s linear infinite}
@keyframes radar-sweep{to{transform:rotate(360deg)}}
.radar .cx{position:absolute;background:rgba(60,180,110,.20)}
.radar .cx.h{left:0;right:0;top:50%;height:1px}
.radar .cx.v{top:0;bottom:0;left:50%;width:1px}
.radar .cell{position:absolute;border-radius:50%;filter:blur(.7cqw);animation:radar-cell 4s ease-in-out infinite}
@keyframes radar-cell{0%,100%{opacity:.32}45%{opacity:.95}}
.radar .c1{width:16cqw;height:12cqw;left:22%;top:28%;background:radial-gradient(circle,#ff5a3c,#ffb02e 45%,#3ad46a 80%,transparent);animation-delay:.3s}
.radar .c2{width:11cqw;height:9cqw;left:58%;top:55%;background:radial-gradient(circle,#ffb02e,#3ad46a 70%,transparent);animation-delay:2.1s}
.radar .c3{width:8cqw;height:8cqw;left:40%;top:67%;background:radial-gradient(circle,#3ad46a,transparent 75%);animation-delay:3s}
.radar-legend{display:flex;gap:3cqw;font-family:"Oswald",sans-serif;font-size:clamp(7px,2.9cqw,11px);text-transform:uppercase;letter-spacing:.1em;color:var(--screen-mut)}
.radar-legend b{color:#3aa564}
/* compact timeline for the lineage screen */
.tl{list-style:none;margin:1cqw 0 2cqw;padding:0;display:flex;flex-direction:column;gap:2.6cqw}
.tl li{display:flex;gap:3cqw;align-items:baseline;font-size:clamp(9px,4.2cqw,14px)}
.tl .yr{font-family:"Space Mono",monospace;font-weight:700;color:var(--screen-accent);flex:0 0 auto;min-width:12cqw}
.tl .ev{color:var(--screen-ink)} .tl .ev b{color:var(--screen-ink)}
.bignum{font-family:"Space Mono",monospace;font-weight:700;color:var(--screen-accent);
  font-size:clamp(30px,17cqw,66px);line-height:1;text-align:center;margin:2cqw 0 1cqw}
.bignum small{display:block;font-family:"Oswald",sans-serif;font-size:.22em;letter-spacing:.14em;
  text-transform:uppercase;color:var(--screen-mut);font-weight:600;margin-top:2cqw}
"""

# ---- what the screens say. Nine of them, in order.
CARDS_JS = r"""const CARDS = [
  // HOME &mdash; the whole story in one screen
  {cls:"ccard", html:`<div class="ek">The Concurrent 3280</div>
    <h2>This computer was made in New Jersey<span class="h2sub">Deployed everywhere &middot; 1981&ndash;1986</span></h2>
    <div class="mont4">
      <div class="mp" style="background-image:url('__M_WEATHER__')"><span class="tag">Weather</span></div>
      <div class="mp" style="background-image:url('__M_SPACE__');background-position:center 28%"><span class="tag">Space</span></div>
      <div class="mp" style="background-image:url('__M_DEFENSE__')"><span class="tag">Defense</span></div>
      <div class="mp" style="background-image:url('__M_FINANCE__');background-position:center 22%"><span class="tag">Finance</span></div>
    </div>
    <ul class="blist">
      <li>Designed in <b>Tinton Falls</b>, built in <b>Oceanport</b></li>
      <li>Ran <b>weather radar, spaceflight, defense &amp; Wall Street</b></li>
      <li>Its designers later shaped chips at <b>MIPS, IBM &amp; Sony</b></li>
    </ul>
    <div class="prompt"><span class="dot"></span> Press Next</div>`},

  // WHAT IT DID
  {cls:"ccard", html:`<div class="ek">What it did</div>
    <h2>One machine, many jobs</h2>
    <div class="cimg"><img src="__RADAR__" alt="Weather radar"></div>
    <ul class="blist">
      <li>Tracked storms on the <b>national weather radar</b></li>
      <li>Trained <b>NASA astronauts</b> for the Space Shuttle</li>
      <li>Ran the computers on <b>Wall Street</b></li>
    </ul>`},

  // POWER
  {cls:"ccard", html:`<div class="ek">What it did &middot; weather</div>
    <h2>The nation&rsquo;s storm radar</h2>
    <div class="radar-wrap">
      <div class="radar"><span class="cx h"></span><span class="cx v"></span>
        <span class="cell c1"></span><span class="cell c2"></span><span class="cell c3"></span></div>
      <div class="radar-legend"><span><b>NEXRAD</b> Doppler</span><span>plan&#8209;position scope</span></div>
    </div>
    <ul class="blist">
      <li>Concurrent machines processed the <b>national Doppler radar</b></li>
      <li>Raw echoes became the <b>storm maps</b> on the evening news</li>
    </ul>`},

  {cls:"ccard", html:`<div class="ek">Under the hood</div>
    <h2>Big iron, built by hand</h2>
    <div class="cimg"><img src="__INTERIOR__" alt="The 3280 circuit boards"></div>
    <ul class="blist">
      <li>Built for jobs <b>too big for any desktop</b></li>
      <li>Grew to <b>12 processors</b> working as one</li>
      <li>Every circuit board <b>wired by hand</b></li>
    </ul>`},

  // NEW JERSEY
  {cls:"ccard", html:`<div class="ek">Under the hood &middot; power</div>
    <h2>Twelve brains, one machine</h2>
    <div class="bignum">76.8<small>aggregate MIPS &middot; 1988</small></div>
    <ul class="blist">
      <li>Up to <b>12 processors</b> shared one memory</li>
      <li>Over the <b>S&#8209;Bus</b> &mdash; two data paths at once</li>
      <li>A design patented in <b>Ken Yeager&rsquo;s name</b>, 1986</li>
    </ul>`},

  {cls:"ccard", html:`<div class="ek">Where it was born</div>
    <h2>Made in Monmouth County</h2>
    <div class="cimg"><img src="__NJPLANT__" alt="Concurrent's New Jersey plant"></div>
    <ul class="blist">
      <li><b>Designed</b> in Tinton Falls</li>
      <li><b>Built</b> in Oceanport</li>
      <li><b>A few miles from this museum</b></li>
    </ul>`},

  // THE PEOPLE
  {cls:"ccard", html:`<div class="ek">Where it was born &middot; lineage</div>
    <h2>Sixty years, one New Jersey lab</h2>
    <ul class="tl">
      <li><span class="yr">1966</span><span class="ev"><b>Interdata</b> founded, Oceanport NJ</span></li>
      <li><span class="yr">1973</span><span class="ev"><b>Perkin&#8209;Elmer</b> buys it, moves to Tinton Falls</span></li>
      <li><span class="yr">1985</span><span class="ev"><b>Concurrent</b> spins off &mdash; same lab, same people</span></li>
      <li><span class="yr">1988</span><span class="ev">the <b>3280</b> ships &mdash; 12 CPUs, 76.8 MIPS</span></li>
      <li><span class="yr">1990s</span><span class="ev">the line pivots to <b>MIPS</b> chips</span></li>
    </ul>`},

  {cls:"ccard", html:`<div class="ek">Who built it</div>
    <h2>Built by a small team</h2>
    <div class="cimg"><img src="__YEAGER__" alt="Ken Yeager"></div>
    <div class="cimcap">Ken Yeager &middot; lead architect</div>
    <ul class="blist">
      <li>About <b>15 engineers</b>, in one New Jersey lab</li>
      <li>One later designed the chip inside the <b>PlayStation 3 &amp; Xbox 360</b></li>
      <li>Its lead architect went on to <b>SGI</b> &mdash; and his chip is <b>in this museum</b></li>
    </ul>`},

  // THE FULL TEAM — from Ken Yeager's letters. Build/test freely; the on-card
  // 'family approval pending' line MUST stay until Ruth Yeager clears it for public
  // display. De-naming standard honored (some colleagues deliberately unnamed).
  {cls:"ccard", html:`<div class="ek">The team &middot; from Ken Yeager&rsquo;s letters</div>
    <h2>Who built the 3280</h2>
    <ul class="roster">
      <li><span class="nm">Ken Yeager</span> &mdash; <span class="rl">Architect</span></li>
      <li><span class="nm">Hampton Sailor &amp; Rich Chirumbolo</span> &mdash; <span class="rl">Instruction fetch</span></li>
      <li><span class="nm">Tony Catanzaro</span> &mdash; <span class="rl">Address translation</span></li>
      <li><span class="nm">Brent Bush</span> &mdash; <span class="rl">Execution unit</span></li>
      <li><span class="nm">Walt Gan</span> &mdash; <span class="rl">Engineer</span></li>
      <li><span class="nm">Rocco Brescia</span> &mdash; <span class="rl">Senior engineer</span></li>
      <li><span class="nm">Jim Hodge</span> &mdash; <span class="rl">Barrel shifter</span></li>
      <li><span class="nm">Mike Martone</span> &mdash; <span class="rl">Built it &middot; OS bring-up</span></li>
      <li><span class="nm">Dan Masi</span> &mdash; <span class="rl">Engineer</span></li>
    </ul>
    <div class="morep">Names from Ken Yeager&rsquo;s letters &middot; family approval pending before public display</div>`},

  {cls:"ccard", html:`<div class="ek">A quiet first</div>
    <h2>The line that set Unix free</h2>
    <ul class="blist">
      <li>This machine&rsquo;s ancestor, the <b>Interdata</b>, ran the <b>first Unix</b> off DEC hardware</li>
      <li>Wollongong, Australia &mdash; <b>1977</b></li>
      <li>The <b>OS/32</b> you can type on here is that same family</li>
    </ul>`},

  // CROSS-LINK to the museum's SGI Onyx (Yeager's R10000)
  {cls:"ccard", html:`<div class="ek">Just down the room</div>
    <h2>Two machines, one designer</h2>
    <div class="cimg"><img src="__R10000__" alt="The MIPS R10000 processor"></div>
    <div class="cimcap">MIPS R10000</div>
    <ul class="blist">
      <li><b>Ken Yeager</b> architected this 3280 in New Jersey</li>
      <li>Then he designed the <b>MIPS R10000</b> chip at SGI</li>
      <li>It powers the <b>SGI Onyx</b> on display here &mdash; that chip sits on top of it</li>
    </ul>`},

  // OPEN THE CABINET
  {cls:"img", html:`<img src="__INTERIOR__" alt="The 3280 card cage, opened">
    <div class="imgcap"><span class="k">Open it up</span>
      <p>Hundreds of boards &mdash; every wire placed by hand.</p></div>`},

  {cls:"img", hl:{top:"20%",bottom:"48%"}, html:`<img src="__INTERIOR__" alt="Upper card cage">
    <div class="imgcap"><span class="k">The processor</span>
      <p>Up top: where the calculations happened.</p></div>`},

  {cls:"img", hl:{top:"62%",bottom:"6%"}, html:`<img src="__INTERIOR__" alt="Lower card cage">
    <div class="imgcap"><span class="k">Memory &amp; control</span>
      <p>Below: where the data lived.</p></div>`},
];"""

N_CARDS = CARDS_JS.count("{cls:")
