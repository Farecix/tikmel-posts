"""Render a bold 'WHAT ARE WE DOING?' style cover slide (1080x1350) for carousels.

Usage: python3 design/render_poster.py design/covers.json
Each item: id, title (English, \\n = line break), thai (Thai question), body (Thai), bg (optional).
"""
import html, json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).parent))
from render_guide import FACES, ROOT

e = html.escape


def page(c):
    title = "<br>".join(e(x) for x in c["title"].split("\n"))
    bg = c.get("bg", "#DEFD62")
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{FACES}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px}}
body{{background:{bg};color:#0B0D08;font-family:"Plex Thai",sans-serif;padding:84px 72px 70px;display:flex;flex-direction:column}}
.brand{{font-size:28px;font-weight:700;letter-spacing:.06em}}
h1{{font-family:Anton,"Plex Thai",sans-serif;font-weight:400;font-size:{c.get("size",200)}px;line-height:.98;
 letter-spacing:-.01em;margin-top:150px;text-transform:uppercase}}
.th{{font-size:64px;font-weight:700;line-height:1.3;margin-top:34px}}
.body{{font-size:34px;line-height:1.5;margin-top:18px;max-width:900px}}
.bottom{{margin-top:auto;border-top:3px solid #0B0D08;padding-top:26px;display:flex;justify-content:space-between;
 font-size:30px;font-weight:700}}
</style></head><body>
<div class="brand">TIKMEL TECH</div>
<h1>{title}</h1>
<div class="th">{e(c["thai"])}</div>
<div class="body">{e(c["body"])}</div>
<div class="bottom"><span>tikmeltech.live</span><span>ปัดเลย →</span></div>
</body></html>"""


def main(path):
    items = json.loads((ROOT / path).read_text())
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for c in items:
            f = ROOT / f"posts/v2/_{c['id']}.html"
            f.write_text(page(c))
            pg.goto(f.as_uri()); pg.evaluate("document.fonts.ready")
            over = pg.evaluate("document.body.scrollHeight > 1350")
            pg.screenshot(path=str(ROOT / f"posts/v2/{c['id']}.jpg"), type="jpeg", quality=92)
            f.unlink()
            print(c["id"], "OVERFLOW" if over else "ok")
        b.close()


if __name__ == "__main__":
    main(sys.argv[1])
