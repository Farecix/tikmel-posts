"""Render the 1080x1920 Reels cover for the TikTok guide."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import sys
sys.path.insert(0, str(Path(__file__).parent))
from render_guide import FACES, CHIP, CYAN, PINK, ROOT

P = lambda n: (ROOT / "design/photos" / n).as_uri()
HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
{FACES}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden}}
body{{font-family:"Plex Thai",sans-serif;color:#F3F6F8;
 background:radial-gradient(900px 700px at 0% 0%,rgba(254,44,85,.22),transparent 70%),
 radial-gradient(900px 800px at 100% 55%,rgba(34,211,238,.16),transparent 70%),#0A0E11;
 padding:110px 80px 0;position:relative}}
.brand{{display:flex;align-items:center;gap:14px;font-size:30px;font-weight:700;letter-spacing:.06em}}
.kicker{{margin-top:120px;font-size:30px;font-weight:700;color:{CYAN};letter-spacing:.2em}}
h1{{font-size:112px;line-height:1.22;font-weight:700;margin-top:18px}}
h1 .hl{{color:{PINK}}}
.en{{font-size:42px;font-weight:600;color:{CYAN};margin-top:18px}}
.phones{{position:absolute;left:0;right:0;top:930px;display:flex;justify-content:center;gap:44px}}
.ph{{height:700px;border-radius:40px;border:3px solid #2A3740;box-shadow:0 30px 80px rgba(0,0,0,.6)}}
.ph.a{{transform:rotate(-4deg) translateY(30px)}} .ph.b{{transform:rotate(4deg)}}
.swipe{{position:absolute;left:80px;right:80px;top:1690px;display:flex;justify-content:space-between;align-items:center;font-size:30px;color:#A8B3B9}}
.pill{{background:{CYAN};color:#071014;font-weight:700;padding:16px 34px;border-radius:999px;font-size:32px}}
</style></head><body>
<div class="brand">{CHIP}TIKMEL TECH</div>
<div class="kicker">GUIDE · TIKTOK LIVE</div>
<h1>ไลฟ์ TikTok อยู่?<br><span class="hl">เพิ่มรายได้</span><br>จากของขวัญ</h1>
<div class="en">Turn gifts into photos on your live</div>
<div class="phones"><img class="ph a" src="{P('tiktok_guest_upload.jpg')}"><img class="ph b" src="{P('tiktok_obs_screen_full.jpg')}"></div>
<div class="swipe"><span>ScreenUp LIVE by TIKMEL TECH</span><span class="pill">tikmeltech.live</span></div>
</body></html>"""

out = ROOT / "posts/v2/tiktok_reel_cover.jpg"
f = ROOT / "posts/v2/_cover.html"
f.write_text(HTML)
with sync_playwright() as pw:
    b = pw.chromium.launch(args=["--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.goto(f.as_uri()); pg.evaluate("document.fonts.ready")
    pg.screenshot(path=str(out), type="jpeg", quality=92)
    b.close()
f.unlink()
print(out)
