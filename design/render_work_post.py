"""Portfolio carousel posts (1080x1350) + matching 9:16 stories, per client.

Usage: python3 design/render_work_post.py design/work_posts.json
Each project: id, name, sector_th, sector_en, cover {th, en, phone, window}, slides [ {label, shot|phones, points, tags} ]
Outputs posts/v2/work/<id>_00_cover.jpg, <id>_01.jpg ... and stories/<id>_story_NN.jpg
"""
import html, json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).parent))
from render_guide import FACES, ROOT
from render_story import story, LIME, BG

e = html.escape
P = lambda p: (ROOT / p).as_uri()

POST_CSS = """<style>
html,body{height:1350px!important}
body{padding:72px 72px 0!important}
.top{font-size:26px!important}
h1{font-size:68px!important;margin-top:34px!important}
.sec{font-size:32px!important;margin-top:10px!important}
.sec small{font-size:23px!important}
.frame{top:400px!important;bottom:150px!important;left:72px!important;right:72px!important;gap:30px!important}
.frame .phones{height:560px!important} .frame .phones img,.frame .phones.n2 img{height:560px!important}
li b{font-size:30px!important} li span{font-size:22px!important} ul{gap:16px!important}
li:before{top:13px!important;width:12px!important;height:12px!important}
.tags{display:none!important}
.foot{bottom:56px!important;font-size:26px!important}
</style></head>"""


def cover(c, name, th_sector):
    win = (f'<div class="win"><div class="bar"><i></i><i></i><i></i></div><img src="{P(c["window"])}"></div>'
           if c.get("window") else "")
    phone = f'<img class="ph" src="{P(c["phone"])}">' if c.get("phone") else ""
    head = "<br>".join(e(x) for x in name.split("\n"))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FACES}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;overflow:hidden}}
body{{font-family:"Plex Thai",sans-serif;color:#F4F5F0;position:relative;padding:72px 72px 0;
 background:radial-gradient(800px 600px at 100% 0%,rgba(212,255,58,.10),transparent 70%),{BG}}}
.top{{display:flex;justify-content:space-between;font-size:26px;font-weight:700;letter-spacing:.06em}}
.top .k{{color:{LIME}}}
h1{{font-size:96px;line-height:1.05;font-weight:700;margin-top:56px}}
.th{{font-size:38px;font-weight:700;color:{LIME};margin-top:18px}}
.en{{font-size:26px;color:#A9ABA4;margin-top:6px}}
.win{{position:absolute;left:72px;width:760px;top:640px;border-radius:18px;overflow:hidden;border:3px solid #2B2C2F;background:#1A1B1E;transform:rotate(-2deg)}}
.win .bar{{height:30px;display:flex;gap:8px;align-items:center;padding:0 14px}}
.win .bar i{{width:10px;height:10px;border-radius:50%;background:#3A3B3F}}
.win img{{width:100%;display:block}}
.ph{{position:absolute;right:70px;top:600px;height:540px;border-radius:40px;border:5px solid #2B2C2F;transform:rotate(4deg);box-shadow:0 24px 60px rgba(0,0,0,.6)}}
.bar2{{position:absolute;left:72px;right:72px;bottom:52px;display:flex;justify-content:space-between;align-items:center;font-size:26px;font-weight:700}}
.pill{{background:{LIME};color:{BG};padding:12px 28px;border-radius:999px}}
</style></head><body>
<div class="top"><span>TIKMEL TECH</span><span class="k">ผลงาน · OUR WORK</span></div>
<h1>{head}</h1>
<div class="th">{e(c["th"])}</div>
<div class="en">{e(c["en"])} · {e(th_sector)}</div>
{win}{phone}
<div class="bar2"><span class="pill">tikmeltech.live</span><span>ปัดเลย · Swipe →</span></div>
</body></html>"""


def shoot(pg, htm, out, h):
    f = ROOT / "posts/v2/_tmp.html"
    f.write_text(htm)
    pg.set_viewport_size({"width": 1080, "height": h})
    pg.goto(f.as_uri()); pg.evaluate("document.fonts.ready")
    out.parent.mkdir(parents=True, exist_ok=True)
    pg.screenshot(path=str(out), type="jpeg", quality=92)
    f.unlink()
    print(out.name)


def main(path, only=None):
    projects = json.loads((ROOT / path).read_text())
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page()
        for p in projects:
            if only and p["id"] not in only:
                continue
            od = ROOT / "posts/v2/work"
            shoot(pg, cover(p["cover"], p["name"], p["sector_en"]), od / f"{p['id']}_00_cover.jpg", 1350)
            for i, s in enumerate(p["slides"], 1):
                item = {"name": p["name"], "sector_th": p["sector_th"], "sector_en": p["sector_en"],
                        "tags": s.get("tags", []), **s}
                h9 = story(item)
                shoot(pg, h9, ROOT / f"posts/v2/stories/{p['id']}_story_{i:02d}.jpg", 1920)
                shoot(pg, h9.replace("</head>", POST_CSS, 1), od / f"{p['id']}_{i:02d}.jpg", 1350)
        b.close()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:] or None)
