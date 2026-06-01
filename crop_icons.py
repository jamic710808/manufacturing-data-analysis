from PIL import Image
from pathlib import Path

img = Image.open("D:/opencode/manufacturing-data-analysis/images/icon-sheet.png").convert("RGBA")
w, h = img.size
n = 4
icons = ["icon_price", "icon_delivery", "icon_quality", "icon_payment"]

for i, name in enumerate(icons):
    x0 = i * (w // n)
    x1 = (i + 1) * (w // n) if i < n-1 else w
    col_w = x1 - x0
    sq = min(col_w, h)
    cx, cy = x0 + col_w // 2, h // 2
    crop = img.crop((cx-sq//2, cy-sq//2, cx+sq//2, cy+sq//2))
    crop = crop.resize((256, 256), Image.LANCZOS)
    crop.save(f"D:/opencode/manufacturing-data-analysis/images/{name}.png")
    print(f"Saved {name}.png")

DARK_THRESHOLD = 45
FADE_THRESHOLD = 80

for name in icons:
    p = Path(f"D:/opencode/manufacturing-data-analysis/images/{name}.png")
    img2 = Image.open(p).convert("RGBA")
    data = img2.load()
    rw, rh = img2.size
    for y in range(rh):
        for x in range(rw):
            r, g, b, a = data[x, y]
            lum = r * 0.299 + g * 0.587 + b * 0.114
            if lum < DARK_THRESHOLD:
                data[x, y] = (r, g, b, 0)
            elif lum < FADE_THRESHOLD:
                ratio = (lum - DARK_THRESHOLD) / (FADE_THRESHOLD - DARK_THRESHOLD)
                data[x, y] = (r, g, b, int(255 * ratio))
    img2.save(p)
    print(f"Background removed: {name}.png")