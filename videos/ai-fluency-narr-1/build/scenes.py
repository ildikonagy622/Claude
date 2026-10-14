"""Generate compositions/broll-*.html — the ten back-to-back B-roll scenes of ai-fluency-narr-1.

Visual language = the script1-front inserts: thin off-white line art, Inter Tight labels, Bodoni Moda
italic accents, on the shared violet stage that lives in index.html. Every scene keeps its content in
y 160-1100 so the captions own the lower third.

Run from the project root:  python3 build/scenes.py
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cards import BROLL, DURATION  # noqa: E402

SPAN = {cid: (a, b) for cid, a, b in BROLL}


def icon(name, sw=1.3):
    raw = open(os.path.join(ROOT, "assets", "icons", f"{name}.svg"), encoding="utf-8").read()
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S).strip()
    head, rest = raw.split(">", 1)
    raw = re.sub(r'\s(class|width|height)="[^"]*"', "", head) + ">" + rest
    raw = raw.replace('stroke-width="2"', f'stroke-width="{sw}"')
    return re.sub(r"\s+", " ", raw)


def local(cid, **glob):
    """Global (output-timeline) seconds -> seconds inside the scene."""
    a, b = SPAN[cid]
    out = {k: round(v - a, 2) for k, v in glob.items()}
    out["end"] = round(b - a, 2)
    return out


COMMON_CSS = """
        @font-face {
          font-family: "Inter Tight";
          src: url("assets/fonts/InterTight-800.ttf") format("truetype");
          font-weight: 800;
          font-style: normal;
        }
        @font-face {
          font-family: "Inter Tight";
          src: url("assets/fonts/InterTight-700.ttf") format("truetype");
          font-weight: 700;
          font-style: normal;
        }
        @font-face {
          font-family: "Bodoni Moda";
          src: url("assets/fonts/BodoniModa-Italic-400.ttf") format("truetype");
          font-weight: 400;
          font-style: italic;
        }
        %S {
          position: absolute;
          inset: 0;
          overflow: hidden;
          color: #fffdf8;
          font-family: "Inter Tight", sans-serif;
        }
        %S .sc {
          position: absolute;
          left: 0;
          top: 0;
          width: 1080px;
          height: 1160px;
          transform-origin: 50% 45%;
        }
        %S .lbl {
          position: absolute;
          font-weight: 700;
          font-size: 30px;
          letter-spacing: 0.22em;
          text-transform: uppercase;
          opacity: 0.6;
          white-space: nowrap;
        }
        %S .serif {
          font-family: "Bodoni Moda", serif;
          font-style: italic;
          font-weight: 400;
        }
        %S .box {
          position: absolute;
          border: 2px solid rgba(255, 253, 248, 0.85);
          border-radius: 22px;
        }
        %S .bar {
          position: absolute;
          height: 12px;
          border-radius: 6px;
          background: rgba(255, 253, 248, 0.34);
          transform-origin: 0% 50%;
        }
        %S .ic svg {
          display: block;
          width: 100%;
          height: 100%;
        }
        %S svg.wires {
          position: absolute;
          left: 0;
          top: 0;
          width: 1080px;
          height: 1160px;
          overflow: visible;
        }
        %S svg.wires path,
        %S svg.wires line {
          fill: none;
          stroke: #fffdf8;
          stroke-width: 2;
          stroke-linecap: round;
        }
"""


def page(cid, css, body, js, last=False):
    T = SPAN[cid]
    dur = round(T[1] - T[0], 2)
    exit_js = (
        f'tl.to("#{cid} .sc", {{ opacity: 0, duration: 0.5, ease: "power1.in" }}, {dur - 0.5});'
        if last
        else f'tl.to("#{cid} .sc", {{ opacity: 0, y: -14, duration: 0.24, ease: "power1.in" }}, {dur - 0.24});'
    )
    return f"""<!doctype html>
<html lang="hu">
  <head>
    <meta charset="UTF-8" />
  </head>
  <body>
    <template>
      <style>{(COMMON_CSS + css).replace("%S", "#" + cid)}      </style>

      <div id="{cid}" data-composition-id="{cid}" data-width="1080" data-height="1920">
        <div class="sc">
{body}
        </div>
      </div>

      <script>
        (function () {{
          const ROOT = "#{cid} ";
          const $ = (s) => document.querySelector(ROOT + s);
          const $$ = (s) => Array.from(document.querySelectorAll(ROOT + s));
          // Prime every drawable stroke so a 0 -> 1 "draw" is a dashoffset tween.
          $$("svg.wires .draw").forEach((p) => {{
            const len = p.getTotalLength();
            p.style.strokeDasharray = len + " " + len;
            p.style.strokeDashoffset = len;
          }});
          const draw = (sel, at, dur, ease) =>
            tl.to(ROOT + sel, {{ strokeDashoffset: 0, duration: dur, ease: ease || "power2.inOut" }}, at);
          const tl = gsap.timeline({{ paused: true }});
          tl.fromTo(ROOT + ".sc", {{ opacity: 0, y: 18 }}, {{ opacity: 1, y: 0, duration: 0.38, ease: "power2.out" }}, 0);
          tl.fromTo(ROOT + ".sc", {{ scale: 1 }}, {{ scale: 1.03, duration: {dur}, ease: "none" }}, 0);
{js}
          {exit_js}
          window.__timelines["{cid}"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
"""


SCENES = {}

# ---------------------------------------------------------------- shared tool / task board
TOOLS = ["ChatGPT", "Gemini", "Claude", "Perplexity", "Gemini Notebook"]
TASKS = ["ötletek", "kampány", "szöveg", "kutatás", "összefoglaló"]
ROW_Y = [300, 450, 600, 750, 900]  # row centres
CHIP_L, CHIP_R, DOT_X = 80, 470, 676

BOARD_CSS = """
        %S .chip {
          position: absolute;
          left: 80px;
          width: 390px;
          height: 96px;
          margin-top: -48px;
          border: 2px solid rgba(255, 253, 248, 0.9);
          border-radius: 48px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: 800;
          font-size: 44px;
          letter-spacing: -0.035em;
          white-space: nowrap;
        }
        %S .task {
          position: absolute;
          left: 664px;
          height: 80px;
          margin-top: -40px;
          display: flex;
          align-items: center;
          gap: 26px;
          white-space: nowrap;
        }
        %S .task i {
          width: 24px;
          height: 24px;
          border-radius: 50%;
          border: 2px solid #fffdf8;
          background: #150f2a;
          flex: none;
        }
        %S .task span {
          font-family: "Bodoni Moda", serif;
          font-style: italic;
          font-size: 58px;
          line-height: 1;
          margin-top: -6px;
        }
"""


def board_body(cid, wires):
    rows = []
    for i, (tool, task) in enumerate(zip(TOOLS, TASKS)):
        rows.append(f'          <div class="chip" id="{cid}-t{i}" style="top: {ROW_Y[i]}px">{tool}</div>')
        rows.append(f'          <div class="task" id="{cid}-k{i}" style="top: {ROW_Y[i]}px"><i></i><span>{task}</span></div>')
    paths = []
    for n, (i, j) in enumerate(wires):
        y1, y2 = ROW_Y[i], ROW_Y[j]
        paths.append(
            f'            <path class="draw w{n}" d="M{CHIP_R + 4},{y1} C{CHIP_R + 110},{y1} {DOT_X - 110},{y2} {DOT_X - 2},{y2}" />'
        )
    return (
        '          <div class="lbl" style="left: 84px; top: 170px">Eszköz</div>\n'
        '          <div class="lbl" style="left: 668px; top: 170px">Feladat</div>\n'
        '          <svg class="wires" viewBox="0 0 1080 1160">\n' + "\n".join(paths) + "\n          </svg>\n" + "\n".join(rows)
    )


# 1. broll-match — every tool wired to several tasks: a tangle, then a big question mark.
cid = "broll-match"
T = local(cid, users=1.11, melyik=1.96, ai=2.56, mire=3.11)
TANGLE = [(0, 2), (0, 4), (1, 0), (1, 3), (2, 4), (2, 1), (3, 0), (3, 2), (4, 1), (4, 3), (0, 3), (2, 0)]
SCENES[cid] = page(
    cid,
    BOARD_CSS
    + """
        %S svg.wires path {
          stroke-width: 1.6;
          opacity: 0.4;
        }
        %S .q {
          position: absolute;
          left: 0;
          width: 1080px;
          top: 360px;
          text-align: center;
          font-size: 400px;
          line-height: 1;
          text-shadow: 0 0 60px rgba(11, 10, 16, 0.9), 0 0 120px rgba(21, 15, 42, 0.9);
        }
""",
    board_body(cid, TANGLE) + '\n          <div class="q serif" id="broll-match-q">?</div>',
    f"""          const T = {json.dumps(T)};
          for (let i = 0; i < 5; i++) {{
            tl.fromTo("#{cid}-t" + i, {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }}, 0.1 + i * 0.12);
            tl.fromTo("#{cid}-k" + i, {{ opacity: 0, x: 30 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }}, 0.5 + i * 0.12);
          }}
          for (let n = 0; n < {len(TANGLE)}; n++) draw("svg.wires .w" + n, 1.0 + n * 0.11, 0.7);
          // "melyik AI-eszközt": the chips flicker through, nobody knows which one.
          for (let i = 0; i < 5; i++) {{
            tl.to("#{cid}-t" + i, {{ opacity: 0.35, duration: 0.12, yoyo: true, repeat: 1, ease: "none" }}, T.melyik + i * 0.16);
          }}
          tl.to(ROOT + ".chip, " + ROOT + ".task, " + ROOT + "svg.wires", {{ opacity: 0.32, duration: 0.4, ease: "power1.out" }}, T.mire - 0.05);
          tl.fromTo("#broll-match-q", {{ opacity: 0, scale: 1.12, filter: "blur(10px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.6, ease: "power3.out" }}, T.mire);""",
)

# 6. broll-tools — the payoff: the same board, each tool wired cleanly to the one task it suits.
cid = "broll-tools"
T = local(cid, chat=18.53, gemini=19.22, claude=19.83, perplexity=20.37, notebook=21.36, tasks=23.54, use=24.18, work=25.09)
CLEAN = [(i, i) for i in range(5)]
SCENES[cid] = page(
    cid,
    BOARD_CSS
    + """
        %S .task.on i {
          background: #fffdf8;
        }
""",
    board_body(cid, CLEAN),
    f"""          const T = {json.dumps(T)};
          const AT = [T.chat, T.gemini, T.claude, T.perplexity, T.notebook];
          tl.fromTo(ROOT + ".lbl", {{ opacity: 0 }}, {{ opacity: 0.6, duration: 0.4 }}, 0.1);
          AT.forEach((at, i) => {{
            tl.fromTo("#{cid}-t" + i, {{ opacity: 0, x: -36, scale: 0.96 }}, {{ opacity: 1, x: 0, scale: 1, duration: 0.5, ease: "power3.out" }}, at - 0.04);
          }});
          for (let i = 0; i < 5; i++) {{
            tl.fromTo("#{cid}-k" + i, {{ opacity: 0, x: 30 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }}, T.tasks - 0.05 + i * 0.1);
            draw("svg.wires .w" + i, T.use - 0.1 + i * 0.16, 0.6);
            tl.fromTo("#{cid}-k" + i + " i", {{ backgroundColor: "#150f2a" }}, {{ backgroundColor: "#fffdf8", duration: 0.25 }}, T.use + 0.45 + i * 0.16);
          }}""",
)

# 2. broll-doc — a full page collapses into a three-point summary.
cid = "broll-doc"
T = local(cid, keszit=5.61, doc=6.28, sum=6.94)
doc_bars = "\n".join(
    f'            <div class="bar dl" style="left: 44px; top: {92 + k * 34}px; width: {w}px"></div>'
    for k, w in enumerate([300, 330, 270, 320, 210, 330, 300, 250, 320, 290, 160, 310, 280, 200])
)
sum_rows = "\n".join(
    f'            <div class="srow" style="top: {96 + k * 74}px"><i></i><div class="bar" style="position: relative; width: {w}px; background: rgba(255, 253, 248, 0.85)"></div></div>'
    for k, w in enumerate([190, 150, 175])
)
SCENES[cid] = page(
    cid,
    """
        %S .doc {
          left: 110px;
          top: 300px;
          width: 420px;
          height: 600px;
          overflow: hidden;
        }
        %S .scan {
          position: absolute;
          left: 0;
          right: 0;
          top: 0;
          height: 3px;
          background: #fffdf8;
          box-shadow: 0 0 24px 6px rgba(255, 253, 248, 0.35);
          opacity: 0;
        }
        %S .sum {
          left: 670px;
          top: 440px;
          width: 300px;
          height: 330px;
          transform-origin: 0% 50%;
        }
        %S .srow {
          position: absolute;
          left: 36px;
          display: flex;
          align-items: center;
          gap: 18px;
        }
        %S .srow i {
          width: 16px;
          height: 16px;
          border-radius: 50%;
          background: #fffdf8;
          flex: none;
        }
        %S .doc .ic {
          position: absolute;
          left: 40px;
          top: 30px;
          width: 44px;
          height: 44px;
          opacity: 0.8;
        }
""",
    f"""          <div class="lbl" style="left: 114px; top: 246px">Dokumentum</div>
          <div class="box doc" id="broll-doc-page">
            <div class="ic">{icon("file-text", 1.6)}</div>
{doc_bars}
            <div class="scan" id="broll-doc-scan"></div>
          </div>
          <svg class="wires" viewBox="0 0 1080 1160">
            <path class="draw arrow" d="M560,605 L640,605" />
            <path class="draw arrow" d="M622,587 L642,605 L622,623" />
          </svg>
          <div class="lbl" id="broll-doc-sl" style="left: 674px; top: 386px">Összefoglaló</div>
          <div class="box sum" id="broll-doc-sum">
{sum_rows}
          </div>""",
    f"""          const T = {json.dumps(T)};
          tl.fromTo("#broll-doc-page", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, 0.05);
          tl.fromTo(ROOT + ".dl", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.4, ease: "power2.out", stagger: 0.05 }}, 0.3);
          tl.fromTo("#broll-doc-scan", {{ opacity: 0, y: 0 }}, {{ opacity: 1, duration: 0.1 }}, T.doc);
          tl.to("#broll-doc-scan", {{ y: 596, duration: 0.65, ease: "power1.inOut" }}, T.doc);
          tl.to("#broll-doc-scan", {{ opacity: 0, duration: 0.15 }}, T.doc + 0.6);
          tl.to(ROOT + ".dl", {{ opacity: 0.45, duration: 0.4 }}, T.sum);
          draw("svg.wires .arrow", T.sum - 0.1, 0.35);
          tl.fromTo("#broll-doc-sum", {{ opacity: 0, scale: 0.9, x: -20 }}, {{ opacity: 1, scale: 1, x: 0, duration: 0.5, ease: "power3.out" }}, T.sum);
          tl.fromTo("#broll-doc-sl", {{ opacity: 0 }}, {{ opacity: 0.6, duration: 0.4 }}, T.sum + 0.05);
          tl.fromTo(ROOT + ".srow", {{ opacity: 0, x: -14 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power2.out", stagger: 0.1 }}, T.sum + 0.08);""",
)

# 3. broll-campaign — a four-week campaign plan fills in.
cid = "broll-campaign"
T = local(cid, hasznal=7.98, ai=8.87, kampany=9.21, terv=9.77)
ROWS = [("Ötlet", 0, 1.2), ("Szöveg", 0.8, 2.2), ("Vizuál", 1.5, 3.1), ("Indulás", 3.2, 3.95)]
COL0, COLW = 330, 160  # x of week 1, width of one week
gantt = []
for k in range(4):
    gantt.append(f'          <div class="wk" style="left: {COL0 + k * COLW}px">{k + 1}. hét</div>')
    gantt.append(f'          <div class="vl" style="left: {COL0 + k * COLW}px"></div>')
gantt.append(f'          <div class="vl" style="left: {COL0 + 4 * COLW}px"></div>')
for r, (name, a, b) in enumerate(ROWS):
    y = 480 + r * 130
    gantt.append(f'          <div class="rn" style="top: {y}px">{name}</div>')
    gantt.append(
        f'          <div class="gb" style="top: {y}px; left: {COL0 + a * COLW + 8}px; width: {(b - a) * COLW - 16}px"></div>'
    )
SCENES[cid] = page(
    cid,
    """
        %S .head {
          position: absolute;
          left: 110px;
          top: 250px;
          display: flex;
          align-items: center;
          gap: 26px;
        }
        %S .head .ic {
          width: 84px;
          height: 84px;
        }
        %S .head span {
          font-size: 96px;
          line-height: 1;
        }
        %S .wk {
          position: absolute;
          top: 400px;
          width: 160px;
          text-align: center;
          font-weight: 700;
          font-size: 26px;
          letter-spacing: 0.18em;
          text-transform: uppercase;
          opacity: 0.55;
        }
        %S .vl {
          position: absolute;
          top: 450px;
          width: 0;
          height: 540px;
          border-left: 1.5px dashed rgba(255, 253, 248, 0.22);
          transform-origin: 50% 0%;
        }
        %S .rn {
          position: absolute;
          left: 110px;
          height: 72px;
          margin-top: 4px;
          display: flex;
          align-items: center;
          font-weight: 800;
          font-size: 44px;
          letter-spacing: -0.03em;
        }
        %S .gb {
          position: absolute;
          height: 80px;
          border: 2px solid rgba(255, 253, 248, 0.9);
          border-radius: 40px;
          background: rgba(255, 253, 248, 0.1);
          transform-origin: 0% 50%;
        }
        %S .ph {
          position: absolute;
          top: 440px;
          width: 2px;
          height: 560px;
          background: #fffdf8;
          box-shadow: 0 0 18px 2px rgba(255, 253, 248, 0.4);
          left: 330px;
          opacity: 0;
        }
""",
    f"""          <div class="head" id="broll-campaign-head"><div class="ic">{icon("megaphone", 1.3)}</div><span class="serif">kampányterv</span></div>
{chr(10).join(gantt)}
          <div class="ph" id="broll-campaign-ph"></div>""",
    f"""          const T = {json.dumps(T)};
          tl.fromTo("#broll-campaign-head", {{ opacity: 0, x: -24 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }}, 0.05);
          tl.fromTo(ROOT + ".wk", {{ opacity: 0, y: 10 }}, {{ opacity: 0.55, y: 0, duration: 0.35, stagger: 0.08 }}, 0.25);
          tl.fromTo(ROOT + ".vl", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.6, ease: "power2.out", stagger: 0.06 }}, 0.3);
          tl.fromTo(ROOT + ".rn", {{ opacity: 0, x: -16 }}, {{ opacity: 1, x: 0, duration: 0.35, stagger: 0.1 }}, T.ai - 0.1);
          tl.fromTo(ROOT + ".gb", {{ scaleX: 0, opacity: 0 }}, {{ scaleX: 1, opacity: 1, duration: 0.55, ease: "power3.out", stagger: 0.22 }}, T.kampany);
          tl.fromTo("#broll-campaign-ph", {{ opacity: 0, x: 0 }}, {{ opacity: 0.9, duration: 0.2 }}, T.terv);
          tl.to("#broll-campaign-ph", {{ x: 640, duration: T.end - T.terv - 0.3, ease: "power1.inOut" }}, T.terv);""",
)

# 4. broll-rewrite — the text is rewritten, but its style signature carries over.
cid = "broll-rewrite"
T = local(cid, dolgoz=11.58, szoveg=12.48, megmarad=13.98, eredeti=14.76, stilus=15.18)


def text_card(n, top, label, widths):
    bars = "\n".join(
        f'            <div class="bar b{n}" style="left: 250px; top: {70 + k * 44}px; width: {w}px"></div>'
        for k, w in enumerate(widths)
    )
    return f"""          <div class="lbl" id="broll-rewrite-l{n}" style="left: 114px; top: {top - 54}px">{label}</div>
          <div class="box card" id="broll-rewrite-c{n}" style="top: {top}px">
            <div class="aa serif" id="broll-rewrite-aa{n}">Aa</div>
{bars}
          </div>"""


SCENES[cid] = page(
    cid,
    """
        %S .card {
          left: 110px;
          width: 860px;
          height: 300px;
        }
        %S .aa {
          position: absolute;
          left: 44px;
          top: 58px;
          font-size: 150px;
          line-height: 1;
        }
        %S .pen {
          position: absolute;
          width: 72px;
          height: 72px;
          left: 0;
          top: 0;
          opacity: 0;
        }
        %S .tag {
          position: absolute;
          left: 600px;
          top: 1000px;
          height: 72px;
          padding: 0 30px;
          border: 2px solid rgba(255, 253, 248, 0.9);
          border-radius: 36px;
          display: flex;
          align-items: center;
          gap: 14px;
          font-weight: 800;
          font-size: 36px;
          letter-spacing: -0.02em;
        }
        %S .tag .ic {
          width: 40px;
          height: 40px;
        }
""",
    text_card(1, 270, "Eredeti", [540, 590, 480, 570, 330])
    + "\n"
    + text_card(2, 680, "Átdolgozott", [560, 430, 590, 520, 380])
    + f"""
          <svg class="wires" viewBox="0 0 1080 1160">
            <path class="draw link" d="M150,480 C20,560 20,620 150,700" stroke-dasharray="6 10" />
          </svg>
          <div class="pen ic" id="broll-rewrite-pen">{icon("pen-line", 1.3)}</div>
          <div class="tag" id="broll-rewrite-tag"><div class="ic">{icon("check", 1.6)}</div>stílus</div>""",
    f"""          const T = {json.dumps(T)};
          tl.fromTo("#broll-rewrite-c1, #broll-rewrite-l1", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, 0.05);
          tl.fromTo(ROOT + ".b1", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.4, stagger: 0.06 }}, 0.2);
          // The pen runs over the original lines ("dolgoztassunk át").
          tl.set("#broll-rewrite-pen", {{ x: 350, y: 300, opacity: 0 }}, 0);
          tl.to("#broll-rewrite-pen", {{ opacity: 1, duration: 0.2 }}, T.dolgoz);
          tl.to("#broll-rewrite-pen", {{ keyframes: [{{ x: 900, y: 300 }}, {{ x: 380, y: 384 }}, {{ x: 900, y: 384 }}, {{ x: 380, y: 468 }}, {{ x: 760, y: 468 }}], duration: 1.3, ease: "none" }}, T.dolgoz);
          tl.to("#broll-rewrite-pen", {{ opacity: 0, duration: 0.2 }}, T.dolgoz + 1.3);
          tl.fromTo("#broll-rewrite-c2, #broll-rewrite-l2", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, T.szoveg);
          tl.fromTo(ROOT + ".b2", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.4, stagger: 0.07 }}, T.szoveg + 0.2);
          tl.set("#broll-rewrite-aa2", {{ opacity: 0 }}, 0);
          // "megmaradjon": the style mark travels from the original into the rewrite.
          draw("svg.wires .link", T.megmarad - 0.1, 0.5);
          tl.fromTo("#broll-rewrite-aa2", {{ opacity: 0, y: -60, filter: "blur(6px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.6, ease: "power3.out" }}, T.megmarad + 0.1);
          tl.to("#broll-rewrite-aa1", {{ opacity: 0.55, duration: 0.4 }}, T.megmarad + 0.1);
          tl.fromTo("#broll-rewrite-tag", {{ opacity: 0, scale: 0.9 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "power3.out" }}, T.stilus - 0.05);""",
)

# 5. broll-brand — the course title.
cid = "broll-brand"
T = local(cid, ai=16.15, kepzes=16.84, megtud=17.45)
SCENES[cid] = page(
    cid,
    """
        %S .win {
          left: 130px;
          top: 330px;
          width: 820px;
          height: 600px;
        }
        %S .dots {
          position: absolute;
          left: 34px;
          top: 30px;
          display: flex;
          gap: 12px;
        }
        %S .dots i {
          width: 14px;
          height: 14px;
          border-radius: 50%;
          border: 2px solid rgba(255, 253, 248, 0.7);
        }
        %S .pill {
          position: absolute;
          right: 30px;
          top: 20px;
          height: 40px;
          padding: 0 18px;
          border: 2px solid rgba(255, 253, 248, 0.7);
          border-radius: 20px;
          display: flex;
          align-items: center;
          gap: 10px;
          font-weight: 700;
          font-size: 22px;
          letter-spacing: 0.18em;
        }
        %S .pill b {
          width: 10px;
          height: 10px;
          border-radius: 50%;
          background: #fffdf8;
        }
        %S .topline {
          position: absolute;
          left: 0;
          right: 0;
          top: 80px;
          border-top: 2px solid rgba(255, 253, 248, 0.35);
        }
        %S .title {
          position: absolute;
          left: 0;
          right: 0;
          top: 190px;
          text-align: center;
          font-size: 176px;
          line-height: 1;
          letter-spacing: -0.02em;
          white-space: nowrap;
        }
        %S .rule {
          position: absolute;
          left: 250px;
          right: 250px;
          top: 430px;
          border-top: 2px solid rgba(255, 253, 248, 0.7);
        }
        %S .sub {
          position: absolute;
          left: 0;
          right: 0;
          top: 470px;
          text-align: center;
          font-weight: 700;
          font-size: 28px;
          letter-spacing: 0.26em;
          opacity: 0.7;
        }
        %S .spark {
          position: absolute;
          left: 638px;
          top: 150px;
          width: 64px;
          height: 64px;
        }
""",
    f"""          <div class="box win" id="broll-brand-win">
            <div class="dots"><i></i><i></i><i></i></div>
            <div class="pill"><b></b>ÉLŐ</div>
            <div class="topline"></div>
            <div class="title serif" id="broll-brand-title">AI fluency</div>
            <div class="spark ic" id="broll-brand-spark">{icon("sparkles", 1.3)}</div>
            <div class="rule" id="broll-brand-rule"></div>
            <div class="sub" id="broll-brand-sub">ONLINE KÉPZÉS</div>
          </div>""",
    f"""          const T = {json.dumps(T)};
          tl.fromTo("#broll-brand-win", {{ opacity: 0, scale: 0.96 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }}, 0.02);
          tl.fromTo("#broll-brand-title", {{ opacity: 0, y: 14, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.6, ease: "power3.out" }}, T.ai - 0.02);
          tl.fromTo("#broll-brand-spark", {{ opacity: 0, scale: 0.6, rotation: -20 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.5, ease: "power3.out" }}, T.ai + 0.35);
          tl.fromTo("#broll-brand-rule", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.5, ease: "power2.out" }}, T.kepzes);
          tl.fromTo("#broll-brand-sub", {{ opacity: 0, y: 8 }}, {{ opacity: 0.7, y: 0, duration: 0.4 }}, T.kepzes + 0.15);""",
)

# 7. broll-flow — brief -> AI -> result -> check, travelling down a rail.
cid = "broll-flow"
T = local(cid, gyak=26.04, pontos=26.81, kiadas=27.22, folyamat=28.05, eredmeny=28.82, ellenor=29.53)
NODES = [("message-circle", "feladat"), ("sparkles", "AI"), ("file-text", "eredmény"), ("circle-check", "ellenőrzés")]
NODE_Y = [270, 480, 690, 900]
nodes = "\n".join(
    f'          <div class="node" id="broll-flow-n{k}" style="top: {NODE_Y[k]}px"><div class="ring ic">{icon(ic, 1.3)}</div>'
    f'<div class="nl"><b>0{k + 1}</b><span class="serif">{name}</span></div></div>'
    for k, (ic, name) in enumerate(NODES)
)
SCENES[cid] = page(
    cid,
    """
        %S .node {
          position: absolute;
          left: 250px;
          height: 140px;
          margin-top: -70px;
          display: flex;
          align-items: center;
          gap: 44px;
        }
        %S .ring {
          width: 140px;
          height: 140px;
          border-radius: 50%;
          border: 2px solid rgba(255, 253, 248, 0.9);
          background: #150f2a;
          padding: 34px;
          flex: none;
        }
        %S .nl {
          display: flex;
          flex-direction: column;
          gap: 6px;
        }
        %S .nl b {
          font-weight: 700;
          font-size: 26px;
          letter-spacing: 0.22em;
          opacity: 0.55;
        }
        %S .nl span {
          font-size: 84px;
          line-height: 0.9;
          white-space: nowrap;
        }
        %S .pulse {
          position: absolute;
          left: 308px;
          top: 262px;
          width: 24px;
          height: 24px;
          border-radius: 50%;
          background: #fffdf8;
          box-shadow: 0 0 22px 6px rgba(255, 253, 248, 0.45);
          opacity: 0;
        }
""",
    f"""          <svg class="wires" viewBox="0 0 1080 1160">
            <path class="draw rail" d="M320,270 L320,900" style="opacity: 0.45" />
          </svg>
          <div class="pulse" id="broll-flow-pulse"></div>
{nodes}""",
    f"""          const T = {json.dumps(T)};
          const AT = [T.gyak + 0.1, T.kiadas, T.eredmeny, T.ellenor];
          draw("svg.wires .rail", 0.1, T.ellenor - 0.2, "none");
          AT.forEach((at, k) => {{
            tl.fromTo("#broll-flow-n" + k + " .ring", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.6)" }}, at - 0.05);
            tl.fromTo("#broll-flow-n" + k + " .nl", {{ opacity: 0, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }}, at);
          }});
          tl.fromTo("#broll-flow-pulse", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, T.kiadas - 0.4);
          tl.to("#broll-flow-pulse", {{ y: 210, duration: T.kiadas - (T.kiadas - 0.4), ease: "power2.inOut" }}, T.kiadas - 0.4);
          tl.to("#broll-flow-pulse", {{ y: 420, duration: T.eredmeny - T.folyamat, ease: "power2.inOut" }}, T.folyamat);
          tl.to("#broll-flow-pulse", {{ y: 630, duration: T.ellenor - T.eredmeny, ease: "power2.inOut" }}, T.eredmeny);
          tl.to("#broll-flow-pulse", {{ opacity: 0, duration: 0.2 }}, T.ellenor);
          tl.to("#broll-flow-n3 .ring", {{ backgroundColor: "rgba(255, 253, 248, 0.16)", duration: 0.4 }}, T.ellenor + 0.2);""",
)

# 8. broll-split — what you hand to the AI vs. what stays with you.
cid = "broll-split"
T = local(cid, kiadni=31.68, ainak=32.09, jobb=33.39, nalad=33.87)
LEFT = ["vázlat", "összefoglaló", "ötletelés"]
RIGHT = ["döntés", "bizalmas adat", "végső hang"]
items = []
for k, w in enumerate(LEFT):
    items.append(f'          <div class="it il" style="left: 110px; top: {450 + k * 150}px">{w}</div>')
for k, w in enumerate(RIGHT):
    items.append(f'          <div class="it ir" style="left: 590px; top: {450 + k * 150}px">{w}</div>')
SCENES[cid] = page(
    cid,
    """
        %S .colh {
          position: absolute;
          top: 250px;
          display: flex;
          align-items: center;
          gap: 22px;
        }
        %S .colh .ic {
          width: 76px;
          height: 76px;
        }
        %S .colh span {
          font-size: 92px;
          line-height: 1;
          white-space: nowrap;
        }
        %S .div {
          position: absolute;
          left: 539px;
          top: 240px;
          width: 2px;
          height: 760px;
          background: rgba(255, 253, 248, 0.35);
          transform-origin: 50% 0%;
        }
        %S .it {
          position: absolute;
          width: 380px;
          height: 104px;
          border: 2px solid rgba(255, 253, 248, 0.88);
          border-radius: 52px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: 800;
          font-size: 44px;
          letter-spacing: -0.03em;
          white-space: nowrap;
        }
        %S .ir {
          background: rgba(255, 253, 248, 0.1);
        }
""",
    f"""          <div class="colh" id="broll-split-hl" style="left: 110px"><div class="ic">{icon("sparkles", 1.3)}</div><span class="serif">AI-nak</span></div>
          <div class="colh" id="broll-split-hr" style="left: 590px"><div class="ic">{icon("user-round", 1.3)}</div><span class="serif">nálad</span></div>
          <div class="div" id="broll-split-div"></div>
{chr(10).join(items)}""",
    f"""          const T = {json.dumps(T)};
          tl.fromTo("#broll-split-div", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.8, ease: "power2.out" }}, 0.1);
          tl.fromTo("#broll-split-hl", {{ opacity: 0, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }}, T.kiadni - 0.1);
          tl.fromTo(ROOT + ".il", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "power3.out", stagger: 0.16 }}, T.ainak - 0.1);
          tl.fromTo("#broll-split-hr", {{ opacity: 0, x: 20 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }}, T.jobb);
          tl.fromTo(ROOT + ".ir", {{ opacity: 0, x: 30 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "power3.out", stagger: 0.16 }}, T.nalad - 0.05);""",
)

# 9. broll-verify — a magnifier checks the lines; then sources feed the research.
cid = "broll-verify"
T = local(cid, kiprob=35.10, kulonb=35.91, ellenor=36.47, es=37.15, kutat=37.27, tech=37.77)
vbars = "\n".join(
    f'            <div class="bar vb" style="left: 44px; top: {60 + k * 52}px; width: {w}px"></div>'
    f'<div class="ck ic" style="left: {64 + w}px; top: {44 + k * 52}px">{icon("check", 1.8)}</div>'
    for k, w in enumerate([560, 480, 620, 430])
)
srcs = "\n".join(
    f'          <div class="box src" style="left: {x}px"><div class="bar" style="left: 26px; top: 30px; width: 120px; background: rgba(255, 253, 248, 0.7)"></div>'
    f'<div class="bar" style="left: 26px; top: 60px; width: 160px"></div><div class="bar" style="left: 26px; top: 90px; width: 90px"></div></div>'
    for x in (110, 420, 730)
)
SCENES[cid] = page(
    cid,
    """
        %S .vcard {
          left: 110px;
          top: 290px;
          width: 860px;
          height: 290px;
        }
        %S .ck {
          position: absolute;
          width: 44px;
          height: 44px;
        }
        %S .mag {
          position: absolute;
          left: 0;
          top: 0;
          width: 150px;
          height: 150px;
          opacity: 0;
        }
        %S .src {
          top: 830px;
          width: 240px;
          height: 140px;
        }
""",
    f"""          <div class="lbl" id="broll-verify-l1" style="left: 114px; top: 236px">Ellenőrzés</div>
          <div class="box vcard" id="broll-verify-card">
{vbars}
          </div>
          <div class="mag ic" id="broll-verify-mag">{icon("search", 1.3)}</div>
          <div class="lbl" id="broll-verify-l2" style="left: 114px; top: 760px">Kutatás</div>
          <svg class="wires" viewBox="0 0 1080 1160">
            <path class="draw sw" d="M230,830 C230,720 540,700 540,582" />
            <path class="draw sw" d="M540,830 L540,582" />
            <path class="draw sw" d="M850,830 C850,720 540,700 540,582" />
          </svg>
{srcs}""",
    f"""          const T = {json.dumps(T)};
          tl.fromTo("#broll-verify-card, #broll-verify-l1", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, 0.05);
          tl.fromTo(ROOT + ".vb", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.4, stagger: 0.07 }}, 0.2);
          tl.set(ROOT + ".ck", {{ opacity: 0 }}, 0);
          tl.set("#broll-verify-mag", {{ x: 140, y: 300 }}, 0);
          tl.to("#broll-verify-mag", {{ opacity: 1, duration: 0.25 }}, T.kiprob);
          tl.to("#broll-verify-mag", {{ keyframes: [{{ x: 640, y: 300 }}, {{ x: 200, y: 352 }}, {{ x: 760, y: 404 }}, {{ x: 560, y: 456 }}], duration: T.ellenor - T.kiprob + 0.1, ease: "none" }}, T.kiprob);
          tl.to("#broll-verify-mag", {{ opacity: 0, duration: 0.25 }}, T.ellenor + 0.1);
          tl.fromTo(ROOT + ".ck", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)", stagger: 0.14 }}, T.ellenor);
          tl.fromTo("#broll-verify-l2", {{ opacity: 0 }}, {{ opacity: 0.6, duration: 0.4 }}, T.kutat - 0.1);
          tl.fromTo(ROOT + ".src", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out", stagger: 0.12 }}, T.kutat);
          for (let k = 0; k < 3; k++) draw("svg.wires .sw:nth-of-type(" + (k + 1) + ")", T.tech - 0.1 + k * 0.1, 0.5);""",
)

# 10. broll-sessions — three live sessions, six hours.
cid = "broll-sessions"
T = local(cid, kepzes=39.11, harom=39.56, elo=39.92, alkalom=40.14, osszesen=41.18, hat=41.76, ora=41.99)
tiles = "\n".join(
    f'          <div class="box tile" id="broll-sessions-t{k}" style="left: {110 + k * 300}px">'
    f'<div class="live"><b></b>ÉLŐ</div><div class="num serif">0{k + 1}</div><div class="hr">2 óra</div></div>'
    for k in range(3)
)
segs = "\n".join(
    f'          <div class="seg" style="left: {110 + k * 290}px"><div class="fill" id="broll-sessions-f{k}"></div></div>' for k in range(3)
)
SCENES[cid] = page(
    cid,
    """
        %S .tile {
          top: 290px;
          width: 260px;
          height: 330px;
        }
        %S .live {
          position: absolute;
          left: 28px;
          top: 26px;
          display: flex;
          align-items: center;
          gap: 10px;
          font-weight: 700;
          font-size: 22px;
          letter-spacing: 0.2em;
          opacity: 0.75;
        }
        %S .live b {
          width: 10px;
          height: 10px;
          border-radius: 50%;
          background: #fffdf8;
        }
        %S .num {
          position: absolute;
          left: 0;
          right: 0;
          top: 90px;
          text-align: center;
          font-size: 150px;
          line-height: 1;
        }
        %S .hr {
          position: absolute;
          left: 0;
          right: 0;
          bottom: 30px;
          text-align: center;
          font-weight: 800;
          font-size: 36px;
          letter-spacing: -0.02em;
          opacity: 0.85;
        }
        %S .seg {
          position: absolute;
          top: 700px;
          width: 280px;
          height: 16px;
          border-radius: 8px;
          border: 2px solid rgba(255, 253, 248, 0.6);
          overflow: hidden;
        }
        %S .fill {
          position: absolute;
          inset: 0;
          background: #fffdf8;
          transform-origin: 0% 50%;
          transform: scaleX(0);
        }
        %S .total {
          position: absolute;
          left: 0;
          right: 0;
          top: 780px;
          display: flex;
          justify-content: center;
          align-items: baseline;
          gap: 26px;
        }
        %S .total .big {
          font-size: 260px;
          line-height: 0.8;
        }
        %S .total .unit {
          font-weight: 800;
          font-size: 92px;
          letter-spacing: -0.045em;
        }
""",
    f"""{tiles}
{segs}
          <div class="total" id="broll-sessions-total"><span class="big serif" id="broll-sessions-n">0</span><span class="unit">óra</span></div>""",
    f"""          const T = {json.dumps(T)};
          [T.harom, T.harom + 0.18, T.elo].forEach((at, k) => {{
            tl.fromTo("#broll-sessions-t" + k, {{ opacity: 0, y: 30, scale: 0.95 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "power3.out" }}, at - 0.05);
          }});
          tl.fromTo(ROOT + ".seg", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, stagger: 0.08 }}, T.alkalom);
          tl.fromTo("#broll-sessions-total", {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, T.osszesen);
          // Hours count 0 -> 6 as the three bars fill; driven by timeline time so any seek is exact.
          const n = document.getElementById("broll-sessions-n");
          const counter = {{ v: 0 }};
          tl.fromTo(counter, {{ v: 0 }}, {{ v: 6, duration: T.hat - T.osszesen + 0.25, ease: "power1.inOut", onUpdate() {{ n.textContent = String(Math.round(counter.v)); }} }}, T.osszesen);
          for (let k = 0; k < 3; k++) {{
            tl.fromTo("#broll-sessions-f" + k, {{ scaleX: 0 }}, {{ scaleX: 1, duration: (T.hat - T.osszesen + 0.25) / 3, ease: "none" }}, T.osszesen + k * (T.hat - T.osszesen + 0.25) / 3);
          }}
          tl.fromTo("#broll-sessions-n", {{ scale: 1.08 }}, {{ scale: 1, duration: 0.4, ease: "power3.out" }}, T.hat + 0.25);""",
)

# 11. broll-cta — closing card on its own page, set in the caption typography.
cid = "broll-cta"
SCENES[cid] = page(
    cid,
    """
        %S .cta {
          position: absolute;
          left: 60px;
          right: 60px;
          top: 700px;
          display: flex;
          flex-direction: column;
          align-items: center;
          text-align: center;
          text-shadow: 0 2px 22px rgba(12, 8, 20, 0.28);
        }
        %S .cta .ic {
          width: 108px;
          height: 108px;
          margin-bottom: 44px;
          filter: drop-shadow(0 2px 14px rgba(12, 8, 20, 0.3));
        }
        %S .cm {
          font-weight: 800;
          font-size: 94px;
          line-height: 0.9;
          letter-spacing: -0.045em;
          white-space: nowrap;
        }
        %S .ce {
          font-size: 136px;
          line-height: 0.82;
          letter-spacing: -0.025em;
          margin: -0.06em 0 -0.02em;
          white-space: nowrap;
        }
        %S .ul {
          width: 520px;
          margin-top: 54px;
          border-top: 2px solid rgba(255, 253, 248, 0.7);
          transform-origin: 50% 50%;
        }
""",
    f"""          <div class="cta">
            <div class="ic" id="broll-cta-ico">{icon("mouse-pointer-click", 1.3)}</div>
            <div class="cm" id="broll-cta-m1">Kattints és</div>
            <div class="cm" id="broll-cta-m2">nézd meg</div>
            <div class="ce serif" id="broll-cta-e">a részleteket!</div>
            <div class="ul" id="broll-cta-ul"></div>
          </div>""",
    """          tl.fromTo("#broll-cta-m1", { opacity: 0, scale: 0.97, y: 8 }, { opacity: 1, scale: 1, y: 0, duration: 0.32, ease: "power2.out" }, 0.12);
          tl.fromTo("#broll-cta-m2", { opacity: 0, scale: 0.97, y: 8 }, { opacity: 1, scale: 1, y: 0, duration: 0.32, ease: "power2.out" }, 0.3);
          tl.fromTo("#broll-cta-e", { opacity: 0, scale: 1.06, y: 10, filter: "blur(6px)" }, { opacity: 1, scale: 1, y: 0, filter: "blur(0px)", duration: 0.5, ease: "power3.out" }, 0.55);
          tl.fromTo("#broll-cta-ico", { opacity: 0, scale: 0.82, rotation: -10 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.55, ease: "power3.out" }, 0.85);
          tl.fromTo("#broll-cta-ul", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power2.out" }, 1.0);
          // A soft "click" pulse on the pointer once everything has landed.
          tl.to("#broll-cta-ico", { scale: 0.9, duration: 0.12, ease: "power1.in", yoyo: true, repeat: 1 }, 1.7);""",
    last=True,
)

for cid, html_text in SCENES.items():
    with open(os.path.join(ROOT, "compositions", f"{cid}.html"), "w", encoding="utf-8") as f:
        f.write(html_text)
assert set(SCENES) == set(SPAN), set(SPAN) ^ set(SCENES)
print(f"wrote {len(SCENES)} B-roll scenes, {DURATION}s")
