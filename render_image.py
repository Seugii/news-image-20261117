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
        ("DIPLOMACY", BLUE,
         "Trump in Asia: Manila for ASEAN, then Shenzhen for APEC",
         "Trilateral nuclear talks with Xi and Putin set for Nov 19."),
        ("MIDDLE EAST", BURGUNDY,
         "Hormuz on edge: Iran drones at US radar in Bahrain intercepted",
         "Tankers hit mines; a third US carrier arrives in the Gulf."),
        ("ASIA-PACIFIC", TEAL,
         "Japan scrambles jets as suspected Russian aircraft violate airspace",
         "Tokyo calls the incursion a serious violation of sovereignty."),
        ("GAZA", OLIVE,
         "UK sanctions Israeli settlement firms",
         "West urges Israel to open Gaza aid crossings."),
        ("YEMEN", AMBER,
         "Houthis advance in Yemen; forces pull back to defend Aden",
         "Front lines shift as the port city braces for a siege."),
    ]
    f_stag = font(SANS_BOLD, 15)
    f_sh = font(SANS_BOLD, 23)
    f_ss = font(SANS, 17)
    y = 464
    for tag, color, head, summ in stories:
        d.rectangle([MARGIN, y, MARGIN + 8, y + 78], fill=color)
        d.text((MARGIN + 24, y), tag, font=f_stag, fill=color)
        hy = y + 21
        for ln in wrap(d, head, f_sh, W - MARGIN - (MARGIN + 24)):
            d.text((MARGIN + 24, hy), ln, font=f_sh, fill=INK)
            hy += 27
        for ln in wrap(d, summ, f_ss, W - MARGIN - (MARGIN + 24)):
            d.text((MARGIN + 24, hy), ln, font=f_ss, fill=GRAY)
            hy += 21
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
