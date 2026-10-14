"""Generate index.html + compositions/captions.html for script1-front from cards.py.

Run from the project root:  python3 build/gen.py
"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cards import CARDS, CUTS, DURATION  # noqa: E402

LEAD = 0.06  # a card appears this much before its first spoken word
MAX_HOLD = 2.2  # a card never lingers longer than this after its last line lands

FONT_FACES = """      @font-face {
        font-family: "Inter Tight";
        src: url("{p}assets/fonts/InterTight-800.ttf") format("truetype");
        font-weight: 800;
        font-style: normal;
      }
      @font-face {
        font-family: "Bodoni Moda";
        src: url("{p}assets/fonts/BodoniModa-Italic-400.ttf") format("truetype");
        font-weight: 400;
        font-style: italic;
      }"""

cards = []
for i, lines in enumerate(CARDS):
    start = max(0.0, lines[0][2] - LEAD)
    if i + 1 < len(CARDS):
        end = min(CARDS[i + 1][0][2] - LEAD, lines[-1][2] + MAX_HOLD)
    else:
        end = DURATION
    cards.append({"start": round(start, 2), "end": round(end, 2), "lines": lines})

card_html = []
for i, c in enumerate(cards):
    rows = []
    for j, (kind, text, _t) in enumerate(c["lines"]):
        cls = "ln-m" if kind == "m" else "ln-e"
        rows.append(f'          <div class="ln {cls}" id="cap-c{i}l{j}"><span>{html.escape(text)}</span></div>')
    card_html.append(
        f'        <div class="cap-inner clip" id="cap-c{i}" data-start="{c["start"]}" '
        f'data-duration="{round(c["end"] - c["start"], 2)}" data-track-index="0">\n'
        + "\n".join(rows)
        + "\n        </div>"
    )

timing = [
    {
        "id": f"cap-c{i}",
        "start": c["start"],
        "end": c["end"],
        "lines": [{"id": f"cap-c{i}l{j}", "kind": k, "t": t} for j, (k, _x, t) in enumerate(c["lines"])],
    }
    for i, c in enumerate(cards)
]

captions = f"""<!doctype html>
<html lang="hu">
  <head>
    <meta charset="UTF-8" />
  </head>
  <body>
    <template>
      <style>
{FONT_FACES.replace("{p}", "")}
        #captions {{
          position: absolute;
          inset: 0;
          pointer-events: none;
        }}
        .cap-inner {{
          position: absolute;
          left: 60px;
          right: 60px;
          top: 1180px;
          display: flex;
          flex-direction: column;
          align-items: center;
          text-align: center;
          color: #fffdf8;
          text-shadow: 0 2px 22px rgba(12, 8, 20, 0.28);
        }}
        .ln {{
          display: block;
          width: 100%;
          white-space: nowrap;
          transform-origin: 50% 60%;
        }}
        .ln > span {{
          display: inline-block;
        }}
        .ln-m {{
          font-family: "Inter Tight", sans-serif;
          font-weight: 800;
          font-size: 94px;
          line-height: 0.9;
          letter-spacing: -0.045em;
        }}
        .ln-e {{
          font-family: "Bodoni Moda", serif;
          font-style: italic;
          font-weight: 400;
          font-size: 136px;
          line-height: 0.82;
          letter-spacing: -0.025em;
          margin: -0.06em 0 -0.02em;
        }}
      </style>

      <div id="captions" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(card_html)}
      </div>

      <script>
        (function () {{
          const CARDS = {json.dumps(timing)};
          const MAX_W = 960;

          function fitLines() {{
            document.querySelectorAll("#captions .ln > span").forEach((span) => {{
              const w = span.getBoundingClientRect().width;
              if (w > MAX_W) {{
                const ln = span.parentElement;
                const size = parseFloat(getComputedStyle(ln).fontSize);
                ln.style.fontSize = (size * MAX_W) / w + "px";
              }}
            }});
          }}

          function build() {{
            fitLines();
            const tl = gsap.timeline({{ paused: true }});
            CARDS.forEach((c) => {{
              c.lines.forEach((l) => {{
                const el = "#" + l.id;
                const at = Math.max(c.start, l.t - 0.04);
                if (l.kind === "e") {{
                  tl.fromTo(
                    el,
                    {{ opacity: 0, scale: 1.06, y: 10, filter: "blur(6px)" }},
                    {{ opacity: 1, scale: 1, y: 0, filter: "blur(0px)", duration: 0.5, ease: "power3.out" }},
                    at
                  );
                }} else {{
                  tl.fromTo(
                    el,
                    {{ opacity: 0, scale: 0.97, y: 8 }},
                    {{ opacity: 1, scale: 1, y: 0, duration: 0.32, ease: "power2.out" }},
                    at
                  );
                }}
              }});
              // Exit: fade every line of the card together just before the next card.
              tl.to(
                c.lines.map((l) => "#" + l.id),
                {{ opacity: 0, duration: 0.16, ease: "power1.in" }},
                Math.max(c.start + 0.3, c.end - 0.16)
              );
            }});
            window.__timelines["captions"] = tl;
          }}

          if (document.fonts && document.fonts.ready) {{
            document.fonts.ready.then(build);
          }} else {{
            build();
          }}
        }})();
      </script>
    </template>
  </body>
</html>
"""

index = f"""<!doctype html>
<html lang="hu">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
{FONT_FACES.replace("{p}", "")}
      * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }}
      html,
      body {{
        margin: 0;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #0b0a10;
      }}
      #root {{
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: #0b0a10;
      }}
      #cam {{
        position: absolute;
        inset: 0;
        transform-origin: 50% 32%;
      }}
      #aroll {{
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
      }}
      /* Soft low-frame shade so the off-white type holds on the light shirt. Not a caption box. */
      #shade {{
        position: absolute;
        inset: 0;
        pointer-events: none;
        background: linear-gradient(
          180deg,
          rgba(10, 8, 16, 0) 38%,
          rgba(10, 8, 16, 0.22) 58%,
          rgba(10, 8, 16, 0.3) 72%,
          rgba(10, 8, 16, 0.12) 100%
        );
      }}
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-duration="{DURATION}"
      data-width="1080"
      data-height="1920"
    >
      <div id="cam">
        <video
          id="aroll"
          class="clip"
          src="assets/video/cut.mp4"
          data-has-audio="true"
          data-start="0"
          data-duration="{DURATION}"
          data-track-index="0"
          data-volume="1"
          playsinline
        ></video>
      </div>
      <div id="shade"></div>
      <div
        id="captions"
        data-composition-id="captions"
        data-composition-src="compositions/captions.html"
        data-track-kind="captions"
        data-start="0"
        data-duration="{DURATION}"
        data-track-index="2"
        data-width="1080"
        data-height="1920"
      ></div>
    </div>
    <script>
      const CUTS = {json.dumps(CUTS)};
      const DURATION = {DURATION};
      const tl = gsap.timeline({{ paused: true }});

      // Camera: a slow push-in inside every cut, reset at the cut. The source edit already
      // alternates wide / close framing, so each cut lands as a punch.
      CUTS.forEach((t, i) => {{
        const end = i + 1 < CUTS.length ? CUTS[i + 1] : DURATION;
        tl.fromTo(
          "#cam",
          {{ scale: 1 }},
          {{ scale: 1.035, duration: end - t, ease: "none", immediateRender: i === 0 }},
          t
        );
      }});

      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""

os.makedirs(os.path.join(ROOT, "compositions"), exist_ok=True)
with open(os.path.join(ROOT, "compositions", "captions.html"), "w", encoding="utf-8") as f:
    f.write(captions)
with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(index)
print(f"wrote index.html + compositions/captions.html: {len(cards)} cards, {DURATION}s")
