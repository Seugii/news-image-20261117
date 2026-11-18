#!/usr/bin/env python3
"""Render the entry image for make.fun news-image-20261117.

Draws a 1024x1024 newspaper front page summing up the world news of
Tuesday 17 November 2026, using only PIL. No network, no AI generation:
every glyph is placed by this script so the text is exact and legible.
Output: entry.png beside this file (1024x1024 PNG, <= 1 MiB).
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 36

PAPER = (250, 246, 236)      # warm newsprint
INK = (26, 26, 26)           # near-black
NAVY = (22, 35, 63)          # masthead / headlines
GRAY = (85, 85, 85)
LIGHT_RULE = (200, 192, 175)
RED = (185, 28, 28)
BLUE = (29, 78, 216)
BURGUNDY = (157, 23, 77)
TEAL = (15, 118, 110)
OLIVE = (77, 124, 15)
AMBER = (180, 83, 9)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
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
    return lines


def draw_bridge(draw, x0, y0, w, h):
    """Schematic suspension bridge with a collapsed middle span."""
    sky = (188, 214, 232)
    sea = (47, 110, 142)
    deck_y = y0 + 118
    sea_y = y0 + 152
    draw.rectangle([x0, y0, x0 + w, sea_y], fill=sky)
    draw.rectangle([x0, sea_y, x0 + w, y0 + h], fill=sea)
    # sun
    draw.ellipse([x0 + 34, y0 + 22, x0 + 70, y0 + 58], fill=(242, 201, 76))
    # waves
    for wy in (sea_y + 26, sea_y + 62, sea_y + 92):
        for wx in range(x0 + 8, x0 + w - 20, 44):
            draw.arc([wx, wy, wx + 36, wy + 14], 180, 360, fill=(255, 255, 255), width=2)
    # towers
    for tx in (x0 + 96, x0 + 216):
        draw.rectangle([tx, y0 + 34, tx + 12, deck_y], fill=(58, 58, 58))
    # cables
    for tx in (x0 + 102, x0 + 222):
        draw.line([(tx, y0 + 34), (x0 + 10, deck_y)], fill=(90, 90, 90), width=2)
        draw.line([(tx, y0 + 34), (x0 + w - 10, deck_y)], fill=(90, 90, 90), width=2)
    # deck segments (gap in the middle: the collapsed span)
    draw.rectangle([x0 + 8, deck_y, x0 + 138, deck_y + 8], fill=(43, 43, 43))
    draw.rectangle([x0 + 186, deck_y, x0 + w - 8, deck_y + 8], fill=(43, 43, 43))
    # fallen span, tilted into the sea
    draw.polygon([(x0 + 138, deck_y), (x0 + 182, deck_y + 2),
                  (x0 + 172, deck_y + 26), (x0 + 130, deck_y + 22)],
                 fill=(43, 43, 43))
    # debris in the water
    for dx, dy in ((x0 + 150, sea_y + 8), (x0 + 168, sea_y + 16), (x0 + 142, sea_y + 20)):
        draw.rectangle([dx, dy, dx + 10, dy + 4], fill=(43, 43, 43))
    # smoke + flame at the break
    draw.ellipse([x0 + 142, deck_y - 28, x0 + 164, deck_y - 8], fill=(154, 165, 177))
    draw.ellipse([x0 + 154, deck_y - 40, x0 + 174, deck_y - 20], fill=(170, 180, 190))
    draw.polygon([(x0 + 156, deck_y), (x0 + 164, deck_y - 16), (x0 + 172, deck_y)],
                 fill=(232, 89, 12))
    # frame
    draw.rectangle([x0, y0, x0 + w, y0 + h], outline=NAVY, width=2)


def draw_flags(draw, x0, y0, w, h):
    """Three small flags (US, China, Russia) on poles — trilateral talks."""
    sky = (188, 214, 232)
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=sky)
    draw.rectangle([x0, y0 + h - 8, x0 + w, y0 + h], fill=(226, 220, 205))
    for px in (x0 + 10, x0 + 40, x0 + 70):
        draw.rectangle([px, y0 + 12, px + 2, y0 + h - 8], fill=(58, 58, 58))
        draw.ellipse([px - 2, y0 + 8, px + 4, y0 + 14], fill=(242, 201, 76))
    fy, fw, fh = y0 + 12, 20, 15
    # US flag: stripes + blue canton
    fx = x0 + 14
    for i in range(5):
        draw.rectangle([fx, fy + i * 3, fx + fw, fy + i * 3 + 3],
                       fill=(185, 28, 28) if i % 2 == 0 else (255, 255, 255))
    draw.rectangle([fx, fy, fx + 10, fy + 8], fill=(29, 78, 216))
    for dx, dy in ((2, 2), (6, 2), (2, 5), (6, 5)):
        draw.ellipse([fx + dx, fy + dy, fx + dx + 1, fy + dy + 1], fill=(255, 255, 255))
    # China flag: red field, yellow stars
    fx = x0 + 44
    draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16))
    draw.ellipse([fx + 3, fy + 3, fx + 7, fy + 7], fill=(255, 222, 89))
    for dx, dy in ((12, 2), (16, 5), (12, 9), (17, 9)):
        draw.ellipse([fx + dx, fy + dy, fx + dx + 2, fy + dy + 2], fill=(255, 222, 89))
    # Russia flag: white / blue / red bands
    fx = x0 + 74
    for i, c in enumerate(((255, 255, 255), (29, 78, 216), (222, 41, 16))):
        draw.rectangle([fx, fy + i * 5, fx + fw, fy + i * 5 + 5], fill=c)
    draw.rectangle([x0, y0, x0 + w, y0 + h], outline=NAVY, width=2)


def draw_tanker(draw, x0, y0, w, h):
    """Oil tanker on waves — Strait of Hormuz."""
    sky = (188, 214, 232)
    sea = (47, 110, 142)
    draw.rectangle([x0, y0, x0 + w, y0 + 42], fill=sky)
    draw.rectangle([x0, y0 + 42, x0 + w, y0 + h], fill=sea)
    draw.ellipse([x0 + 10, y0 + 10, x0 + 26, y0 + 26], fill=(242, 201, 76))
    hy = y0 + 38
    # hull (bow to the right)
    draw.polygon([(x0 + 8, hy), (x0 + 66, hy), (x0 + 88, hy + 10),
                  (x0 + 8, hy + 10)], fill=(43, 43, 43))
    # burgundy stripe along the hull
    draw.polygon([(x0 + 8, hy + 3), (x0 + 66, hy + 3), (x0 + 72, hy + 6),
                  (x0 + 8, hy + 6)], fill=(157, 23, 77))
    # deck cargo containers
    draw.rectangle([x0 + 40, hy - 8, x0 + 62, hy], fill=(90, 90, 90))
    # superstructure at the stern
    draw.rectangle([x0 + 12, hy - 16, x0 + 32, hy], fill=(255, 255, 255))
    draw.rectangle([x0 + 12, hy - 16, x0 + 32, hy - 12], fill=(157, 23, 77))
    # funnel with smoke
    draw.rectangle([x0 + 34, hy - 20, x0 + 40, hy], fill=(58, 58, 58))
    draw.ellipse([x0 + 30, hy - 28, x0 + 40, hy - 20], fill=(200, 205, 210))
    draw.ellipse([x0 + 34, hy - 34, x0 + 42, hy - 27], fill=(214, 218, 222))
    # waves
    for wy in (y0 + 58, y0 + 68):
        for wx in range(x0 + 6, x0 + w - 18, 34):
            draw.arc([wx, wy, wx + 28, wy + 10], 180, 360, fill=(255, 255, 255), width=2)
    draw.rectangle([x0, y0, x0 + w, y0 + h], outline=NAVY, width=2)


def draw_jet(draw, x0, y0, w, h):
    """Fighter-jet silhouette in the sky, red sun (Japan)."""
    sky = (188, 214, 232)
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=sky)
    draw.ellipse([x0 + w - 24, y0 + 10, x0 + w - 8, y0 + 26], fill=(185, 28, 28))
    for cx, cy in ((x0 + 8, y0 + 14), (x0 + 30, y0 + 58), (x0 + 58, y0 + 62)):
        draw.ellipse([cx, cy, cx + 18, cy + 8], fill=(255, 255, 255))
    cy = y0 + h // 2
    for ly in (cy - 14, cy + 12):
        draw.line([(x0 + 6, ly), (x0 + 20, ly)], fill=(255, 255, 255), width=2)
    # jet silhouette, nose to the right
    draw.polygon([(x0 + 16, cy - 3), (x0 + 56, cy - 5), (x0 + 86, cy),
                  (x0 + 56, cy + 5), (x0 + 16, cy + 3)], fill=NAVY)
    draw.polygon([(x0 + 38, cy - 4), (x0 + 52, cy - 22), (x0 + 58, cy - 4)], fill=NAVY)
    draw.polygon([(x0 + 40, cy + 4), (x0 + 52, cy + 16), (x0 + 58, cy + 4)], fill=NAVY)
    draw.polygon([(x0 + 18, cy - 3), (x0 + 24, cy - 15), (x0 + 30, cy - 3)], fill=NAVY)
    draw.rectangle([x0, y0, x0 + w, y0 + h], outline=NAVY, width=2)


def draw_scales(draw, x0, y0, w, h):
    """Scales of justice — sanctions / the law."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(240, 238, 228))
    cx = x0 + w // 2
    base_y = y0 + h - 10
    draw.rectangle([cx - 3, y0 + 16, cx + 3, base_y], fill=NAVY)
    draw.rectangle([cx - 18, base_y, cx + 18, base_y + 4], fill=NAVY)
    draw.ellipse([cx - 4, y0 + 9, cx + 4, y0 + 17], fill=(180, 83, 9))
    draw.rectangle([x0 + 14, y0 + 20, x0 + w - 14, y0 + 24], fill=NAVY)
    for px in (x0 + 18, x0 + w - 18):
        draw.line([(px, y0 + 24), (px - 9, y0 + 46)], fill=NAVY, width=2)
        draw.line([(px, y0 + 24), (px + 9, y0 + 46)], fill=NAVY, width=2)
        draw.line([(px, y0 + 24), (px, y0 + 46)], fill=NAVY, width=2)
        draw.polygon([(px - 11, y0 + 46), (px + 11, y0 + 46), (px, y0 + 58)],
                     fill=(77, 124, 15))
    draw.rectangle([x0, y0, x0 + w, y0 + h], outline=NAVY, width=2)


def draw_desert(draw, x0, y0, w, h):
    """Desert dunes, mountains and a palm — Yemen."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(245, 222, 179))
    draw.ellipse([x0 + 66, y0 + 8, x0 + 88, y0 + 30], fill=(232, 140, 40))
    draw.polygon([(x0, y0 + 52), (x0 + 30, y0 + 24), (x0 + 60, y0 + 52)],
                 fill=(150, 110, 70))
    draw.polygon([(x0 + 42, y0 + 52), (x0 + 72, y0 + 30), (x0 + w, y0 + 52)],
                 fill=(130, 95, 60))
    draw.ellipse([x0 - 24, y0 + 46, x0 + 58, y0 + 88], fill=(214, 164, 100))
    draw.ellipse([x0 + 38, y0 + 54, x0 + w + 24, y0 + 94], fill=(196, 144, 82))
    # palm tree
    draw.line([(x0 + 24, y0 + 74), (x0 + 28, y0 + 46)], fill=(101, 67, 33), width=3)
    for ex, ey in ((x0 + 10, y0 + 38), (x0 + 18, y0 + 32), (x0 + 28, y0 + 30),
                   (x0 + 38, y0 + 32), (x0 + 46, y0 + 38)):
        draw.line([(x0 + 28, y0 + 46), (ex, ey)], fill=(77, 124, 15), width=3)
    draw.rectangle([x0, y0, x0 + w, y0 + h], outline=NAVY, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead band -------------------------------------------------
    d.rectangle([0, 0, W, 110], fill=NAVY)
    f_mast = font(SERIF_BOLD, 56)
    t = "THE WORLD IN ONE PAGE"
    d.text(((W - d.textlength(t, font=f_mast)) / 2, 20), t, font=f_mast, fill=(255, 255, 255))
    f_sub = font(SANS, 16)
    s = "WORLD NEWS  ·  SUMMED UP IN A SINGLE IMAGE"
    d.text(((W - d.textlength(s, font=f_sub)) / 2, 82), s, font=f_sub, fill=(201, 210, 224))

    # ---- date strip ----------------------------------------------------
    f_date = font(SANS_BOLD, 27)
    dt = "TUESDAY, 17 NOVEMBER 2026"
    d.text(((W - d.textlength(dt, font=f_date)) / 2, 120), dt, font=f_date, fill=NAVY)
    d.line([(0, 152), (W, 152)], fill=INK, width=3)
    d.line([(0, 157), (W, 157)], fill=INK, width=1)

    # ---- lead story ----------------------------------------------------
    # tag pill
    f_tag = font(SANS_BOLD, 17)
    tag = "WAR IN UKRAINE"
    tw = d.textlength(tag, font=f_tag)
    d.rectangle([MARGIN, 172, MARGIN + tw + 22, 172 + 30], fill=RED)
    d.text((MARGIN + 11, 177), tag, font=f_tag, fill=(255, 255, 255))

    # headline (wrapped, max 3 lines)
    f_head = font(SANS_BOLD, 38)
    head = "Ukraine strikes Crimea bridge — span collapses; Russia hits Kyiv bridges in reply"
    lines = wrap(d, head, f_head, 600)
    y = 212
    for ln in lines:
        d.text((MARGIN, y), ln, font=f_head, fill=NAVY)
        y += 46

    # summary
    f_sum = font(SANS, 20)
    summ = ("Kyiv says the Kerch crossing is down; Moscow answers with strikes "
            "on bridges in the capital — the sharpest exchange of the war.")
    for ln in wrap(d, summ, f_sum, 600):
        d.text((MARGIN, y), ln, font=f_sum, fill=(51, 51, 51))
        y += 27

    # bridge illustration, right of the lead text
    draw_bridge(d, 664, 168, 324, 260)

    # ---- double rule ---------------------------------------------------
    d.line([(0, 444), (W, 444)], fill=INK, width=3)
    d.line([(0, 449), (W, 449)], fill=INK, width=1)

    # ---- supporting stories --------------------------------------------
    stories = [
        ("DIPLOMACY", BLUE, draw_flags,
         "Trump in Asia: Manila for ASEAN, then Shenzhen for APEC",
         "Trilateral nuclear talks with Xi and Putin set for Nov 19."),
        ("MIDDLE EAST", BURGUNDY, draw_tanker,
         "Hormuz on edge: Iran drones at US radar in Bahrain intercepted",
         "Tankers hit mines; a third US carrier arrives in the Gulf."),
        ("ASIA-PACIFIC", TEAL, draw_jet,
         "Japan scrambles jets as suspected Russian aircraft violate airspace",
         "Tokyo calls the incursion a serious violation of sovereignty."),
        ("GAZA", OLIVE, draw_scales,
         "UK sanctions Israeli settlement firms",
         "West urges Israel to open Gaza aid crossings."),
        ("YEMEN", AMBER, draw_desert,
         "Houthis advance in Yemen; forces pull back to defend Aden",
         "Front lines shift as the port city braces for a siege."),
    ]
    f_stag = font(SANS_BOLD, 15)
    f_sh = font(SANS_BOLD, 22)
    f_ss = font(SANS, 17)
    THUMB_W, THUMB_H = 96, 78
    THUMB_X = W - MARGIN - THUMB_W
    TEXT_W = THUMB_X - 12 - (MARGIN + 24)
    y = 464
    for tag, color, illus, head, summ in stories:
        d.rectangle([MARGIN, y, MARGIN + 8, y + 78], fill=color)
        d.text((MARGIN + 24, y), tag, font=f_stag, fill=color)
        hy = y + 21
        for ln in wrap(d, head, f_sh, TEXT_W):
            d.text((MARGIN + 24, hy), ln, font=f_sh, fill=INK)
            hy += 26
        for ln in wrap(d, summ, f_ss, TEXT_W):
            d.text((MARGIN + 24, hy), ln, font=f_ss, fill=GRAY)
            hy += 21
        # thumbnail: render on a temp image so nothing can spill past
        # the panel bounds, then paste it into the row
        thumb = Image.new("RGB", (THUMB_W, THUMB_H), PAPER)
        td = ImageDraw.Draw(thumb)
        illus(td, 0, 0, THUMB_W, THUMB_H)
        img.paste(thumb, (THUMB_X, y))
        y += 96
        if y < 940:
            d.line([(MARGIN, y - 10), (W - MARGIN, y - 10)], fill=LIGHT_RULE, width=1)

    # ---- footer: also strip + sources ----------------------------------
    d.line([(0, 944), (W, 944)], fill=INK, width=2)
    f_also_tag = font(SANS_BOLD, 16)
    f_also = font(SANS, 16)
    also = ("Europe: five nations plan a Rwanda return hub for rejected asylum "
            "seekers. ULA Vulcan rocket fails — 40 Amazon satellites lost.")
    d.text((MARGIN, 954), "ALSO", font=f_also_tag, fill=RED)
    ax = MARGIN + 58
    ay = 954
    for ln in wrap(d, also, f_also, W - MARGIN - ax):
        d.text((ax, ay), ln, font=f_also, fill=(51, 51, 51))
        ay += 21
    f_src = font(SANS, 14)
    src = "Sources: BBC  ·  Reuters  ·  AP  ·  Just Security  —  17 November 2026"
    d.text(((W - d.textlength(src, font=f_src)) / 2, 1000), src, font=f_src, fill=GRAY)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
