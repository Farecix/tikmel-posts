"""Dark 4:5 covers (same style as render_cover45.py) for the backoffice guide and the six general posts.

Usage: python3 design/render_cover_v3.py   ->  posts/v3/<id>_00_cover.jpg
"""
from pathlib import Path
import sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).parent))
from render_guide import FACES, CHIP, CYAN, PINK, ROOT

W = lambda n: (ROOT / "design/photos/work" / n).as_uri()
V3 = lambda n: (ROOT / "posts/v3" / n).as_uri()

def window_and_card(win, card):
    return (f'<img class="win" src="{W(win)}">'
            f'<img class="card" src="{V3(card)}">')

def phones_and_card(phones, card):
    ph = "".join(f'<img class="ph p{i}" src="{W("mobile/" + p)}">' for i, p in enumerate(phones))
    return f'<div class="phones">{ph}</div><img class="card" src="{V3(card)}">'

def card_only(card, second=None):
    s = f'<img class="card2" src="{V3(second)}">' if second else ""
    return f'{s}<img class="card big" src="{V3(card)}">'

COVERS = [
    {"id": "backoffice", "kicker": "GUIDE · BACKOFFICE",
     "h1": 'ระบบหลังบ้าน<br><span class="hl">ช่วยร้านคุณ</span><br>ได้อย่างไร?',
     "en": "What does a backoffice do for your business?",
     "art": window_and_card("pearl_bo_overview_top.jpg", "backoffice_03.jpg")},
    {"id": "general_website", "kicker": "WEBSITE",
     "h1": 'ร้านของคุณ<br><span class="hl">มีเว็บไซต์</span><br>หรือยัง?',
     "en": "Why your business needs a website",
     "art": phones_and_card(["pearl_0.png", "twobox_0.png", "ink_0.png"], "general_website.jpg")},
    {"id": "general_line", "kicker": "LINE OA",
     "h1": 'เชื่อม <span class="hl">LINE OA</span><br>กับร้านของคุณ',
     "en": "Connect LINE OA to your business",
     "art": phones_and_card(["twobox_1.png", "pearl_1.png"], "general_line.jpg")},
    {"id": "general_promptpay", "kicker": "ONLINE PAYMENTS",
     "h1": 'รับเงินออนไลน์<br>ผ่าน <span class="hl">PromptPay</span>',
     "en": "Get paid online with PromptPay",
     "art": card_only("general_promptpay.jpg", "backoffice_02.jpg")},
    {"id": "general_ads", "kicker": "DIGITAL ADS",
     "h1": 'โฆษณา<br><span class="hl">ให้ถึงลูกค้า</span><br>ที่ใช่',
     "en": "Ads that reach the right customers",
     "art": card_only("general_ads.jpg", "backoffice_05.jpg")},
    {"id": "general_support", "kicker": "MAINTENANCE &amp; SUPPORT",
     "h1": 'ส่งงานแล้ว<br><span class="hl">เราไม่หายไป</span>',
     "en": "We stay with you after launch",
     "art": window_and_card("twobox_bo_earnings.jpg", "general_support.jpg")},
    {"id": "general_howwework", "kicker": "HOW WE WORK",
     "h1": 'เราทำงาน<br><span class="hl">อย่างไร?</span>',
     "en": "How we work, step by step",
     "art": window_and_card("pearl.jpg", "general_howwework.jpg")},
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
img{{border:3px solid #2A3740;box-shadow:0 24px 60px rgba(0,0,0,.6)}}
.win{{position:absolute;left:60px;top:700px;width:660px;border-radius:20px;transform:rotate(-3deg)}}
.card{{position:absolute;right:60px;top:690px;width:380px;border-radius:22px;transform:rotate(4deg)}}
.card.big{{width:430px;right:110px;top:660px;transform:rotate(4deg)}}
.card2{{position:absolute;left:90px;top:720px;width:400px;border-radius:22px;transform:rotate(-5deg);opacity:.9}}
.phones{{position:absolute;left:60px;top:690px;display:flex;gap:18px}}
.phones .ph{{height:460px;border-radius:28px}}
.phones .p0{{transform:rotate(-5deg)}} .phones .p1{{transform:translateY(30px)}} .phones .p2{{transform:rotate(5deg)}}
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


if __name__ == "__main__":
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for c in COVERS:
            f = ROOT / f"posts/v3/_{c['id']}.html"
            f.write_text(page(c))
            pg.goto(f.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
            pg.screenshot(path=str(ROOT / f"posts/v3/{c['id']}_00_cover.jpg"), type="jpeg", quality=92)
            f.unlink()
            print(c["id"])
        b.close()
