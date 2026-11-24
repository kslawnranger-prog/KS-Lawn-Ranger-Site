#!/usr/bin/env python3
"""Resize and compress site photos. Originals stay in images/originals/."""

import json
import shutil
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "images"
ORIGINALS = SRC / "originals"
OUT = SRC / "opt"
MANIFEST = ROOT / "images" / "manifest.json"

PHOTO_WIDTHS = (480, 720, 960)
# Largest file a page should download for one photo.
MAX_BYTES = 190_000


def save_bytes(im, fmt, quality):
    buf = BytesIO()
    if fmt == "WEBP":
        im.save(buf, "WEBP", quality=quality, method=6)
    else:
        im.save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
    return buf.getvalue()


def compress(im, fmt, target=MAX_BYTES):
    """Drop quality, then blur noisy detail, until the file fits the budget."""
    work = im
    radius = 0.0
    for _ in range(5):
        quality = 74 if fmt == "WEBP" else 76
        floor = 40 if fmt == "WEBP" else 46
        while quality >= floor:
            data = save_bytes(work, fmt, quality)
            if len(data) <= target:
                return data, quality, radius
            quality -= 6
        radius += 0.35
        work = im.filter(ImageFilter.GaussianBlur(radius))
    data = save_bytes(work, fmt, floor)
    return data, floor, radius


def archive_originals():
    ORIGINALS.mkdir(parents=True, exist_ok=True)
    for path in sorted(SRC.iterdir()):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            continue
        dest = ORIGINALS / path.name
        if not dest.exists():
            shutil.copy2(path, dest)


def trim_near_white(im, threshold=28):
    rgb = im.convert("RGB")
    diff = ImageChops.difference(rgb, Image.new("RGB", rgb.size, (255, 255, 255)))
    mask = diff.convert("L").point(lambda p: 255 if p > threshold else 0)
    bbox = mask.getbbox()
    if not bbox:
        return rgb
    pad = 12
    left = max(0, bbox[0] - pad)
    top = max(0, bbox[1] - pad)
    right = min(rgb.width, bbox[2] + pad)
    bottom = min(rgb.height, bbox[3] + pad)
    return rgb.crop((left, top, right, bottom))


def optimize_photo(path):
    im = Image.open(path)
    im = ImageOps.exif_transpose(im).convert("RGB")
    slug = path.stem
    variants = []
    for width in PHOTO_WIDTHS:
        if im.width < width and width != PHOTO_WIDTHS[0]:
            continue
        target_w = min(width, im.width)
        height = round(im.height * (target_w / im.width))
        resized = im.resize((target_w, height), Image.Resampling.LANCZOS)
        webp = OUT / f"{slug}-{target_w}.webp"
        jpg = OUT / f"{slug}-{target_w}.jpg"
        w_data, w_q, w_blur = compress(resized, "WEBP")
        j_data, j_q, j_blur = compress(resized, "JPEG")
        webp.write_bytes(w_data)
        jpg.write_bytes(j_data)
        variants.append(
            {
                "w": target_w,
                "h": height,
                "webp": f"/images/opt/{webp.name}",
                "jpg": f"/images/opt/{jpg.name}",
                "webp_bytes": len(w_data),
                "jpg_bytes": len(j_data),
                "webp_q": w_q,
                "jpg_q": j_q,
                "blur": round(max(w_blur, j_blur), 2),
            }
        )
    return {
        "slug": slug,
        "src_w": im.width,
        "src_h": im.height,
        "variants": variants,
    }


def optimize_logo():
    src = ORIGINALS / "logo-centered.png"
    im = trim_near_white(Image.open(src))
    width = 320
    height = round(im.height * (width / im.width))
    resized = im.resize((width, height), Image.Resampling.LANCZOS)
    webp = OUT / "logo.webp"
    png = OUT / "logo.png"
    resized.save(webp, "WEBP", quality=76, method=6)
    quantized = resized.quantize(colors=48, method=2, dither=0)
    quantized.save(png, "PNG", optimize=True)

    square = Image.new("RGB", (512, 512), (255, 255, 255))
    thumb = resized.copy()
    thumb.thumbnail((440, 440), Image.Resampling.LANCZOS)
    square.paste(thumb, ((512 - thumb.width) // 2, (512 - thumb.height) // 2))
    icon32 = square.resize((32, 32), Image.Resampling.LANCZOS)
    icon180 = square.resize((180, 180), Image.Resampling.LANCZOS)
    icon32.save(ROOT / "favicon-32.png", "PNG", optimize=True)
    icon180.save(ROOT / "apple-touch-icon.png", "PNG", optimize=True)
    icon16 = square.resize((16, 16), Image.Resampling.LANCZOS)
    icon32.save(
        ROOT / "favicon.ico",
        format="ICO",
        sizes=[(16, 16), (32, 32)],
        append_images=[icon16],
    )
    return {
        "slug": "logo",
        "src_w": resized.width,
        "src_h": resized.height,
        "variants": [
            {
                "w": resized.width,
                "h": resized.height,
                "webp": "/images/opt/logo.webp",
                "jpg": "/images/opt/logo.png",
                "webp_bytes": webp.stat().st_size,
                "jpg_bytes": png.stat().st_size,
            }
        ],
    }


def main():
    archive_originals()
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    manifest = {}
    for path in sorted(ORIGINALS.iterdir()):
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            continue
        if path.name == "logo-centered.png":
            continue
        info = optimize_photo(path)
        manifest[info["slug"]] = info
        largest = info["variants"][-1]
        print(
            f"{info['slug']:22} {largest['w']}x{largest['h']}  "
            f"webp {largest['webp_bytes']//1024:4}KB  jpg {largest['jpg_bytes']//1024:4}KB"
        )
    logo = optimize_logo()
    manifest["logo"] = logo
    print(
        f"logo                   {logo['src_w']}x{logo['src_h']}  "
        f"webp {logo['variants'][0]['webp_bytes']//1024}KB  "
        f"png {logo['variants'][0]['jpg_bytes']//1024}KB"
    )
    MANIFEST.write_text(json.dumps(manifest, indent=2))
    print("wrote", MANIFEST)


if __name__ == "__main__":
    main()
