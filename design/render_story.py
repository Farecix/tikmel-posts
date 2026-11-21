"""Portfolio ('ผลงาน · Our Work') stories, 1080x1920, plus the highlight cover.

Usage: python3 design/render_story.py design/work_stories.json
Each item: id, name, sector_th, sector_en, tags [..], shot (path to screenshot, or null = placeholder).
"""
import html, json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).parent))
from render_guide import FACES, ROOT

e = html.escape
LIME, BG = "#D4FF3A", "#0E0E10"
MONITOR = ('<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="1.8" '
           'stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="12" rx="2"/>'
           '<path d="M12 16v4M8 20h8"/></svg>')
BASE = f"""{FACES}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden}}
body{{background:{BG};color:#F4F5F0;font-family:"Plex Thai",sans-serif}}"""


def story(s):
    shot = (f'<div class="win"><div class="bar"><i></i><i></i><i></i></div><img src="{(ROOT / s["shot"]).as_uri()}"></div>' if s.get("shot")
            else '<div class="ph">screenshot</div>')
    if s.get("phones"):
        shot = f'<div class="phones n{len(s["phones"])}">' + "".join(f'<img src="{(ROOT / x).as_uri()}">' for x in s["phones"]) + '</div>'
    pts = "".join(f'<li><b>{e(a)}</b><span>{e(b)}</span></li>' for a, b in s.get("points", []))
    tags = "".join(f'<span>{e(t)}</span>' for t in s["tags"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE}
body{{padding:120px 80px 0;position:relative}}
.top{{display:flex;justify-content:space-between;font-size:30px;font-weight:700;letter-spacing:.06em}}
.top .k{{color:{LIME}}}
h1{{font-size:96px;line-height:1.08;font-weight:700;margin-top:60px}}
.sec{{font-size:40px;font-weight:700;color:{LIME};margin-top:16px}}
.sec small{{display:block;font-size:28px;color:#A9ABA4;font-weight:500;margin-top:4px}}
.frame{{position:absolute;left:80px;right:80px;top:600px;bottom:330px;display:flex;flex-direction:column;gap:54px}}
.win{{border-radius:22px;overflow:hidden;border:3px solid #2B2C2F;background:#1A1B1E}}
.win .bar{{height:40px;display:flex;gap:10px;align-items:center;padding:0 18px}}
.win .bar i{{width:13px;height:13px;border-radius:50%;background:#3A3B3F}}
.frame .win img{{width:100%;max-width:none;max-height:none;border:0;border-radius:0;display:block}}
.phones{{display:flex;justify-content:center;gap:40px;height:1000px}} .phones.n2{{height:880px;gap:30px}} .frame .phones.n2 img{{height:880px}}
.frame .phones img{{height:1000px;width:auto;flex:none;max-width:none;max-height:none;border-radius:48px;border:5px solid #2B2C2F}}
ul{{list-style:none;display:flex;flex-direction:column;gap:26px}}
li{{display:flex;flex-direction:column;padding-left:34px;position:relative}}
li:before{{content:"";position:absolute;left:0;top:18px;width:14px;height:14px;border-radius:4px;background:{LIME}}}
li b{{font-size:38px;font-weight:600}} li span{{font-size:27px;color:#A9ABA4}}
.frame img,.ph{{max-height:100%;max-width:820px;border-radius:44px;border:4px solid #2B2C2F;display:block}}
.ph{{width:560px;height:100%;display:flex;align-items:center;justify-content:center;color:#555;font-size:34px;background:#18181B}}
.tags{{position:absolute;left:80px;right:80px;bottom:200px;display:flex;flex-wrap:wrap;gap:16px}}
.tags span{{font-size:30px;padding:14px 28px;border:2px solid #3A3B3F;border-radius:999px}}
.foot{{position:absolute;left:80px;right:80px;bottom:110px;font-size:32px;font-weight:700;display:flex;justify-content:space-between}}
.foot .u{{color:{LIME}}}
</style></head><body>
<div class="top"><span>TIKMEL TECH</span><span class="k">ผลงาน · OUR WORK</span></div>
<h1>{"<br>".join(e(x) for x in s["name"].split(chr(10)))}</h1>
<div class="sec">{e(s["sector_th"])}<small>{e(s["sector_en"])}</small></div>
<div class="frame">{shot}<ul>{pts}</ul></div>
<div class="tags">{tags}</div>
<div class="foot"><span>ปรึกษาฟรี · Free consultation</span><span class="u">tikmeltech.live</span></div>
</body></html>"""


def cover():
    icon = MONITOR.format(s=300, c=BG)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE}
body{{display:flex;align-items:center;justify-content:center}}
.c{{width:620px;height:620px;border-radius:50%;background:{LIME};display:flex;align-items:center;justify-content:center}}
</style></head><body><div class="c">{icon}</div></body></html>"""


def shoot(pg, htmls, name):
    f = ROOT / f"posts/v2/_{name}.html"
    f.write_text(htmls)
    pg.goto(f.as_uri()); pg.evaluate("document.fonts.ready")
    pg.screenshot(path=str(ROOT / f"posts/v2/stories/{name}.jpg"), type="jpeg", quality=92)
    f.unlink()
    print(name)


def main(path):
    items = json.loads((ROOT / path).read_text())
    (ROOT / "posts/v2/stories").mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        shoot(pg, cover(), "highlight_cover_work")
        for s in items:
            shoot(pg, story(s), s["id"])
        b.close()


if __name__ == "__main__":
    main(sys.argv[1])
