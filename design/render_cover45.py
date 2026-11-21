"""Render 4:5 (1080x1350) carousel covers in the dark 'reel cover' style.

Usage: python3 design/render_cover45.py
"""
from pathlib import Path
import sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).parent))
from render_guide import FACES, CHIP, CYAN, PINK, ROOT

P = lambda n: (ROOT / "design/photos" / n).as_uri()

COVERS = [
    {"id": "tiktok_guide_00_cover", "kicker": "GUIDE · TIKTOK LIVE",
     "h1": 'ไลฟ์ TikTok อยู่?<br><span class="hl">เพิ่มรายได้</span><br>จากของขวัญ',
     "en": "Turn gifts into photos on your live", "foot": "ScreenUp LIVE by TIKMEL TECH",
     "art": f'<div class="phones2"><img class="ph a" src="{P("tiktok_guest_upload.jpg")}">'
            f'<img class="ph b" src="{P("tiktok_obs_screen_full.jpg")}"></div>'},
    {"id": "club_guide_00_cover", "kicker": "GUIDE · NIGHTCLUB",
     "h1": 'จอในร้าน<br><span class="hl">ทำเงินได้</span><br>ทุกคืน',
     "en": "Turn your club's screens into revenue", "foot": "ScreenUp by TIKMEL TECH",
     "art": f'<img class="scr" src="{P("club_screen.jpg")}"><div class="phones3">'
            f'<img class="ph a" src="{P("club_guest.jpg")}"><img class="ph b" src="{P("club_djsong.jpg")}"></div>'},
]


def page(c):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{FACES}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;overflow:hidden}}
body{{font-family:"Plex Thai",sans-serif;color:#F3F6F8;position:relative;padding:72px 72px 0;
 background:radial-gradient(800px 600px at 0% 0%,rgba(254,44,85,.22),transparent 70%),
 radial-gradient(800px 700px at 100% 60%,rgba(34,211,238,.16),transparent 70%),#0A0E11}}
.brand{{display:flex;align-items:center;gap:14px;font-size:28px;font-weight:700;letter-spacing:.06em}}
.kicker{{margin-top:64px;font-size:26px;font-weight:700;color:{CYAN};letter-spacing:.2em}}
h1{{font-size:88px;line-height:1.2;font-weight:700;margin-top:10px}}
h1 .hl{{color:{PINK}}}
.en{{font-size:34px;font-weight:600;color:{CYAN};margin-top:10px}}
.ph{{border-radius:30px;border:3px solid #2A3740;box-shadow:0 24px 60px rgba(0,0,0,.6)}}
.phones2{{position:absolute;left:0;right:0;top:665px;display:flex;justify-content:center;gap:40px}}
.phones2 .ph{{height:520px}} .phones2 .a{{transform:rotate(-4deg) translateY(20px)}} .phones2 .b{{transform:rotate(4deg)}}
.scr{{position:absolute;left:60px;width:640px;top:680px;border-radius:20px;border:3px solid #2A3740;transform:rotate(-2deg)}}
.phones3{{position:absolute;left:520px;right:40px;top:850px;display:flex;justify-content:space-between}}
.phones3 .ph{{height:350px}} .phones3 .a{{transform:rotate(-4deg)}} .phones3 .b{{transform:rotate(4deg)}}
.bar{{position:absolute;left:72px;right:72px;bottom:56px;display:flex;justify-content:space-between;align-items:center;font-size:26px;color:#A8B3B9}}
.pill{{background:{CYAN};color:#071014;font-weight:700;padding:14px 30px;border-radius:999px;font-size:28px}}
.swipe{{font-size:26px;color:#F3F6F8;font-weight:600}}
</style></head><body>
<div class="brand">{CHIP}TIKMEL TECH</div>
<div class="kicker">{c["kicker"]}</div>
<h1>{c["h1"]}</h1>
<div class="en">{c["en"]}</div>
{c["art"]}
<div class="bar"><span class="pill">tikmeltech.live</span><span class="swipe">ปัดเลย · Swipe →</span></div>
</body></html>"""


with sync_playwright() as pw:
    b = pw.chromium.launch(args=["--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for c in COVERS:
        f = ROOT / f"posts/v2/_{c['id']}.html"
        f.write_text(page(c))
        pg.goto(f.as_uri()); pg.evaluate("document.fonts.ready")
        pg.screenshot(path=str(ROOT / f"posts/v2/{c["id"]}_dark.jpg"), type="jpeg", quality=92)
        f.unlink()
        print(c["id"])
    b.close()
