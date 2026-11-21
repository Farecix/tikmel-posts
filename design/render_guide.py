"""Render a GUIDE-style carousel (dark, like the backoffice carousel) from a JSON file.

Usage: python3 design/render_guide.py design/tiktok_guide.json
Each slide: kicker, headline (Thai, \n = line break), en (English headline line),
body (Thai), body_en, visual {type: tiles|rows|steps|chat|photo|none}, cta (bool).
Photos: visual {"type":"photo","src":"design/photos/x.jpg"} (path relative to repo root).
"""
import html, json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "design/fonts"
e = html.escape
FACES = "".join(
    f'@font-face{{font-family:"Plex Thai";font-weight:{w};src:url("{(FONT_DIR / f"IBMPlexSansThai-{n}.ttf").as_uri()}")}}'
    for n, w in [("Regular", 400), ("Medium", 500), ("SemiBold", 600), ("Bold", 700)])
CYAN, PINK = "#22D3EE", "#FE2C55"
CHIP = ('<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="' + CYAN + '" stroke-width="1.6">'
        '<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9.5" y="9.5" width="5" height="5"/>'
        '<path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/></svg>')


def visual(v):
    t = v.get("type", "none")
    if t == "none":
        return ""
    if t == "photo":
        return f'<div class="photo"><img src="{(ROOT / v["src"]).as_uri()}"></div>'
    if t == "tiles":
        tiles = "".join(f'<div class="tile"><span class="dot" style="background:{c}"></span>{e(x)}</div>'
                        for x, c in zip(v["items"], [CYAN, "#34D399", "#FBBF24", "#C084FC"]))
        return f'<div class="tiles">{tiles}</div>'
    if t == "rows":
        rows = "".join(
            f'<div class="row"><span class="l">{e(l)}</span><span class="r">{e(r)}'
            + (f'<span class="tag">{e(tag)}</span>' if tag else "") + "</span></div>"
            for l, r, tag in v["items"])
        foot = f'<div class="foot">{e(v["foot"])}</div>' if v.get("foot") else ""
        return f'<div class="card"><div class="ct">{e(v["title"])}</div>{rows}{foot}</div>'
    if t == "steps":
        s = "".join(f'<div class="step"><span class="n">{i}</span><span>{e(x)}</span></div>'
                    for i, x in enumerate(v["items"], 1))
        return f'<div class="card">{s}</div>'
    if t == "chat":
        return '<div class="chat">' + "".join(f'<div class="b">{e(x)}</div>' for x in v["items"]) + "</div>"
    raise ValueError(t)


def page(s, i, n):
    head = "<br>".join(e(x) for x in s["headline"].split("\n"))
    bars = "".join(f'<span class="bar{" on" if k <= i else ""}"></span>' for k in range(n))
    if s.get("cta"):
        bottom = (f'<div class="ctaw"><span class="pill">tikmeltech.live</span>'
                  f'<div class="msg">ทักมาทาง DM หรือ LINE · Message us on DM or LINE</div></div>'
                  f'<div class="prog">{bars}</div>')
    else:
        bottom = f'<div class="prog">{bars}<span class="swipe">ปัดต่อ · Swipe →</span></div>'
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{FACES}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px}}
body{{font-family:"Plex Thai",sans-serif;color:#F3F6F8;letter-spacing:0;
 background:radial-gradient(900px 600px at 100% 0%,rgba(34,211,238,.13),transparent 70%),#0A0E11;
 padding:72px 72px 64px;display:flex;flex-direction:column}}
.brand{{display:flex;align-items:center;gap:14px;font-size:28px;font-weight:700;letter-spacing:.06em}}
.kicker{{margin-top:{"150px" if s.get("cta") else "58px"};font-size:24px;font-weight:700;color:{CYAN};letter-spacing:.22em}}
h1{{font-size:{s.get("size",76)}px;line-height:1.28;font-weight:700;margin-top:18px}}
.en{{font-size:36px;font-weight:600;color:{CYAN};margin-top:12px;padding-bottom:26px;border-bottom:2px solid #1E2930}}
.body{{font-size:30px;line-height:1.5;margin-top:24px;color:#E4E9EC}}
.body_en{{font-size:23px;color:#8B989F;margin-top:6px}}
.vis{{margin-top:40px;flex:1;min-height:0;display:flex;flex-direction:column}}
.card{{background:#11171B;border:2px solid #1E2930;border-radius:26px;padding:30px 34px}}
.ct{{font-size:26px;font-weight:700;color:{CYAN};padding-bottom:14px;border-bottom:2px solid #1E2930}}
.row{{display:flex;justify-content:space-between;align-items:center;font-size:30px;padding:18px 0;border-bottom:2px solid #182127}}
.row .l{{color:#A8B3B9}} .row .r{{font-weight:600;display:flex;gap:14px;align-items:center}}
.tag{{font-size:21px;font-weight:700;color:#0A0E11;background:{CYAN};padding:5px 14px;border-radius:999px}}
.foot{{font-size:22px;color:#7D8A91;padding-top:16px}}
.step{{display:flex;align-items:center;gap:24px;font-size:32px;padding:14px 0}}
.n{{width:52px;height:52px;border-radius:50%;border:2px solid {CYAN};color:{CYAN};font-weight:700;font-size:26px;
 display:flex;align-items:center;justify-content:center;flex:none}}
.tiles{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}
.tile{{background:#11171B;border:2px solid #1E2930;border-radius:22px;padding:28px;font-size:30px;font-weight:600;
 display:flex;flex-direction:column;gap:18px}}
.dot{{width:22px;height:22px;border-radius:6px}}
.chat{{display:flex;flex-direction:column;gap:16px;align-items:flex-end}}
.b{{font-size:29px;padding:16px 26px;border-radius:26px;border-bottom-right-radius:8px;background:#11171B;
 border:2px solid #1E2930}}
.b:first-child{{border-color:{PINK}}}
.photo{{flex:1;min-height:0;display:flex;justify-content:center;align-items:flex-start}}
.photo img{{max-width:100%;max-height:100%;border-radius:22px;border:2px solid #263139;display:block}}
.prog{{display:flex;align-items:center;gap:10px;margin-top:36px}}
.bar{{width:52px;height:5px;border-radius:3px;background:#26323A}} .bar.on{{background:{CYAN}}}
.swipe{{margin-left:auto;font-size:22px;color:#8B989F}}
.ctaw{{margin-top:auto}}
.pill{{display:inline-block;background:{CYAN};color:#071014;font-size:40px;font-weight:700;padding:22px 44px;border-radius:999px}}
.msg{{font-size:26px;color:#A8B3B9;margin-top:26px}}
</style></head><body>
<div class="brand">{CHIP}TIKMEL TECH</div>
<div class="kicker">{e(s["kicker"])}</div>
<h1>{head}</h1>
<div class="en">{e(s["en"])}</div>
<div class="body">{e(s["body"])}</div>
<div class="body_en">{e(s["body_en"])}</div>
<div class="vis">{visual(s.get("visual", {}))}</div>
{bottom}
</body></html>"""


def main(path):
    slides = json.loads((ROOT / path).read_text())
    out_dir = ROOT / "posts/v2"
    out_dir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for i, s in enumerate(slides):
            f = out_dir / f"{s['id']}.html"
            f.write_text(page(s, i, len(slides)))
            pg.goto(f.as_uri())
            pg.evaluate("document.fonts.ready")
            over = pg.evaluate("document.body.scrollHeight > 1350")
            pg.screenshot(path=str(out_dir / f"{s['id']}.jpg"), type="jpeg", quality=90)
            f.unlink()
            print(s["id"], "OVERFLOW" if over else "ok")
        b.close()


if __name__ == "__main__":
    main(sys.argv[1])
