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

/* NOAA NEXRAD footage window */
.vidbox{width:100%;aspect-ratio:4/3;background:#000;border-radius:2cqw;overflow:hidden;
  margin:1cqw 0 3.5cqw;box-shadow:0 1px 4px rgba(0,0,0,.25)}
.vidbox video{width:100%;height:100%;object-fit:cover;display:block}
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
    <div class="vidbox"><video src="nexrad-loop.mp4" poster="data:image/jpeg;base64,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" autoplay loop muted playsinline></video></div>
    <ul class="blist">
      <li>The <b>Doppler radar network</b> the Concurrent line helped pioneer</li>
      <li>Storms, aviation, defense &mdash; one system</li>
    </ul>
    <div class="morep">Footage: NOAA / National Weather Service &middot; public domain</div>`},

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

  // THE FULL TEAM — from Ken Yeager's letters. Cleared for public display by
  // Ruth Yeager 2026-09-15. De-naming standard honored (some colleagues unnamed).
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
    <div class="morep">Sourced from Ken Yeager&rsquo;s letters home, 1979&ndash;1989</div>`},

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
