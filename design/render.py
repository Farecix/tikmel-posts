"""Render v2 post images (1080x1350 JPEG) from posts_v2.json.

Usage: python3 design/render.py [id ...]
Thai font: set THAI_FONT to a family name installed on the machine
(e.g. "LINE Seed Sans TH", "Anuphan"). Default: IBM Plex Sans Thai from design/fonts.
"""
import html, json, os, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
FONT = os.environ.get("THAI_FONT", "IBM Plex Sans Thai")
FONT_DIR = ROOT / "design/fonts"
e = html.escape
FACES = "".join(
    f'@font-face{{font-family:"IBM Plex Sans Thai";font-weight:{w};src:url("{(FONT_DIR / f"IBMPlexSansThai-{n}.ttf").as_uri()}")}}'
    for n, w in [("Regular", 400), ("Medium", 500), ("SemiBold", 600), ("Bold", 700)])


def visual(v, accent, tint):
    t = v["type"]
    if t == "chat":
        out = []
        for side, text in v["items"]:
            cls = "me" if side == "r" else "them"
            out.append(f'<div class="b {cls}">{e(text)}</div>')
        return '<div class="chat">' + "".join(out) + "</div>"
    if t == "rows":
        rows = []
        for l, r, tag in v["items"]:
            tg = f'<span class="tag">{e(tag)}</span>' if tag else ""
            rows.append(f'<div class="row"><span class="l">{e(l)}</span><span class="r">{e(r)}{tg}</span></div>')
        foot = f'<div class="foot">{e(v["foot"])}</div>' if v.get("foot") else ""
        return f'<div class="card"><div class="ct">{e(v["title"])}</div>{"".join(rows)}{foot}</div>'
    if t == "steps":
        s = "".join(f'<div class="step"><span class="n">{i}</span><span>{e(x)}</span></div>'
                    for i, x in enumerate(v["items"], 1))
        return f'<div class="card steps">{s}</div>'
    raise ValueError(t)


def page(p):
    a, tint = p["accent"], p["tint"]
    head = "<br>".join(e(x) for x in p["headline"].split("\n"))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{FACES}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px}}
body{{font-family:"{FONT}",sans-serif;background:#F6F2EB;color:#1E1C19;
  padding:88px 84px 72px;display:flex;flex-direction:column;letter-spacing:0}}
.top{{display:flex;justify-content:space-between;align-items:center}}
.kicker{{font-size:30px;font-weight:700;color:{a};background:{tint};padding:10px 22px;border-radius:999px}}
.brand{{font-size:24px;font-weight:700;color:#6B655C}}
h1{{font-size:98px;line-height:1.3;font-weight:700;margin-top:56px}}
.sub{{font-size:38px;line-height:1.5;color:#4A453E;margin-top:22px;max-width:880px}}
.vis{{margin-top:52px;flex:1}}
.card{{background:#fff;border:2px solid #E6DED2;border-radius:28px;padding:34px 38px}}
.ct{{font-size:30px;font-weight:700;color:{a};padding-bottom:18px;border-bottom:2px solid #EFE8DD}}
.row{{display:flex;justify-content:space-between;align-items:center;font-size:34px;padding:20px 0;border-bottom:2px solid #F2ECE3}}
.row .l{{color:#4A453E}} .row .r{{font-weight:700;display:flex;align-items:center;gap:14px}}
.tag{{font-size:24px;font-weight:700;color:{a};background:{tint};padding:6px 14px;border-radius:10px}}
.foot{{font-size:27px;color:#6B655C;padding-top:20px}}
.chat{{display:flex;flex-direction:column;gap:18px}}
.b{{font-size:34px;line-height:1.5;padding:18px 28px;border-radius:30px;max-width:780px}}
.them{{background:#fff;border:2px solid #E6DED2;align-self:flex-start;border-bottom-left-radius:8px}}
.me{{background:{a};color:#fff;align-self:flex-end;border-bottom-right-radius:8px}}
.steps{{display:flex;flex-direction:column;gap:6px}}
.step{{display:flex;align-items:center;gap:26px;font-size:36px;padding:16px 0}}
.n{{width:58px;height:58px;border-radius:50%;background:{tint};color:{a};font-weight:700;
  display:flex;align-items:center;justify-content:center;font-size:30px;flex:none}}
.bottom{{display:flex;justify-content:space-between;align-items:baseline;border-top:2px solid #E2D9CC;padding-top:30px}}
.cta{{font-size:34px;font-weight:700}} .url{{font-size:34px;font-weight:700;color:{a}}}
</style></head><body>
<div class="top"><span class="kicker">{e(p["kicker"])}</span><span class="brand">TIKMEL TECH</span></div>
<h1>{head}</h1>
<div class="sub">{e(p["sub"])}</div>
<div class="vis">{visual(p["visual"], a, tint)}</div>
<div class="bottom"><span class="cta">ปรึกษาฟรี ทัก DM หรือ LINE</span><span class="url">tikmeltech.live</span></div>
</body></html>"""


def main(ids):
    posts = json.loads((ROOT / "design/posts_v2.json").read_text())
    if ids:
        posts = [p for p in posts if p["id"] in ids]
    (ROOT / "posts/v2").mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for p in posts:
            pg.goto("about:blank"); pg.set_content(page(p))
            pg.evaluate("document.fonts.ready")
            over = pg.evaluate("document.body.scrollHeight > 1350")
            out = ROOT / f"posts/v2/{p['id']}.jpg"
            pg.screenshot(path=str(out), type="jpeg", quality=90)
            print(out.name, "OVERFLOW" if over else "ok")
        b.close()


if __name__ == "__main__":
    main(sys.argv[1:])
