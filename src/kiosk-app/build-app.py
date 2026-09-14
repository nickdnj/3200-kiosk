#!/usr/bin/env python3
"""Build the Concurrent 3280 docent-kiosk concept-review app as a single
self-contained index.html. The live screen is composited into the full cabinet
render (a thumbnail); clicking the screen opens it full-size and readable."""
from _deck import HERE, IMG, SCREEN_CSS, CARDS_JS, inline

HTML = r"""<title>3280 Docent Kiosk</title>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Archivo:wght@500;600;700&family=Newsreader:ital,wght@0,400;0,500;0,600;1,400&family=Space+Mono:wght@400;700&display=swap">
<style>
:root{
  --bg:#ECE6DA; --bg2:#E3DBCB; --panel:#F7F3EA; --ink:#221F19; --muted:#6C6558;
  --line:#D8CFBE; --accent:#12305F; --accent2:#C0501C; --gold:#9C7529;
  --shadow:rgba(40,32,18,.24);
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --bg:#161513; --bg2:#0F0E0D; --panel:#201E1B; --ink:#ECE6D9; --muted:#9A9184;
    --line:#332F29; --accent:#7FA0DB; --accent2:#E2782F; --gold:#D7A94E;
    --shadow:rgba(0,0,0,.55);
  }
}
:root[data-theme="dark"]{
  --bg:#161513; --bg2:#0F0E0D; --panel:#201E1B; --ink:#ECE6D9; --muted:#9A9184;
  --line:#332F29; --accent:#7FA0DB; --accent2:#E2782F; --gold:#D7A94E;
  --shadow:rgba(0,0,0,.55);
}
/* live screen paper — matches render glass; constant in both themes */
:root{ --screen:#E9E2D0; --screen-ink:#282419; --screen-mut:#6f6753;
  --screen-accent:#123A6b; --screen-gold:#8f6413; --screen-line:#cdbf9f; }
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Newsreader",Georgia,serif;
  line-height:1.55;background-image:radial-gradient(120% 80% at 50% -12%,var(--bg) 0%,var(--bg2) 100%);
  min-height:100vh}
.wrap{max-width:1060px;margin:0 auto;padding:clamp(22px,5vw,52px) clamp(16px,4vw,40px) 72px}

.eyebrow{font-family:"Oswald",sans-serif;text-transform:uppercase;letter-spacing:.28em;
  font-size:12px;font-weight:600;color:var(--accent)}
.mast{border-bottom:1px solid var(--line);padding-bottom:24px;margin-bottom:clamp(24px,4vw,38px)}
.mast h1{font-family:"Newsreader",serif;font-weight:600;font-size:clamp(28px,5.6vw,50px);
  line-height:1.03;letter-spacing:-.015em;margin:.28em 0 .18em;text-wrap:balance}
.mast p.dek{margin:0;max-width:46ch;color:var(--muted);font-size:clamp(15px,2.1vw,18px)}

/* ---- the installation (thumbnail) ---- */
.stage{display:flex;flex-direction:column;align-items:center;gap:14px}
.install{position:relative;width:min(88vw,470px);aspect-ratio:598/1268;
  background:url("__SHELL__") center/100% 100% no-repeat;border-radius:6px;
  box-shadow:0 34px 74px -30px var(--shadow),0 12px 26px -18px var(--shadow);
  -webkit-user-select:none;user-select:none}

/* CONCEPT marker — this is the guiding-light concept, not the built piece.
   Kept on the cabinet render and the enlarged view so no screenshot loses it. */
.cbadge{position:absolute;z-index:20;top:10px;left:10px;pointer-events:none;
  font-family:"Oswald",sans-serif;font-weight:600;font-size:12px;letter-spacing:.22em;
  text-transform:uppercase;color:#f6dc8c;background:rgba(20,16,9,.72);
  border:1px solid rgba(246,220,140,.55);border-radius:3px;padding:5px 10px 4px;
  box-shadow:0 2px 10px -4px rgba(0,0,0,.6)}

/* base screen surface — shared by the inline thumbnail and the enlarged modal */
/*__SCREEN_CSS__*/
/* three real buttons — transparent hotspots over the drawn controls */
.hotbtn{position:absolute;width:9.8%;aspect-ratio:1;transform:translate(-50%,-50%);
  border:0;background:transparent;border-radius:50%;cursor:pointer;padding:0;z-index:7;
  -webkit-tap-highlight-color:transparent;transition:background .12s ease}
.hotbtn.back{left:36.1%;top:66.1%} .hotbtn.home{left:49.3%;top:66.1%} .hotbtn.next{left:62.4%;top:66.1%}
.hotbtn:active,.hotbtn.press{background:radial-gradient(circle at 50% 44%,rgba(255,255,255,.4),rgba(255,255,255,0) 66%)}
.hotbtn:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.hotbtn[disabled]{cursor:default;background:radial-gradient(circle,rgba(28,24,16,.42),rgba(28,24,16,.30) 70%)}
.hint{font-family:"Oswald",sans-serif;text-transform:uppercase;letter-spacing:.11em;font-size:11px;
  color:var(--muted);text-align:center;margin:2px 0 0} .hint b{color:var(--accent);font-weight:600}

/* ---- enlarged screen (modal) ---- */
.modal{position:fixed;inset:0;z-index:60;display:none;place-items:center;overflow:auto;
  padding:20px;background:rgba(14,11,7,.86);-webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px)}
.modal.open{display:grid}
.mclose{position:fixed;top:14px;right:16px;width:44px;height:44px;border-radius:50%;border:0;cursor:pointer;
  background:rgba(255,255,255,.15);color:#fff;font-size:22px;line-height:1;z-index:62}
.mclose:hover{background:rgba(255,255,255,.26)}
.kbig{position:relative;display:flex;flex-direction:column;align-items:center;gap:18px;margin:auto}
.kbig-screen{background:#26262a;padding:12px;border-radius:12px;
  box-shadow:0 40px 90px -24px rgba(0,0,0,.75),0 0 0 1px rgba(0,0,0,.4)}
.display.big{width:min(86vw,410px);aspect-ratio:230/529;border-radius:3px}
.mbuttons{display:flex;gap:min(9vw,40px)}
.mbtn{display:flex;flex-direction:column;align-items:center;gap:8px;background:none;border:0;
  cursor:pointer;font-family:"Oswald",sans-serif;padding:0;-webkit-tap-highlight-color:transparent}
.mbtn .disc{width:58px;height:58px;border-radius:50%;display:grid;place-items:center;
  background:radial-gradient(circle at 38% 30%,#3d3d43,#2b2b2f 62%,#161618);
  box-shadow:0 3px 0 #0c0c0d,0 7px 14px -5px rgba(0,0,0,.55),0 1px 1px rgba(255,255,255,.22) inset;
  transition:transform .08s ease,box-shadow .08s ease}
.mbtn svg{width:25px;height:25px;stroke:#f0ece2;stroke-width:2.4;fill:none;stroke-linecap:round;stroke-linejoin:round}
.mbtn.home svg{fill:#f0ece2;stroke:none}
.mbtn .cap{text-transform:uppercase;letter-spacing:.14em;font-size:11px;font-weight:600;color:#d8ccb0}
.mbtn:active .disc{transform:translateY(3px);box-shadow:0 0 0 #0c0c0d,0 2px 6px rgba(0,0,0,.5),0 1px 1px rgba(255,255,255,.2) inset}
.mbtn:focus-visible .disc{outline:3px solid #7FA0DB;outline-offset:3px}
.mbtn[disabled]{cursor:default} .mbtn[disabled] .disc{opacity:.4} .mbtn[disabled] .cap{opacity:.5}

/* ---- physical concept ---- */
.concept{margin-top:clamp(46px,8vw,84px);border-top:1px solid var(--line);padding-top:clamp(30px,5vw,44px)}
.concept .eyebrow{color:var(--accent2)}
.concept h2{font-family:"Newsreader",serif;font-weight:600;font-size:clamp(23px,4vw,34px);
  letter-spacing:-.01em;margin:.3em 0 .2em;text-wrap:balance}
.concept .dek{color:var(--muted);max-width:54ch;margin:0 0 26px}
.specs{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 30px}
.spec{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:12px 16px;flex:1;min-width:118px}
.spec .n{font-family:"Space Mono",monospace;font-weight:700;font-size:20px;color:var(--accent);display:block}
.spec .l{font-family:"Oswald",sans-serif;text-transform:uppercase;letter-spacing:.08em;font-size:10px;color:var(--muted);margin-top:4px;display:block}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:clamp(16px,3vw,26px)}
@media(max-width:720px){.grid2{grid-template-columns:1fr}}
figure{margin:0}
.shot{border-radius:10px;overflow:hidden;background:var(--panel);border:1px solid var(--line);box-shadow:0 18px 40px -26px var(--shadow)}
.shot img{width:100%;display:block}
figcaption{font-size:14px;color:var(--muted);margin-top:10px;line-height:1.45}
figcaption b{color:var(--ink);font-family:"Oswald",sans-serif;font-weight:600;text-transform:uppercase;letter-spacing:.06em;font-size:12px}
.feat{list-style:none;padding:0;margin:26px 0 0;display:grid;grid-template-columns:1fr 1fr;gap:2px 30px}
@media(max-width:620px){.feat{grid-template-columns:1fr}}
.feat li{padding:14px 0;border-top:1px solid var(--line);display:flex;gap:12px;align-items:baseline}
.feat .fn{font-family:"Space Mono",monospace;font-size:12px;color:var(--accent2);font-weight:700;flex:none}
.feat b{font-family:"Oswald",sans-serif;font-weight:600;text-transform:uppercase;letter-spacing:.05em;font-size:13px;display:block;margin-bottom:2px}
.feat p{margin:0;font-size:13.5px;color:var(--muted);line-height:1.45}

footer{margin-top:54px;border-top:1px solid var(--line);padding-top:22px;display:flex;gap:16px;
  align-items:center;justify-content:space-between;flex-wrap:wrap}
footer img{height:34px;width:auto;opacity:.9}
footer .note{font-size:12px;color:var(--muted);max-width:60ch;line-height:1.5}

@media (prefers-reduced-motion:reduce){.card{transition:none}.prompt .dot{animation:none}.hotbtn,.mbtn .disc{transition:none}}
</style>

<div class="wrap">
  <header class="mast">
    <div class="eyebrow">VCF Museum · Exhibit Concept Review</div>
    <h1>The 3280, told through its own front panel</h1>
    <p class="dek">The docent kiosk lives inside the Concurrent 3280 itself — one portrait screen where the
    door used to be, three real buttons, the card cage all around it. Tap the screen to read it full-size.</p>
  </header>

  <section class="stage" aria-label="Kiosk prototype in the 3280 cabinet">
    <div class="install">
      <div class="cbadge">Concept</div>
      <div class="display" id="display" role="button" tabindex="0" aria-label="Kiosk screen — activate to enlarge">
        <div class="zoomtag"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><line x1="16" y1="16" x2="21" y2="21"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg></div>
        <div class="counter" id="counter"></div>
      </div>
      <button class="hotbtn back" id="btnBack" aria-label="Back"></button>
      <button class="hotbtn home" id="btnHome" aria-label="Home"></button>
      <button class="hotbtn next" id="btnNext" aria-label="Next"></button>
    </div>
    <p class="hint">Tap the screen to enlarge · press <b>Back · Home · Next</b> · or use <b>← →</b> keys</p>
  </section>

  <section class="concept">
    <div class="eyebrow">The physical concept</div>
    <h2>A screen where the machine's door used to be</h2>
    <p class="dek">ChatGPT concept renders of the installed piece. A hinged, portrait display and three
    buttons; a docent swings it open to show the real card cage behind it.</p>

    <div class="specs">
      <div class="spec"><span class="n">23.0″</span><span class="l">Cabinet width</span></div>
      <div class="spec"><span class="n">69.5″</span><span class="l">Cabinet height</span></div>
      <div class="spec"><span class="n">9U + 9U</span><span class="l">Card cage bins</span></div>
      <div class="spec"><span class="n">3</span><span class="l">Buttons · no touch</span></div>
    </div>

    <div class="grid2">
      <figure>
        <div class="shot"><img src="__KIOSK__" alt="Concept render: the portrait kiosk door closed on the 3280 cabinet"></div>
        <figcaption><b>Door closed</b> — the kiosk screen sits in a hinged door, real boards framing it through the glass.</figcaption>
      </figure>
      <figure>
        <div class="shot"><img src="__INTERIOR__" alt="Concept render: the 3280 cabinet open, showing the 9U over 9U card cage"></div>
        <figcaption><b>Docent view</b> — swung open, the full 9U-over-9U card cage is exposed for a close look at the hand-wired boards.</figcaption>
      </figure>
    </div>

    <ul class="feat">
      <li><span class="fn">01</span><div><b>Hinged kiosk door</b><p>Swings open on left-side hinges so a docent can reveal the real boards behind it.</p></div></li>
      <li><span class="fn">02</span><div><b>Portrait display</b><p>Tall format suits placard text and the exhibit posters one screen at a time.</p></div></li>
      <li><span class="fn">03</span><div><b>Three buttons, no touch</b><p>Back · Home · Next only — nothing to smudge, nothing to explain, nothing to break.</p></div></li>
    </ul>
  </section>

  <footer>
    <img src="__LOGO__" alt="Vintage Computer Federation">
    <p class="note">Concept-review prototype. Cabinet imagery is AI concept art, not the final piece; on-screen
    copy uses the exhibit's verified facts. Screen content is an early draft — a few key points per screen, not the final wording.</p>
  </footer>
</div>

<!-- enlarged screen -->
<div class="modal" id="modal" aria-hidden="true">
  <button class="mclose" id="mclose" aria-label="Close">&times;</button>
  <div class="kbig" role="dialog" aria-modal="true" aria-label="Kiosk screen, enlarged">
    <div class="cbadge">Concept</div>
    <div class="kbig-screen"><div class="display big" id="mdisplay"><div class="counter" id="mcounter"></div></div></div>
    <div class="mbuttons">
      <button class="mbtn back" id="mBack" aria-label="Back">
        <span class="disc"><svg viewBox="0 0 24 24"><polyline points="15 5 8 12 15 19"/></svg></span><span class="cap">Back</span></button>
      <button class="mbtn home" id="mHome" aria-label="Home">
        <span class="disc"><svg viewBox="0 0 24 24"><path d="M3 11.5 12 4l9 7.5V21a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/></svg></span><span class="cap">Home</span></button>
      <button class="mbtn next" id="mNext" aria-label="Next">
        <span class="disc"><svg viewBox="0 0 24 24"><polyline points="9 5 16 12 9 19"/></svg></span><span class="cap">Next</span></button>
    </div>
  </div>
</div>

<script>
// Rick's format: each screen = one point, a graphic, 3–5 short bullets, big font.
/*__CARDS__*/

function buildInto(container){
  return CARDS.map(c=>{
    const el=document.createElement('div');
    el.className='card'+(c.cls?' '+c.cls:'');
    el.innerHTML=c.html;
    if(c.bg){el.style.backgroundImage=`url("${c.bg}")`;el.style.backgroundPosition=`center ${c.pos}`;}
    if(c.hl){const b=document.createElement('div');b.className='hl';b.style.top=c.hl.top;b.style.bottom=c.hl.bottom;el.appendChild(b);}
    container.appendChild(el);
    return el;
  });
}
const display=document.getElementById('display'), mdisplay=document.getElementById('mdisplay');
const counter=document.getElementById('counter'), mcounter=document.getElementById('mcounter');
const inlineNodes=buildInto(display), modalNodes=buildInto(mdisplay);
const backs=[document.getElementById('btnBack'),document.getElementById('mBack')];
const nexts=[document.getElementById('btnNext'),document.getElementById('mNext')];
const homes=[document.getElementById('btnHome'),document.getElementById('mHome')];

let i=0;
function paint(nodes,n){nodes.forEach((el,idx)=>{el.classList.toggle('on',idx===n);el.classList.toggle('prev',idx<n);});}
function show(n){
  n=Math.max(0,Math.min(CARDS.length-1,n)); i=n;
  paint(inlineNodes,n); paint(modalNodes,n);
  const t=(n+1)+' / '+CARDS.length; counter.textContent=t; mcounter.textContent=t;
  backs.forEach(b=>b.disabled=(n===0)); nexts.forEach(b=>b.disabled=(n===CARDS.length-1));
}
function tap(b){b.classList.add('press');setTimeout(()=>b.classList.remove('press'),120);}
function go(d){const n=i+d; if(n<0||n>CARDS.length-1)return; show(n);}
nexts.forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();tap(b);go(1);}));
backs.forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();tap(b);go(-1);}));
homes.forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();tap(b);show(0);}));

// enlarge / close
const modal=document.getElementById('modal');
function openModal(){modal.classList.add('open');modal.setAttribute('aria-hidden','false');}
function closeModal(){modal.classList.remove('open');modal.setAttribute('aria-hidden','true');}
display.addEventListener('click',openModal);
display.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();openModal();}});
document.getElementById('mclose').addEventListener('click',closeModal);
modal.addEventListener('click',e=>{if(e.target===modal)closeModal();});

document.addEventListener('keydown',e=>{
  if(e.key==='Escape'&&modal.classList.contains('open'))closeModal();
  else if(e.key==='ArrowRight')go(1);
  else if(e.key==='ArrowLeft')go(-1);
  else if(e.key==='Home'){e.preventDefault();show(0);}
});
show(0);
</script>
"""

HTML = HTML.replace("/*__SCREEN_CSS__*/", SCREEN_CSS + "\n")
HTML = HTML.replace("/*__CARDS__*/", CARDS_JS)
HTML = inline(HTML)

out = HERE / "index.html"
out.write_text(HTML, encoding="utf-8")
print(f"wrote {out}  ({out.stat().st_size/1024:.0f} KB)")
