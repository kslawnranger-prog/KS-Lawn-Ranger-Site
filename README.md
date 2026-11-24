# KS Lawn Ranger

Static site for [kslawnranger.com](https://kslawnranger.com). GitHub Pages serves the files at the repository root. Keep `CNAME` and `.nojekyll`.

Python 3 builds the HTML. Pillow is only needed when you add or replace a photo.

```bash
pip install pillow   # once, and only if you add photos
python3 tools/optimize_images.py
python3 tools/build_site.py
```

`tools/build_site.py` rewrites the pages, `sitemap.xml`, and `robots.txt`. Edit the config below, then run the build. Do not edit the generated HTML by hand — the next build replaces it.

## Seasonal promo banner

One place: the `promo` object in `site.config.json`.

```json
"promo": {
  "enabled": true,
  "text": "Now booking seasonal snow contracts and late-fall leaf cleanup. Free on-site estimates.",
  "href": "/services/snow-removal/"
}
```

Set `enabled` to `false` to hide the bar. Then run `python3 tools/build_site.py`.

## Reviews

- Live Google reviews load from the existing Elfsight widget on the homepage. They update in Elfsight, not in this repo.
- The three written quotes live in the `testimonials` array in `site.config.json`. Add an object with `quote` and `place` only for a comment you can actually source. Do not add a star count or a total you have not verified.
- The Google review link is `https://g.page/r/CQ3hgayPFJW2EBM/review`.

## Photos

1. Put the original file in `images/originals/` (jpg or png).
2. Run `python3 tools/optimize_images.py`. It writes resized WebP and JPEG files under `images/opt/` and refreshes `images/manifest.json`.
3. Add the photo to `gallery` in `site.config.json`. `image` must match the filename without the extension. Use `cat` of `mowing`, `landscape`, `cleanup`, `lawn`, or `snow`.
4. To add a before/after slider, add an object to `comparisons` with `before`, `after`, alt text, and a caption.
5. Run `python3 tools/build_site.py`.

The site does not publish prices. Service-area wording stays in this order everywhere: Manhattan, Alma, Wamego, St. George, Junction City, and Ogden. Westmoreland and Paxico are nearby only.

## Quote form

Every main page posts to `https://formspree.io/f/mrblvwde` and redirects to `https://kslawnranger.com/thank-you.html`. The thank-you page is `noindex`.
