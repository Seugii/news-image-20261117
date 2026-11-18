#!/usr/bin/env python3
"""Render v2 of the entry image for make.fun news-image-20261117.

Dense newspaper front page summing up the world news of Tuesday
17 November 2026, in the style of a broadsheet front page: masthead
date, a "day in UTC" timeline strip, 4 large stories on top, 11 medium
stories below, each with a small flat PIL illustration, a bold headline
and 1-2 lines of text, plus a sources footer. Only PIL, no network,
no randomness: deterministic output.
Output: entry.png beside this file (1024x1024 PNG, <= 1 MiB).
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 28

PAPER = (250, 246, 236)
INK = (26, 26, 26)
NAVY = (22, 35, 63)
GRAY = (85, 85, 85)
LIGHT_RULE = (200, 192, 175)
RED = (185, 28, 28)
BLUE = (29, 78, 216)
BURGUNDY = (157, 23, 77)
TEAL = (15, 118, 110)
OLIVE = (77, 124, 15)
AMBER = (180, 83, 9)
SKY = (188, 214, 232)
SEA = (47, 110, 142)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w, max_lines=None):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        # mark truncation
        lines[-1] = lines[-1].rstrip(".") + "..."
    return lines


# ---------------------------------------------------------------- illustrations
# Each takes (d, w, h) and draws inside a w x h box on a temp image.

def illus_bridge(d, w, h):
    sky_h = int(h * 0.58)
    d.rectangle([0, 0, w, sky_h], fill=SKY)
    d.rectangle([0, sky_h, w, h], fill=SEA)
    d.ellipse([int(w * 0.08), int(h * 0.08), int(w * 0.20), int(h * 0.24)], fill=(242, 201, 76))
    deck_y = int(h * 0.52)
    # towers
    for fx in (0.28, 0.68):
        tx = int(w * fx)
        d.rectangle([tx, int(h * 0.16), tx + 6, deck_y], fill=(58, 58, 58))
    # cables
    d.line([(int(w * 0.28) + 3, int(h * 0.16)), (6, deck_y)], fill=(90, 90, 90), width=2)
    d.line([(int(w * 0.68) + 3, int(h * 0.16)), (w - 6, deck_y)], fill=(90, 90, 90), width=2)
    # deck with a gap in the middle (collapsed span)
    d.rectangle([4, deck_y, int(w * 0.44), deck_y + 6], fill=(43, 43, 43))
    d.rectangle([int(w * 0.60), deck_y, w - 4, deck_y + 6], fill=(43, 43, 43))
    # fallen span tilted into the sea
    d.polygon([(int(w * 0.44), deck_y), (int(w * 0.60), deck_y + 2),
               (int(w * 0.57), deck_y + 18), (int(w * 0.46), deck_y + 16)],
              fill=(43, 43, 43))
    # smoke + flame at the break
    d.ellipse([int(w * 0.47), deck_y - 22, int(w * 0.55), deck_y - 6], fill=(154, 165, 177))
    d.polygon([(int(w * 0.50), deck_y), (int(w * 0.53), deck_y - 14),
               (int(w * 0.56), deck_y)], fill=(232, 89, 12))
    # waves
    for wy in (sky_h + 10, sky_h + 26):
        for wx in range(6, w - 16, 30):
            d.arc([wx, wy, wx + 24, wy + 10], 180, 360, fill=(255, 255, 255), width=2)


def illus_radar(d, w, h):
    d.rectangle([0, 0, w, int(h * 0.62)], fill=SKY)
    d.rectangle([0, int(h * 0.62), w, h], fill=SEA)
    # radar tower + dish
    bx, by = int(w * 0.22), int(h * 0.62)
    d.rectangle([bx - 3, int(h * 0.30), bx + 3, by], fill=(58, 58, 58))
    d.pieslice([bx - 26, int(h * 0.06), bx + 26, int(h * 0.42)], 180, 360, fill=(240, 240, 240), outline=NAVY, width=2)
    d.line([(bx, int(h * 0.24)), (bx + 30, int(h * 0.10))], fill=RED, width=3)
    # dashed drone paths
    for (x0, y0, x1, y1) in ((int(w * 0.45), int(h * 0.18), int(w * 0.85), int(h * 0.30)),
                             (int(w * 0.50), int(h * 0.42), int(w * 0.88), int(h * 0.50))):
        n = 8
        for i in range(n):
            t0, t1 = i / n, (i + 0.5) / n
            d.line([(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0),
                    (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)], fill=NAVY, width=2)
    # drones
    for (dx, dy) in ((int(w * 0.82), int(h * 0.28)), (int(w * 0.86), int(h * 0.48))):
        d.polygon([(dx - 10, dy), (dx + 10, dy - 3), (dx + 12, dy), (dx + 10, dy + 3)], fill=INK)
    # tanker on the sea
    d.polygon([(int(w * 0.55), int(h * 0.72)), (int(w * 0.92), int(h * 0.72)),
               (int(w * 0.97), int(h * 0.80)), (int(w * 0.55), int(h * 0.80))], fill=(43, 43, 43))
    d.rectangle([int(w * 0.60), int(h * 0.64), int(w * 0.68), int(h * 0.72)], fill=(255, 255, 255))


def illus_flags4(d, w, h):
    d.rectangle([0, 0, w, h], fill=(240, 238, 228))
    d.rectangle([0, h - 10, w, h], fill=(226, 220, 205))
    gy = h - 10
    # four flags: US, India, Japan, Australia
    fw, fh = int(w * 0.20), int(h * 0.30)
    for i, fx in enumerate((int(w * 0.05), int(w * 0.29), int(w * 0.53), int(w * 0.77))):
        d.rectangle([fx + 6, 8, fx + 8, gy], fill=(58, 58, 58))
        fy = 10
        if i == 0:  # US
            for s in range(5):
                d.rectangle([fx + 8, fy + s * 3, fx + 8 + fw, fy + s * 3 + 3],
                            fill=RED if s % 2 == 0 else (255, 255, 255))
            d.rectangle([fx + 8, fy, fx + 18, fy + 8], fill=BLUE)
        elif i == 1:  # India
            for s, c in enumerate(((255, 153, 51), (255, 255, 255), (19, 136, 8))):
                d.rectangle([fx + 8, fy + s * 5, fx + 8 + fw, fy + s * 5 + 5], fill=c)
            d.ellipse([fx + 15, fy + 5, fx + 21, fy + 11], outline=NAVY, width=1)
        elif i == 2:  # Japan
            d.rectangle([fx + 8, fy, fx + 8 + fw, fy + fh], fill=(255, 255, 255))
            d.ellipse([fx + 14, fy + 4, fx + 22, fy + 12], fill=RED)
        else:  # Australia (simplified: blue field, stars)
            d.rectangle([fx + 8, fy, fx + 8 + fw, fy + fh], fill=(0, 0, 139))
            for (sx, sy) in ((4, 3), (12, 2), (16, 8), (6, 10)):
                d.ellipse([fx + 8 + sx, fy + sy, fx + 10 + sx, fy + sy + 2], fill=(255, 255, 255))


def illus_measles(d, w, h):
    d.rectangle([0, 0, w, h], fill=(240, 238, 228))
    fw, fh = int(w * 0.24), 12
    # US, Mexico, Bolivia flags on top
    for i, fx in enumerate((int(w * 0.06), int(w * 0.38), int(w * 0.70))):
        if i == 0:
            for s in range(4):
                d.rectangle([fx, 6 + s * 3, fx + fw, 6 + s * 3 + 3],
                            fill=RED if s % 2 == 0 else (255, 255, 255))
            d.rectangle([fx, 6, fx + 10, 6 + 7], fill=BLUE)
        elif i == 1:
            for s, c in enumerate(((0, 104, 71), (255, 255, 255), (206, 17, 38))):
                d.rectangle([fx + s * 8, 6, fx + s * 8 + 8, 6 + fh], fill=c)
        else:
            for s, c in enumerate(((206, 17, 38), (247, 219, 79), (0, 122, 61))):
                d.rectangle([fx, 6 + s * 4, fx + fw, 6 + s * 4 + 4], fill=c)
    # red virus with spikes
    cx, cy, r = w // 2, int(h * 0.62), int(min(w, h) * 0.22)
    for k in range(10):
        import math
        a = 2 * math.pi * k / 10
        x0, y0 = cx + int(r * 0.9 * math.cos(a)), cy + int(r * 0.9 * math.sin(a))
        x1, y1 = cx + int((r + 9) * math.cos(a)), cy + int((r + 9) * math.sin(a))
        d.line([(x0, y0), (x1, y1)], fill=RED, width=3)
        d.ellipse([x1 - 2, y1 - 2, x1 + 2, y1 + 2], fill=RED)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    for (sx, sy, sr) in ((-8, -6, 4), (7, 3, 3), (-2, 9, 3)):
        d.ellipse([cx + sx - sr, cy + sy - sr, cx + sx + sr, cy + sy + sr], fill=(150, 20, 20))


def illus_cop31(d, w, h):
    d.rectangle([0, 0, w, h], fill=(240, 238, 228))
    # globe
    cx, cy, r = int(w * 0.30), int(h * 0.50), int(min(w, h) * 0.30)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(47, 110, 142))
    for (gx, gy, gr) in ((-8, -8, 8), (9, 2, 6), (-3, 10, 7)):
        d.ellipse([cx + gx - gr, cy + gy - gr, cx + gx + gr, cy + gy + gr], fill=(77, 124, 15))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=2)
    # thermometer
    tx = int(w * 0.68)
    d.rounded_rectangle([tx, int(h * 0.12), tx + 14, int(h * 0.78)], radius=7,
                        outline=NAVY, width=2, fill=(255, 255, 255))
    d.rectangle([tx + 4, int(h * 0.30), tx + 10, int(h * 0.72)], fill=RED)
    d.ellipse([tx - 3, int(h * 0.70), tx + 17, int(h * 0.90)], fill=RED, outline=NAVY, width=2)
    # small "no" slash over a flame
    d.line([(int(w * 0.86), int(h * 0.18)), (int(w * 0.98), int(h * 0.34))], fill=RED, width=3)


def illus_gavel(d, w, h):
    d.rectangle([0, 0, w, h], fill=(240, 238, 228))
    # base block
    d.rectangle([int(w * 0.20), int(h * 0.78), int(w * 0.80), int(h * 0.86)], fill=(101, 67, 33))
    # gavel head (tilted) + handle
    d.line([(int(w * 0.30), int(h * 0.62)), (int(w * 0.72), int(h * 0.30))], fill=(101, 67, 33), width=7)
    d.line([(int(w * 0.58), int(h * 0.16)), (int(w * 0.86), int(h * 0.34))], fill=(58, 58, 58), width=12)
    # impact lines
    for (x0, y0, x1, y1) in ((int(w * 0.14), int(h * 0.60), int(w * 0.24), int(h * 0.68)),
                             (int(w * 0.86), int(h * 0.58), int(w * 0.76), int(h * 0.66))):
        d.line([(x0, y0), (x1, y1)], fill=AMBER, width=3)


def illus_plane(d, w, h):
    d.rectangle([0, 0, w, int(h * 0.70)], fill=SKY)
    d.rectangle([0, int(h * 0.70), w, h], fill=(120, 160, 90))
    # forest triangles
    for fx in (0.08, 0.30, 0.52, 0.74, 0.92):
        x = int(w * fx)
        d.polygon([(x - 12, int(h * 0.98)), (x, int(h * 0.72)), (x + 12, int(h * 0.98))], fill=(46, 90, 46))
    # plane nose-down
    cx, cy = int(w * 0.52), int(h * 0.42)
    d.polygon([(cx - 34, cy - 6), (cx + 20, cy - 26), (cx + 40, cy - 8),
               (cx + 10, cy + 6), (cx - 20, cy + 10)], fill=(90, 90, 90))
    d.polygon([(cx - 8, cy - 4), (cx + 2, cy - 26), (cx + 10, cy - 4)], fill=(70, 70, 70))
    # smoke puffs
    for (sx, sy, sr) in ((int(w * 0.16), int(h * 0.22), 8), (int(w * 0.26), int(h * 0.14), 10),
                         (int(w * 0.38), int(h * 0.08), 7)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(180, 185, 190))


def illus_stocks(d, w, h):
    d.rectangle([0, 0, w, h], fill=(255, 255, 255))
    # grid
    for gy in range(int(h * 0.2), h, int(h * 0.2)):
        d.line([(0, gy), (w, gy)], fill=(230, 230, 230), width=1)
    # descending jagged line
    pts = [(4, int(h * 0.18)), (int(w * 0.20), int(h * 0.30)), (int(w * 0.38), int(h * 0.26)),
           (int(w * 0.55), int(h * 0.48)), (int(w * 0.72), int(h * 0.44)),
           (int(w * 0.88), int(h * 0.72)), (w - 6, int(h * 0.82))]
    d.line(pts, fill=RED, width=4, joint="curve")
    # down arrow at the end
    ex, ey = w - 14, int(h * 0.82)
    d.polygon([(ex - 8, ey - 12), (ex + 8, ey - 12), (ex, ey)], fill=RED)
    # small bars at the bottom
    for i, bh in enumerate((6, 10, 8, 14)):
        x = int(w * 0.12) + i * 12
        d.rectangle([x, h - 4 - bh, x + 7, h - 4], fill=(120, 120, 120))


def illus_crowd(d, w, h):
    d.rectangle([0, 0, w, h], fill=(240, 238, 228))
    # placard
    d.rectangle([int(w * 0.10), 8, int(w * 0.14), int(h * 0.52)], fill=(101, 67, 33))
    d.rectangle([int(w * 0.14), 8, int(w * 0.62), int(h * 0.30)], fill=(255, 255, 255), outline=NAVY, width=2)
    d.line([(int(w * 0.20), int(h * 0.19)), (int(w * 0.56), int(h * 0.19))], fill=RED, width=3)
    # crowd heads
    cols = [(185, 28, 28), (29, 78, 216), (15, 118, 110), (180, 83, 9), (157, 23, 77)]
    for i, c in enumerate(cols):
        cx = int(w * (0.16 + i * 0.17))
        cy = int(h * 0.68)
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=c)
        d.pieslice([cx - 11, cy + 6, cx + 11, h], 180, 360, fill=c)


def illus_resign(d, w, h):
    d.rectangle([0, 0, w, h], fill=(240, 238, 228))
    # paper with folded corner
    px, py, pw, ph = int(w * 0.18), int(h * 0.10), int(w * 0.64), int(h * 0.78)
    d.rectangle([px, py, px + pw, py + ph], fill=(255, 255, 255), outline=NAVY, width=2)
    d.polygon([(px + pw - 14, py), (px + pw, py + 14), (px + pw - 14, py + 14)], fill=(220, 220, 220))
    for i in range(4):
        ly = py + 16 + i * 12
        d.line([(px + 10, ly), (px + pw - 10, ly)], fill=(180, 180, 180), width=2)
    # signature squiggle
    d.line([(px + 12, py + ph - 14), (px + 22, py + ph - 20), (px + 32, py + ph - 12),
            (px + 44, py + ph - 18)], fill=NAVY, width=2)
    # red stamp
    d.rectangle([int(w * 0.52), int(h * 0.52), int(w * 0.92), int(h * 0.72)], outline=RED, width=3)
    d.line([(int(w * 0.52), int(h * 0.52)), (int(w * 0.92), int(h * 0.72))], fill=RED, width=2)


def illus_scales(d, w, h):
    d.rectangle([0, 0, w, h], fill=(240, 238, 228))
    cx = w // 2
    base_y = int(h * 0.86)
    d.rectangle([cx - 2, int(h * 0.14), cx + 2, base_y], fill=NAVY)
    d.rectangle([cx - 16, base_y, cx + 16, base_y + 4], fill=NAVY)
    d.ellipse([cx - 3, int(h * 0.08), cx + 3, int(h * 0.14)], fill=AMBER)
    d.rectangle([int(w * 0.14), int(h * 0.18), int(w * 0.86), int(h * 0.22)], fill=NAVY)
    for px in (int(w * 0.20), int(w * 0.80)):
        d.line([(px, int(h * 0.22)), (px - 8, int(h * 0.46))], fill=NAVY, width=2)
        d.line([(px, int(h * 0.22)), (px + 8, int(h * 0.46))], fill=NAVY, width=2)
        d.line([(px, int(h * 0.22)), (px, int(h * 0.46))], fill=NAVY, width=2)
        d.polygon([(px - 10, int(h * 0.46)), (px + 10, int(h * 0.46)), (px, int(h * 0.58))], fill=OLIVE)


def illus_gaza(d, w, h):
    d.rectangle([0, 0, w, h], fill=SKY)
    # buildings with a crack
    d.rectangle([int(w * 0.08), int(h * 0.30), int(w * 0.42), h], fill=(120, 120, 120))
    d.rectangle([int(w * 0.52), int(h * 0.18), int(w * 0.90), h], fill=(150, 150, 150))
    for (wx, wy) in ((int(w * 0.16), int(h * 0.42)), (int(w * 0.28), int(h * 0.42)),
                     (int(w * 0.60), int(h * 0.30)), (int(w * 0.74), int(h * 0.30))):
        d.rectangle([wx, wy, wx + 10, wy + 12], fill=(60, 60, 60))
    # jagged crack down the right building
    d.line([(int(w * 0.70), int(h * 0.18)), (int(w * 0.66), int(h * 0.40)),
            (int(w * 0.72), int(h * 0.60)), (int(w * 0.68), h)], fill=(60, 60, 60), width=3)
    # white flag on the left building
    d.rectangle([int(w * 0.22), int(h * 0.12), int(w * 0.24), int(h * 0.30)], fill=(58, 58, 58))
    d.polygon([(int(w * 0.24), int(h * 0.12)), (int(w * 0.40), int(h * 0.16)), (int(w * 0.24), int(h * 0.20))],
              fill=(255, 255, 255))


def illus_factory(d, w, h):
    d.rectangle([0, 0, w, int(h * 0.55)], fill=SKY)
    d.rectangle([0, int(h * 0.55), w, h], fill=(226, 220, 205))
    # factory with sawtooth roof + chimney
    d.rectangle([int(w * 0.10), int(h * 0.52), int(w * 0.78), int(h * 0.88)], fill=(150, 150, 150))
    for i in range(3):
        x0 = int(w * (0.10 + i * 0.23))
        d.polygon([(x0, int(h * 0.52)), (x0 + 11, int(h * 0.40)), (x0 + 23, int(h * 0.52))], fill=(120, 120, 120))
    d.rectangle([int(w * 0.80), int(h * 0.28), int(w * 0.88), int(h * 0.88)], fill=(100, 100, 100))
    for (sx, sy, sr) in ((int(w * 0.84), int(h * 0.20), 6), (int(w * 0.88), int(h * 0.12), 8)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(200, 205, 210))
    # worker heads at the gate
    for i, c in enumerate(((185, 28, 28), (29, 78, 216), (15, 118, 110))):
        cx = int(w * (0.22 + i * 0.18))
        d.ellipse([cx - 7, int(h * 0.90) - 7, cx + 7, int(h * 0.90) + 7], fill=c)


def illus_trains(d, w, h):
    d.rectangle([0, 0, w, h], fill=(240, 238, 228))
    # track
    d.rectangle([0, int(h * 0.62), w, int(h * 0.66)], fill=(90, 90, 90))
    # left train (nose right)
    d.rounded_rectangle([6, int(h * 0.34), int(w * 0.44), int(h * 0.62)], radius=6, fill=BLUE)
    for i in range(3):
        d.rectangle([14 + i * 18, int(h * 0.40), 26 + i * 18, int(h * 0.50)], fill=(255, 255, 255))
    # right train (nose left)
    d.rounded_rectangle([int(w * 0.56), int(h * 0.34), w - 6, int(h * 0.62)], radius=6, fill=RED)
    for i in range(3):
        d.rectangle([w - 26 - i * 18, int(h * 0.40), w - 14 - i * 18, int(h * 0.50)], fill=(255, 255, 255))
    # collision starburst
    cx, cy = w // 2, int(h * 0.48)
    for k in range(8):
        import math
        a = 2 * math.pi * k / 8
        d.line([(cx, cy), (cx + int(16 * math.cos(a)), cy + int(16 * math.sin(a)))],
               fill=(242, 201, 76), width=4)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(242, 201, 76))


def illus_cyclone(d, w, h):
    d.rectangle([0, 0, w, int(h * 0.72)], fill=SKY)
    d.rectangle([0, int(h * 0.72), w, h], fill=SEA)
    # spiral
    cx, cy = w // 2, int(h * 0.38)
    for r, a0, a1 in ((8, 0, 300), (16, 40, 340), (24, 80, 20), (32, 120, 60), (40, 160, 100)):
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=(255, 255, 255), width=4)
    # island + palm
    d.ellipse([int(w * 0.30), int(h * 0.74), int(w * 0.70), int(h * 0.86)], fill=(214, 164, 100))
    d.line([(int(w * 0.50), int(h * 0.76)), (int(w * 0.52), int(h * 0.60))], fill=(101, 67, 33), width=3)
    for (ex, ey) in ((int(w * 0.40), int(h * 0.58)), (int(w * 0.48), int(h * 0.54)),
                     (int(w * 0.56), int(h * 0.54)), (int(w * 0.64), int(h * 0.58))):
        d.line([(int(w * 0.52), int(h * 0.60)), (ex, ey)], fill=(77, 124, 15), width=3)
    # waves
    for wx in range(6, w - 16, 30):
        d.arc([wx, int(h * 0.90), wx + 24, int(h * 0.90) + 10], 180, 360, fill=(255, 255, 255), width=2)


ILLUS = {
    "bridge": illus_bridge, "radar": illus_radar, "flags4": illus_flags4,
    "measles": illus_measles, "cop31": illus_cop31, "gavel": illus_gavel,
    "plane": illus_plane, "stocks": illus_stocks, "crowd": illus_crowd,
    "resign": illus_resign, "scales": illus_scales, "gaza": illus_gaza,
    "factory": illus_factory, "trains": illus_trains, "cyclone": illus_cyclone,
}

# (number, tag, color, illustration, headline, body, source-tag)
TOP = [
    (1, "EUROPE · UKRAINE WAR", RED, "bridge",
     "Ukraine says a road span of the Crimean Bridge fell into the sea",
     "Second strike in two days; road and rail traffic halted; 2 killed; Kremlin vows to rebuild.",
     "CLAIM · KYIV"),
    (2, "MIDDLE EAST · IRAN WAR", BURGUNDY, "radar",
     "Iran sends drones at a US radar in Bahrain; US strikes Qeshm",
     "IRGC claims it destroyed a US early-warning radar in Bahrain (CENTCOM denies); US struck a rocket launch site on Qeshm Island; tankers hit mines in the Strait of Hormuz.",
     "CLAIMS · AP"),
    (3, "ASIA · DIPLOMACY", BLUE, "flags4",
     "Trump opens Asia trip in Manila with Quad and ASEAN talks",
     "US, India, Japan and Australia sign critical-minerals deals; next stop APEC in Shenzhen.",
     "CONFIRMED · AP"),
    (4, "AMERICAS · HEALTH", TEAL, "measles",
     "PAHO: US, Mexico and Bolivia lose measles-free status",
     "One ruling for all three; spread ran over a year; 5,400+ US cases.",
     "CONFIRMED · PAHO"),
]

MID1 = [
    (5, "EUROPE · CLIMATE", TEAL, "cop31",
     "COP31 splits over fossil-fuel phase-out",
     "EU calls the Antalya draft untenable; Arab Group rejects it."),
    (6, "AFRICA · JUSTICE", OLIVE, "gavel",
     "Mozambique's Mondlane goes on trial",
     "Opposition leader faces 5 charges over the 2024 post-election protests."),
    (7, "ASIA · AIR CRASH", NAVY, "plane",
     "Russian An-12 crashes in Siberia",
     "All 19 aboard killed near Kemerovo; officials say fault suspected."),
    (8, "GLOBAL · MARKETS", RED, "stocks",
     "Stocks slide; fear gauge jumps",
     "Dow about -1.5%; fear index up 12%; oil near $86."),
    (9, "EUROPE · LABOUR", BURGUNDY, "crowd",
     "France's public sector strikes over pay",
     "140,000 march by police count; CGT says 500,000."),
    (10, "ASIA · POLITICS", BLUE, "resign",
     "Mongolia's president to resign",
     "Khurelsukh quits amid a $25m railway bribe claim he denies."),
]

MID2 = [
    (11, "EUROPE · DIPLOMACY", BLUE, "scales",
     "UK sanctions 8 settlement builders",
     "Plus a settler group that blocked aid to Gaza."),
    (12, "MIDDLE EAST · CONFLICT", RED, "gaza",
     "Israeli strikes kill 5 in Gaza despite truce",
     "A child among the dead; settlers kill a woman, 72, in the West Bank."),
    (13, "ASIA · LABOUR", OLIVE, "factory",
     "Bangladesh garment workers clash with police",
     "Highways blocked; 37 factories shut over pay."),
    (14, "EUROPE · RAIL", NAVY, "trains",
     "Two trains collide head-on in Prague",
     "46 injured, four seriously, in the Czech capital."),
    (15, "OCEANIA · WEATHER", TEAL, "cyclone",
     "Cyclone Xavier bears down on Cook Islands",
     "Northern atolls brace as the storm strengthens."),
]


def draw_story(img, d, x, y, w, illus_h, story, head_size, body_size, max_head=4, max_body=3):
    if len(story) == 7:
        num, tag, color, illus_key, head, body, src = story
    else:
        num, tag, color, illus_key, head, body = story
        src = ""
    # illustration on a temp image so nothing spills past the box
    thumb = Image.new("RGB", (w, illus_h), PAPER)
    td = ImageDraw.Draw(thumb)
    ILLUS[illus_key](td, w, illus_h)
    img.paste(thumb, (x, y))
    d.rectangle([x, y, x + w, y + illus_h], outline=NAVY, width=1)
    ty = y + illus_h + 8
    f_num = font(SANS_BOLD, head_size - 2)
    f_tag = font(SANS_BOLD, head_size - 4)
    d.text((x, ty), str(num), font=f_num, fill=color)
    nw = d.textlength(str(num), font=f_num)
    d.text((x + nw + 5, ty + 1), tag, font=f_tag, fill=color)
    hy = ty + head_size + 4
    if src:
        # source tag on its own line under the tag (never overlapping it)
        f_src = font(SANS_BOLD, head_size - 6)
        d.text((x, hy), src, font=f_src, fill=GRAY)
        hy += head_size - 2
    f_head = font(SANS_BOLD, head_size)
    for ln in wrap(d, head, f_head, w, max_head):
        d.text((x, hy), ln, font=f_head, fill=INK)
        hy += head_size + 4
    f_body = font(SANS, body_size)
    for ln in wrap(d, body, f_body, w, max_body):
        d.text((x, hy), ln, font=f_body, fill=GRAY)
        hy += body_size + 4
    return hy


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # page border
    d.rectangle([4, 4, W - 5, H - 5], outline=INK, width=2)

    # ---- kicker line ---------------------------------------------------
    f_kick = font(SANS_BOLD, 14)
    d.text((MARGIN, 14), "ONE DAY OF WORLD NEWS, ONE PICTURE", font=f_kick, fill=RED)
    rk = "15 STORIES · 7 REGIONS · EVERY ONE FROM THIS TUESDAY"
    d.text((W - MARGIN - d.textlength(rk, font=f_kick), 14), rk, font=f_kick, fill=GRAY)

    # ---- masthead ------------------------------------------------------
    f_mast = font(SERIF_BOLD, 60)
    mast = "Tuesday 17 November 2026"
    d.text(((W - d.textlength(mast, font=f_mast)) / 2, 34), mast, font=f_mast, fill=INK)
    d.line([(MARGIN, 106), (W - MARGIN, 106)], fill=INK, width=3)

    # ---- timeline strip ------------------------------------------------
    ty0, ty1 = 116, 156
    d.rectangle([MARGIN, ty0, MARGIN + 92, ty1], fill=RED)
    f_tl = font(SANS_BOLD, 12)
    d.text((MARGIN + 8, ty0 + 5), "THE DAY", font=f_tl, fill=(255, 255, 255))
    d.text((MARGIN + 8, ty0 + 20), "IN UTC", font=f_tl, fill=(255, 255, 255))
    segs = [
        ("Overnight", "Crimean Bridge span falls"),
        ("~06:10 UTC", "Prague trains collide"),
        ("09:30 UTC", "Trump lands in Manila"),
        ("~14:30 UTC", "An-12 crashes near Kemerovo"),
        ("Day", "PAHO measles ruling; Paris marches"),
        ("Evening", "Wall St slides"),
    ]
    sx = MARGIN + 104
    sw = (W - MARGIN - sx - 6) // 6
    f_st = font(SANS_BOLD, 12)
    f_sl = font(SANS, 11)
    for i, (t, lab) in enumerate(segs):
        x = sx + i * sw
        d.text((x + 4, ty0 + 2), t, font=f_st, fill=INK)
        ly = ty0 + 18
        for ln in wrap(d, lab, f_sl, sw - 8, 2):
            d.text((x + 4, ly), ln, font=f_sl, fill=GRAY)
            ly += 13
        if i < 5:
            d.line([(x + sw - 2, ty0 + 2), (x + sw - 2, ty1 - 2)], fill=LIGHT_RULE, width=1)
    d.line([(MARGIN, 164), (W - MARGIN, 164)], fill=INK, width=2)

    # ---- top row: 4 large stories --------------------------------------
    gutter = 12
    col_w = (W - 2 * MARGIN - 3 * gutter) // 4
    y_top = 174
    illus_h_top = 100
    for i, st in enumerate(TOP):
        x = MARGIN + i * (col_w + gutter)
        draw_story(img, d, x, y_top, col_w, illus_h_top, st, 19, 12, 4, 6)
        if i < 3:
            d.line([(x + col_w + 6, y_top), (x + col_w + 6, y_top + 300)], fill=LIGHT_RULE, width=1)
    d.line([(MARGIN, 492), (W - MARGIN, 492)], fill=INK, width=2)

    # ---- middle row 1: 6 medium stories --------------------------------
    gutter6 = 10
    col6 = (W - 2 * MARGIN - 5 * gutter6) // 6
    y_mid1 = 504
    for i, st in enumerate(MID1):
        x = MARGIN + i * (col6 + gutter6)
        draw_story(img, d, x, y_mid1, col6, 78, st, 15, 12, 4, 3)
    d.line([(MARGIN, 712), (W - MARGIN, 712)], fill=INK, width=1)

    # ---- middle row 2: 5 medium stories --------------------------------
    gutter5 = 12
    col5 = (W - 2 * MARGIN - 4 * gutter5) // 5
    y_mid2 = 724
    for i, st in enumerate(MID2):
        x = MARGIN + i * (col5 + gutter5)
        draw_story(img, d, x, y_mid2, col5, 88, st, 16, 13, 4, 3)

    # ---- footer --------------------------------------------------------
    d.line([(MARGIN, 948), (W - MARGIN, 948)], fill=INK, width=2)
    f_src = font(SANS, 14)
    src = "Sources: AP · Reuters · AFP · Al Jazeera · PAHO — Original drawings."
    d.text(((W - d.textlength(src, font=f_src)) / 2, 960), src, font=f_src, fill=GRAY)
    f_note = font(SANS, 13)
    note = "Every story happened or was first reported on Tuesday 17 November 2026."
    d.text(((W - d.textlength(note, font=f_note)) / 2, 982), note, font=f_note, fill=GRAY)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
