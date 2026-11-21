"""Highlight cover options (1080x1920; Instagram shows the centre circle)."""
from pathlib import Path
import sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).parent))
from render_guide import ROOT
LIME, BG = "#D4FF3A", "#0E0E10"
PHONE = ('<svg width="300" height="300" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="1.6" '
         'stroke-linecap="round" stroke-linejoin="round"><rect x="6.5" y="2.5" width="11" height="19" rx="2.5"/>'
         '<path d="M10.5 18.5h3"/><path d="M9 7h6M9 10h6M9 13h3.5"/></svg>')
GRID = ('<svg width="300" height="300" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="1.6" '
        'stroke-linecap="round" stroke-linejoin="round"><rect x="3.5" y="3.5" width="7" height="7" rx="1.5"/>'
        '<rect x="13.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.5"/>'
        '<rect x="13.5" y="13.5" width="7" height="7" rx="1.5"/></svg>')
OPTS = {"highlight_cover_web_a": (LIME, BG, BG), "highlight_cover_web_b": (BG, LIME, BG),
        "highlight_cover_backoffice_a": (LIME, BG, BG), "highlight_cover_backoffice_b": (BG, LIME, BG)}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    for name, (circle, icon, page_bg) in OPTS.items():
        ring = f"border:8px solid {LIME};" if circle == BG else ""
        pg.set_content(f'<body style="margin:0;width:1080px;height:1920px;background:{page_bg};display:flex;align-items:center;justify-content:center">'
                       f'<div style="width:620px;height:620px;border-radius:50%;background:{circle};{ring}box-sizing:border-box;display:flex;align-items:center;justify-content:center">'
                       f'{(GRID if "backoffice" in name else PHONE).format(c=icon)}</div></body>')
        pg.screenshot(path=str(ROOT / f"posts/v2/stories/{name}.jpg"), type="jpeg", quality=92)
    b.close()
