# tikmel-posts

Public image hosting and posting queue for the TIKMEL TECH Instagram account (tikmeltech.live).

- `posts/` holds the finished post images (1080x1350 JPEG, Thai + English).
- `queue.json` lists what gets posted next: `niche` (posted around 11:47 Bangkok time) and `general` (around 19:41).
  Each item is `pending` until it is posted; then it gets `status: posted`, `posted_at` and `media_id`.

Images are served to Instagram from `https://raw.githubusercontent.com/Farecix/tikmel-posts/main/<path>`.
