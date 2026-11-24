#!/usr/bin/env python3
"""Compose the entry image for make.fun's news-image-20261124 bounty.

Draws a one-page broadsheet front page — "THE WORLD IN ONE DAY",
Tuesday 24 November 2026 — with Python + Pillow: a masthead, a 2x2 grid
of illustrated news panels, and a bottom ticker strip. The drawing is
fully deterministic (fixed geometry, fixed palette, fixed star seed), so
every run produces byte-identical output.

Usage: python3 compose.py [output-path]   (default: entry.png beside
this file)
"""

import os
import random
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- setup

W = H = 1024
MARGIN = 32
CONTENT_W = W - 2 * MARGIN

PAPER = (247, 241, 227)
INK = (26, 24, 20)
ACCENT = (142, 38, 24)
MUTED = (110, 100, 84)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(path, text, max_w, start):
    """Largest font (<= start px) whose rendered text fits max_w."""
    size = start
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    while size > 10:
        f = font(path, size)
        if probe.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return font(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured in pixels."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def center_text(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


# ------------------------------------------------------- illustrations
# Each illustration is drawn on its own layer (446x140) and pasted into
# its panel, so shapes can bleed to the layer edge without clipping
# logic.

ILLO_W, ILLO_H = 446, 140


def illo_icj():
    """Panel 1: courthouse with columns, and the scales of justice."""
    img = Image.new("RGB", (ILLO_W, ILLO_H), (223, 229, 234))
    d = ImageDraw.Draw(img)
    stone = (198, 205, 212)
    cx = ILLO_W // 2
    top = 12
    # pediment, entablature, columns, steps
    d.polygon([(cx - 128, top + 26), (cx + 128, top + 26), (cx, top)],
              fill=stone, outline=INK, width=2)
    d.rectangle([cx - 118, top + 28, cx + 118, top + 38], fill=stone,
                outline=INK, width=2)
    for i in range(5):
        x = cx - 100 + i * 50
        d.rectangle([x, top + 40, x + 14, top + 96], fill=stone,
                    outline=INK, width=2)
    d.rectangle([cx - 126, top + 98, cx + 126, top + 106], fill=stone,
                outline=INK, width=2)
    d.rectangle([cx - 138, top + 108, cx + 138, top + 116], fill=stone,
                outline=INK, width=2)
    d.rectangle([cx - 150, top + 118, cx + 150, top + 126], fill=stone,
                outline=INK, width=2)
    # scales of justice, silhouetted in front of the columns
    sy = 46                      # beam height
    base = 130                   # foot of the post
    d.line([cx, sy, cx, base], fill=INK, width=4)
    d.line([cx - 40, sy, cx + 40, sy], fill=INK, width=4)
    d.ellipse([cx - 4, sy - 5, cx + 4, sy + 3], fill=ACCENT)
    for sx in (cx - 40, cx + 40):
        d.line([sx, sy, sx - 15, sy + 22], fill=INK, width=2)
        d.line([sx, sy, sx + 15, sy + 22], fill=INK, width=2)
        d.arc([sx - 17, sy + 14, sx + 17, sy + 34], 0, 180, fill=INK,
              width=3)
        d.line([sx - 17, sy + 24, sx + 17, sy + 24], fill=INK, width=2)
    d.line([cx - 14, base, cx + 14, base], fill=INK, width=4)
    return img


def illo_nato():
    """Panel 2: satellite and shield above the arc of the Earth."""
    img = Image.new("RGB", (ILLO_W, ILLO_H), (20, 38, 63))
    d = ImageDraw.Draw(img)
    rng = random.Random(20261124)  # fixed seed: same stars every run
    for _ in range(80):
        x, y = rng.uniform(0, ILLO_W), rng.uniform(0, ILLO_H)
        r = rng.choice((1, 1, 2))
        d.ellipse([x - r, y - r, x + r, y + r], fill=(235, 238, 245))
    # Earth: a great circle whose top arc crosses the lower frame
    d.ellipse([ILLO_W - 330, 74, ILLO_W + 130, 534], fill=(61, 110, 165))
    d.ellipse([ILLO_W - 250, 96, ILLO_W - 130, 140], fill=(96, 142, 96))
    d.ellipse([ILLO_W - 90, 116, ILLO_W + 30, 156], fill=(96, 142, 96))
    d.ellipse([ILLO_W - 190, 128, ILLO_W - 90, 160], fill=(150, 160, 110))
    # satellite, upper left: gold body, blue panel wings with grid
    bx, by = 118, 40
    for px in (bx - 74, bx + 28):
        d.rectangle([px, by - 4, px + 46, by + 24], fill=(70, 110, 180),
                    outline=(220, 226, 235), width=1)
        for gx in range(px + 11, px + 46, 11):
            d.line([gx, by - 4, gx, by + 24], fill=(220, 226, 235))
        d.line([px, by + 10, px + 46, by + 10], fill=(220, 226, 235))
    d.rectangle([bx - 28, by + 6, bx, by + 14], fill=(200, 205, 215))
    d.rectangle([bx, by + 6, bx + 28, by + 14], fill=(200, 205, 215))
    d.rectangle([bx - 13, by - 6, bx + 13, by + 26], fill=(216, 178, 90),
                outline=(240, 240, 240), width=1)
    d.ellipse([bx - 4, by + 30, bx + 4, by + 38], fill=(240, 240, 240))
    # shield with a star, right of centre
    sx, sy = 268, 26
    shield = [(sx, sy), (sx + 52, sy), (sx + 52, sy + 38),
              (sx + 26, sy + 66), (sx, sy + 38)]
    d.polygon(shield, outline=(242, 238, 224), width=3)
    center_text(d, sx + 26, sy + 12, "★", font(SANS, 30), ACCENT)
    return img


def illo_hormuz():
    """Panel 3: a tanker threads the strait; a warship keeps watch."""
    img = Image.new("RGB", (ILLO_W, ILLO_H), (242, 227, 194))
    d = ImageDraw.Draw(img)
    sea_y = 62
    d.rectangle([0, sea_y, ILLO_W, ILLO_H], fill=(46, 111, 121))
    for wx, wy in ((60, 118), (180, 128), (330, 120), (120, 92), (268, 100)):
        d.line([wx, wy, wx + 26, wy], fill=(120, 180, 186), width=2)
    d.ellipse([26, 12, 58, 44], fill=(240, 200, 90))  # sun
    rock = (176, 137, 84)
    d.polygon([(0, 40), (132, 66), (116, ILLO_H), (0, ILLO_H)], fill=rock)
    d.polygon([(ILLO_W, 34), (318, 62), (330, ILLO_H), (ILLO_W, ILLO_H)],
              fill=rock)
    d.line([6, 74, 108, 92], fill=(140, 106, 62), width=3)
    d.line([ILLO_W - 8, 70, 344, 88], fill=(140, 106, 62), width=3)
    # tanker in the channel
    cx, wy = 224, 96
    d.polygon([(cx - 74, wy), (cx + 74, wy), (cx + 58, wy + 20),
               (cx - 58, wy + 20)], fill=(120, 50, 40))
    d.rectangle([cx - 66, wy - 10, cx + 66, wy], fill=(90, 60, 48))
    box_cols = [(70, 110, 180), (178, 110, 60), (96, 142, 96),
                (200, 160, 70)]
    for i, col in enumerate(box_cols):
        x = cx - 52 + i * 27
        d.rectangle([x, wy - 26, x + 24, wy - 11], fill=col,
                    outline=INK, width=1)
    d.rectangle([cx + 44, wy - 34, cx + 62, wy - 10], fill=(238, 234, 224),
                outline=INK, width=1)  # bridge tower
    d.line([cx - 58, wy - 10, cx - 58, wy - 30], fill=INK, width=2)
    # warship silhouette, lower right foreground
    gx, gy = 356, 112
    d.polygon([(gx - 52, gy), (gx + 56, gy), (gx + 42, gy + 14),
               (gx - 38, gy + 14)], fill=(58, 63, 70))
    d.rectangle([gx - 8, gy - 14, gx + 22, gy], fill=(58, 63, 70))
    d.rectangle([gx + 26, gy - 9, gx + 38, gy], fill=(58, 63, 70))
    d.line([gx + 6, gy - 14, gx + 6, gy - 30], fill=(58, 63, 70), width=3)
    d.line([gx - 30, gy - 6, gx - 8, gy - 6], fill=(58, 63, 70), width=3)
    return img


def illo_drone():
    """Panel 4: a surveillance drone circles over a desert town."""
    img = Image.new("RGB", (ILLO_W, ILLO_H), (246, 221, 186))
    d = ImageDraw.Draw(img)
    d.ellipse([ILLO_W - 66, 10, ILLO_W - 30, 46], fill=(240, 190, 80))
    ground_y = 96
    d.polygon([(0, ground_y + 12), (150, ground_y - 4), (320, ground_y + 8),
               (ILLO_W, ground_y - 2), (ILLO_W, ILLO_H), (0, ILLO_H)],
              fill=(217, 160, 95))
    # town: flat-roofed houses and one church tower along the ground
    houses = [(18, 22, 20), (48, 30, 26), (84, 24, 18), (150, 34, 24),
              (196, 26, 20), (300, 32, 26), (342, 24, 18), (376, 30, 22),
              (412, 22, 18)]
    for hx, hw, hh in houses:
        base = ILLO_H - 4
        d.rectangle([hx, base - hh, hx + hw, base], fill=(240, 235, 220),
                    outline=(150, 110, 70), width=1)
        d.rectangle([hx - 2, base - hh - 4, hx + hw + 2, base - hh],
                    fill=(178, 128, 80))
        d.rectangle([hx + hw // 2 - 2, base - 10, hx + hw // 2 + 2,
                     base - 4], fill=(90, 70, 50))
    tx = 240  # church tower
    d.rectangle([tx, ILLO_H - 52, tx + 18, ILLO_H - 4], fill=(240, 235, 220),
                outline=(150, 110, 70), width=1)
    d.polygon([(tx - 3, ILLO_H - 52), (tx + 21, ILLO_H - 52),
               (tx + 9, ILLO_H - 70)], fill=(150, 60, 40))
    # dashed surveillance ring on the town
    ring = [196, ILLO_H - 34, 330, ILLO_H + 6]
    for a in range(0, 360, 14):
        d.arc(ring, a, a + 8, fill=ACCENT, width=2)
    # quadcopter drone, dark silhouette in the sky
    cx, cy = 150, 42
    for dx, dy in ((-52, -18), (52, -18), (-52, 18), (52, 18)):
        d.line([cx, cy, cx + dx, cy + dy], fill=INK, width=4)
        d.ellipse([cx + dx - 17, cy + dy - 4, cx + dx + 17, cy + dy + 4],
                  outline=INK, width=3)
    d.ellipse([cx - 24, cy - 11, cx + 24, cy + 11], fill=INK)
    d.ellipse([cx - 5, cy + 9, cx + 5, cy + 19], fill=INK)
    d.ellipse([cx - 2, cy + 13, cx + 2, cy + 17], fill=ACCENT)
    return img


# ---------------------------------------------------------------- news

PANELS = [
    {
        "illo": illo_icj,
        "headline": "ICJ FINDS MYANMAR GUILTY OF GENOCIDE",
        "caption": ("World Court rules 9–6 that Myanmar's 2017 campaign "
                    "against the Rohingya was genocide — the first time "
                    "the ICJ has held a state responsible. A precedent "
                    "for the Gaza case."),
    },
    {
        "illo": illo_nato,
        "headline": "NATO VOWS DEFENCE AGAINST SPACE THREAT",
        "caption": ("Allies brace as reports say Russia could orbit a "
                    "nuclear-armed satellite within 60 days, after a "
                    "year of airspace violations across the alliance."),
    },
    {
        "illo": illo_hormuz,
        "headline": "HORMUZ TENSIONS FLARE",
        "caption": ("Britain logs fresh Iranian attacks in the Strait "
                    "of Hormuz as Trump warns Tehran of a 'very "
                    "traumatic' outcome if nuclear talks fail."),
    },
    {
        "illo": illo_drone,
        "headline": "US DRONE HELPS MEXICO CAPTURE 'EL CHAPO ISIDRO'",
        "caption": ("Cartel boss Fausto Isidro Meza Flores is seized in "
                    "Sinaloa with help from a US surveillance drone; "
                    "Mexico insists he will stand trial at home."),
    },
]

TICKER_ITEMS = [
    "Oregon & Virginia sue SpaceX over alleged Grok-generated abuse images",
    "UN chief Guterres demands global AI-risk framework within a year",
    "Magnitude 5.6 earthquake strikes Nepal near China border",
    "Pennsylvania measles epidemic claims a ninth death",
    "China opens Tiangong station to first foreign astronaut, "
    "Pakistan's Zeeshan Ali",
    "Bangladesh begins typhoid vaccination drive for 50 million children",
]

# ------------------------------------------------------------- layout

PANEL_TOP = 216
PANEL_H = 328
PANEL_GAP = 20
PANEL_W = (CONTENT_W - PANEL_GAP) // 2


def draw_masthead(d):
    center_text(d, W // 2, 26, "THE DAILY NEWS SUMMARY — ONE PAGE, "
                "THE WHOLE PLANET", font(SANS_BOLD, 16), MUTED)
    d.line([MARGIN, 54, W - MARGIN, 54], fill=INK, width=2)
    title_f = fit_font(SERIF_BOLD, "THE WORLD IN ONE DAY", CONTENT_W, 92)
    center_text(d, W // 2, 66, "THE WORLD IN ONE DAY", title_f, INK)
    center_text(d, W // 2, 160, "TUESDAY 24 NOVEMBER 2026",
                font(SANS_BOLD, 27), ACCENT)
    d.line([MARGIN, 198, W - MARGIN, 198], fill=INK, width=5)
    d.line([MARGIN, 207, W - MARGIN, 207], fill=INK, width=1)


def draw_panel(d, page, x, y, panel):
    d.rectangle([x, y, x + PANEL_W, y + PANEL_H], outline=INK, width=2)
    page.paste(panel["illo"](), (x + 12, y + 12))
    d.rectangle([x + 12, y + 12, x + 12 + ILLO_W, y + 12 + ILLO_H],
                outline=MUTED, width=1)
    # Headlines get two lines: shrink the font until the wrap fits.
    head_f = font(SERIF_BOLD, 27)
    head_lines = wrap(d, panel["headline"], head_f, PANEL_W - 24)
    size = 27
    while len(head_lines) > 2 and size > 18:
        size -= 1
        head_f = font(SERIF_BOLD, size)
        head_lines = wrap(d, panel["headline"], head_f, PANEL_W - 24)
    for i, line in enumerate(head_lines):
        d.text((x + 12, y + 160 + i * 34), line, font=head_f, fill=INK)
    cap_f = font(SANS, 18)
    for i, line in enumerate(wrap(d, panel["caption"], cap_f,
                                  PANEL_W - 24)):
        d.text((x + 12, y + 234 + i * 23), line, font=cap_f, fill=INK)


def draw_ticker(d):
    d.line([MARGIN, 906, W - MARGIN, 906], fill=INK, width=2)
    d.text((MARGIN, 916), "ALSO IN THE NEWS",
           font=font(SANS_BOLD, 15), fill=ACCENT)
    text = "  •  ".join(TICKER_ITEMS)
    tick_f = font(SANS, 16)
    for i, line in enumerate(wrap(d, text, tick_f, CONTENT_W)):
        d.text((MARGIN, 940 + i * 20), line, font=tick_f, fill=INK)


def build():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)
    draw_masthead(d)
    for i, panel in enumerate(PANELS):
        x = MARGIN + (i % 2) * (PANEL_W + PANEL_GAP)
        y = PANEL_TOP + (i // 2) * (PANEL_H + PANEL_GAP)
        draw_panel(d, page, x, y, panel)
    draw_ticker(d)
    return page


def main():
    if len(sys.argv) > 1:
        out = sys.argv[1]
    else:
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "entry.png")
    img = build()
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out}: {img.size[0]}x{img.size[1]}, "
          f"{os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
