# tikmel-posts

Public image hosting and posting queue for the TIKMEL TECH Instagram account (tikmeltech.live).

- `posts/` holds the finished post images (1080x1350 JPEG, Thai + English).
- `queue.json` lists what gets posted next: `niche` (posted around 11:47 Bangkok time) and `general` (around 19:41).
  Each item is `pending` until it is posted; then it gets `status: posted`, `posted_at` and `media_id`.

Images are served to Instagram from `https://raw.githubusercontent.com/Farecix/tikmel-posts/main/<path>`.

## Design rules (v2)

- Carousels always open with a standalone cover slide (dark reel-cover style: kicker, big Thai headline with pink highlight, English line, product screenshots; `design/render_cover45.py`), then the GUIDE slides.
- Guide carousels use `design/render_guide.py` (dark style); single posts use `design/render.py`.
- Thai font: IBM Plex Sans Thai (`design/fonts`). Reels covers are 1080x1920 (`design/render_cover*.py`).
- Never publish private webhook URLs, client domains or live QR codes in screenshots; blur them.
