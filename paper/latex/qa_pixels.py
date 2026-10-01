from PIL import Image
import glob, os

pages = sorted(glob.glob('build/rendered_pages/page-*.png'))
print(f"pages: {len(pages)}")
issues = []
for p in pages:
    img = Image.open(p).convert('L')
    w, h = img.size
    px = img.load()
    # find ink bounds (non-white pixels; threshold 245)
    minx, maxx, miny, maxy = w, -1, h, -1
    dark_rows_white_span = 0
    for y in range(0, h, 2):
        row_ink = False
        for x in range(0, w, 2):
            if px[x, y] < 245:
                if x < minx: minx = x
                if x > maxx: maxx = x
                if y < miny: miny = y
                if y > maxy: maxy = y
                row_ink = True
    name = os.path.basename(p)
    n = int(name.split('-')[1].split('.')[0])
    # geometry at 100dpi: page ~610x926px; text block ~x[69,545];
    # running header starts at y=40px (10.2mm) by design (journal convention)
    flag = []
    if minx < 58: flag.append(f"ink at x={minx} (left overflow?)")
    if maxx > 555: flag.append(f"ink at x={maxx} (right overflow?)")
    if miny < 38: flag.append(f"ink at y={miny} (top overflow?)")
    if maxy > 880: flag.append(f"ink at y={maxy} (bottom overflow?)")
    ink_ratio = 0
    if flag:
        issues.append((n, flag, (minx, maxx, miny, maxy), img.size))

print("pages with bounds flags:")
for n, flag, bounds, size in issues:
    print(f"  page {n}: {flag} bounds={bounds} size={size}")
if not issues:
    print("  none - all pages within printable bounds")

# blank-ish page detection: fraction of sampled dark pixels
print("\nvery sparse pages (<0.3% ink):")
for p in pages:
    img = Image.open(p).convert('L')
    w, h = img.size
    px = img.load()
    dark = sum(1 for y in range(0, h, 4) for x in range(0, w, 4) if px[x, y] < 200)
    total = (h // 4) * (w // 4)
    if dark / total < 0.003:
        print(" ", os.path.basename(p), f"{dark/total:.4%}")
