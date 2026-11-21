"""Take mobile screenshots of client sites (iPhone 13 emulation)."""
import sys
from playwright.sync_api import sync_playwright
SITES = {"twobox": "https://twoboxhairstudio.live", "ink": "https://goodlytattoo.live",
         "pearl": "https://queentarathaimassage.com", "goggen": "https://goggensportpub.online"}
want = sys.argv[1:] or list(SITES)
with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(**pw.devices["iPhone 13"])
    for k in want:
        pg = ctx.new_page()
        try:
            pg.goto(SITES[k], wait_until="networkidle", timeout=45000)
        except Exception as ex:
            print(k, "load issue:", str(ex)[:80])
        pg.wait_for_timeout(2500)
        h = pg.evaluate("document.body.scrollHeight")
        for i, y in enumerate([0, int(h * 0.25), int(h * 0.5)]):
            pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(1200)
            pg.screenshot(path=f"design/photos/work/mobile/{k}_{i}.png")
        print(k, "ok", h)
        pg.close()
    b.close()
