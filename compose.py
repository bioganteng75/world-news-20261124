#!/usr/bin/env python3
"""Compose the v2 front page for Tuesday 24 November 2026.

Denser edition: 4 hero panels + 28 one-line briefs (32 stories) + a
markets strip. All geometry is fixed; no timestamps, no randomness, so
running this twice produces byte-identical PNG output.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 28                      # page margin
CW = W - 2 * M              # content width (968)
PAPER = (247, 242, 231)
INK = (24, 22, 20)
RED = (168, 32, 26)
MUTED = (112, 102, 88)
SKY = (214, 228, 238)
NAVY = (16, 28, 54)
TEAL = (38, 110, 118)
SAND = (206, 178, 132)
DESERT = (232, 205, 160)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, int(round(size)))


def text_w(draw, text, f):
    return draw.textlength(text, font=f)


def wrap(draw, text, f, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, f, max_w, max_lines):
    """Wrap text; if it needs more than max_lines, shrink the font."""
    size = f.size
    while size > 10:
        lines = wrap(draw, text, font(f.path, size), max_w)
        if len(lines) <= max_lines:
            return lines, font(f.path, size)
        size -= 1
    return wrap(draw, text, font(f.path, size), max_w), font(f.path, size)


def center(draw, cx, y, text, f, fill):
    draw.text((cx - text_w(draw, text, f) / 2, y), text, font=f, fill=fill)


def rule(draw, x0, x1, y, wdt, fill=INK):
    draw.rectangle([x0, y, x1, y + wdt - 1], fill=fill)


# ---------------------------------------------------------------- illustrations
def draw_courthouse(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(196, 190, 176))
    # pediment
    d.polygon([(x + 30, y + 34), (x + w - 30, y + 34), (x + w / 2, y + 8)],
              fill=(228, 226, 220), outline=INK)
    d.rectangle([x + 30, y + 34, x + w - 30, y + 44], fill=(228, 226, 220),
                outline=INK)
    # columns
    for i in range(4):
        cx0 = x + 40 + i * 122
        d.rectangle([cx0, y + 44, cx0 + 18, y + h - 26], fill=(226, 224, 218),
                    outline=(90, 88, 84))
    # steps
    for i, sw in enumerate((w - 40, w - 70, w - 100)):
        d.rectangle([x + (w - sw) / 2, y + h - 26 + i * 5,
                     x + (w + sw) / 2, y + h - 21 + i * 5],
                    fill=(210, 206, 196), outline=INK)
    # scales of justice, silhouetted in front
    cx, top, base = x + w / 2, y + 22, y + h - 14
    d.line([(cx, top), (cx, base)], fill=INK, width=4)
    d.line([(cx - 40, top + 12), (cx + 40, top + 12)], fill=INK, width=4)
    d.polygon([(cx - 7, top - 5), (cx + 7, top - 5), (cx, top + 4)], fill=RED)
    for sx in (cx - 40, cx + 40):
        d.line([(sx, top + 12), (sx, top + 34)], fill=INK, width=3)
        d.polygon([(sx - 15, top + 34), (sx + 15, top + 34), (sx, top + 50)],
                  outline=INK, fill=(232, 228, 218))
    d.rectangle([cx - 16, base - 2, cx + 16, base + 2], fill=INK)


def draw_satellite(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    for i in range(42):  # fixed star field, no randomness
        sx = x + (i * 73 + 11) % w
        sy = y + (i * 37 + 7) % (h - 30)
        r = 1 if i % 5 else 2
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(235, 238, 245))
    # Earth arc, kept inside the box
    d.ellipse([x - 60, y + 58, x + w + 60, y + h + 44], fill=(52, 108, 178))
    d.ellipse([x + 40, y + 66, x + 150, y + h], fill=(96, 150, 92))
    d.ellipse([x + w - 190, y + 72, x + w - 60, y + h],
              fill=(96, 150, 92))
    # satellite
    bx, by = x + 96, y + 26
    d.rectangle([bx, by, bx + 34, by + 18], fill=(212, 164, 62), outline=INK)
    for px in (bx - 52, bx + 34):
        d.rectangle([px, by + 2, px + 52, by + 16], fill=(70, 110, 190),
                    outline=(200, 210, 230))
        for gx in range(1, 4):
            d.line([(px + gx * 13, by + 2), (px + gx * 13, by + 16)],
                   fill=(200, 210, 230), width=1)
    d.line([(bx + 17, by), (bx + 17, by - 12)], fill=(220, 220, 220), width=2)
    d.ellipse([bx + 13, by - 16, bx + 21, by - 8], fill=RED)
    # shield with star
    sx, sy = x + w - 96, y + 18
    d.polygon([(sx, sy), (sx + 44, sy), (sx + 44, sy + 30), (sx + 22, sy + 52),
               (sx, sy + 30)], outline=(240, 240, 240), width=3)
    d.polygon([(sx + 22, sy + 8), (sx + 27, sy + 20), (sx + 39, sy + 20),
               (sx + 29, sy + 28), (sx + 33, sy + 40), (sx + 22, sy + 33),
               (sx + 11, sy + 40), (sx + 15, sy + 28), (sx + 5, sy + 20),
               (sx + 17, sy + 20)], fill=RED)


def draw_strait(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 236))
    # cliffs
    d.polygon([(x, y), (x + 92, y), (x + 62, y + h), (x, y + h)], fill=SAND)
    d.polygon([(x + w, y), (x + w - 92, y), (x + w - 62, y + h), (x + w, y + h)],
              fill=(188, 158, 112))
    d.line([(x + 30, y + 30), (x + 70, y + 60)], fill=(160, 130, 88), width=2)
    d.line([(x + w - 30, y + 34), (x + w - 70, y + 62)], fill=(150, 120, 80),
           width=2)
    # water
    d.rectangle([x + 78, y + 52, x + w - 78, y + h], fill=TEAL)
    for i in range(5):
        wx = x + 96 + i * 52
        d.line([(wx, y + h - 16), (wx + 26, y + h - 16)],
               fill=(190, 225, 228), width=2)
    # container tanker
    tx, ty = x + 150, y + 58
    d.rectangle([tx, ty + 12, tx + 150, ty + 30], fill=(150, 40, 34))
    d.polygon([(tx, ty + 12), (tx + 150, ty + 12), (tx + 138, ty + 30),
               (tx + 12, ty + 30)], fill=(120, 30, 26))
    for i, col in enumerate(((52, 110, 190), (216, 130, 44), (96, 150, 92),
                             (232, 228, 218))):
        d.rectangle([tx + 14 + i * 34, ty - 6, tx + 44 + i * 34, ty + 12],
                    fill=col, outline=INK)
    # warship silhouette, foreground right
    wx, wy = x + w - 168, y + h - 34
    d.polygon([(wx, wy), (wx + 128, wy), (wx + 112, wy + 14), (wx + 14, wy + 14)],
              fill=(52, 58, 64))
    d.rectangle([wx + 66, wy - 12, wx + 96, wy], fill=(52, 58, 64))
    d.line([(wx + 80, wy - 12), (wx + 80, wy - 24)], fill=(52, 58, 64), width=3)


def draw_drone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(244, 222, 188))
    d.ellipse([x + w - 66, y + 8, x + w - 34, y + 40], fill=(232, 178, 60))
    # desert ground
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(214, 176, 128))
    # town: flat-roofed houses + church tower
    for i, hx in enumerate((16, 78, 150, 268, 330, 396)):
        hw, hh = (44, 22) if i % 2 == 0 else (36, 16)
        d.rectangle([x + hx, y + h - 34 - hh, x + hx + hw, y + h - 34],
                    fill=(246, 238, 224), outline=(150, 120, 88))
        d.rectangle([x + hx + 8, y + h - 34 - hh + 8, x + hx + 16,
                     y + h - 34 - hh + 14], fill=(90, 70, 50))
    tx = x + 214
    d.rectangle([tx, y + h - 66, tx + 22, y + h - 34], fill=(246, 238, 224),
                outline=(150, 120, 88))
    d.polygon([(tx - 3, y + h - 66), (tx + 25, y + h - 66), (tx + 11, y + h - 80)],
              fill=RED)
    # dashed surveillance ring on the ground
    for a in range(0, 360, 24):
        import math
        a0 = math.radians(a)
        a1 = math.radians(a + 14)
        d.arc([x + 120, y + h - 26, x + 330, y + h - 2], a0 * 180 / 3.14159,
              a1 * 180 / 3.14159, fill=RED, width=2)
    # quadcopter drone
    cx, cy = x + w / 2, y + 30
    d.ellipse([cx - 20, cy - 8, cx + 20, cy + 8], fill=(30, 30, 34))
    d.ellipse([cx - 4, cy + 8, cx + 4, cy + 14], fill=RED)
    for dx, dy in ((-34, -12), (34, -12), (-34, 12), (34, 12)):
        d.line([(cx, cy), (cx + dx, cy + dy)], fill=(30, 30, 34), width=3)
        d.ellipse([cx + dx - 14, cy + dy - 3, cx + dx + 14, cy + dy + 3],
                  outline=(30, 30, 34), width=2)


# ------------------------------------------------------------------- content
HEROES = [
    ("ICJ FINDS MYANMAR GUILTY OF GENOCIDE",
     "World Court rules 9\u20136 that Myanmar\u2019s 2017 campaign against the "
     "Rohingya was genocide \u2014 a first for the ICJ.", draw_courthouse),
    ("NATO VOWS DEFENCE AGAINST SPACE THREAT",
     "Allies brace as reports say Russia could orbit a nuclear-armed "
     "satellite within 60 days, after a year of airspace violations.",
     draw_satellite),
    ("HORMUZ TENSIONS FLARE",
     "Britain logs fresh Iranian attacks in the Strait of Hormuz as Trump "
     "warns Tehran of a \u2018very traumatic\u2019 outcome if talks fail.",
     draw_strait),
    ("US DRONE HELPS MEXICO CAPTURE \u2018EL CHAPO ISIDRO\u2019",
     "Cartel boss Fausto Isidro Meza Flores is seized in Sinaloa with a US "
     "drone\u2019s help; Mexico insists he will stand trial at home.",
     draw_drone),
]

# (region, [(lead, clause), ...]) — 28 briefs, all verified 24 Nov 2026.
BRIEFS = [
    ("AMERICAS", [
        ("OREGON & VIRGINIA", "Two states sue SpaceX over Grok images."),
        ("PENNSYLVANIA", "Ninth measles death; 1,638 cases in 46 counties."),
        ("CARTAGENA", "Gunmen hold 25 people hostage in a supermarket."),
        ("VILLAVICENCIO", "Car bomb destroys buildings; no victims confirmed."),
        ("FIFA", "US, Mexico, Costa Rica, Jamaica host 2031 Women\u2019s Cup."),
        ("WASHINGTON", "Trump gives Giuliani the Medal of Freedom."),
        ("CHICAGO", "Radar failure delays flights at O\u2019Hare airport."),
    ]),
    ("EUROPE", [
        ("GULF OF FINLAND", "Kyiv confirms drone strike on Russian ship."),
        ("ZAPORIZHZHIA", "Russian strike kills two, wounds more than 40."),
        ("PARIS", "Sarkozy corruption case ordered to go to trial."),
        ("FRANKFURT", "Hern\u00e1ndez de Cos tipped to succeed Lagarde."),
        ("PARIS", "Macron wants strategic reserves of rare earths."),
        ("TRIPOLI", "Libya demands Kyiv explain Benghazi ship attack."),
        ("ANKARA", "Libya\u2019s Haftar visits Turkey for the first time."),
    ]),
    ("MIDDLE EAST & AFRICA", [
        ("RIYADH", "Suspected drone strike hits PIF tower; 11 wounded."),
        ("ADEN", "Houthis 60 km from the city and ready to attack."),
        ("LONDON", "UK sanctions Yemen\u2019s Houthis and four officials."),
        ("GAZA", "Israel kills Hamas internal security chief in strike."),
        ("GAZA", "Oxfam calls the territory a \u2018toxic land\u2019."),
        ("TEHRAN", "Iran rules out US talks until seven conditions met."),
        ("DAKAR", "Senegal regains Africa Cup title after CAS appeal."),
    ]),
    ("ASIA-PACIFIC", [
        ("NEW YORK", "US jury convicts Huawei on 10 of 12 counts."),
        ("NEPAL", "5.6 quake strikes Taplejung; no casualties reported."),
        ("JIUQUAN", "China names Pakistan\u2019s Zeeshan Ali for Tiangong."),
        ("SEOUL & TOKYO", "Stocks surge after Nvidia\u2019s Huang returns."),
        ("HANOI", "Gas blast at restaurant kills six, injures ten."),
        ("DHAKA", "Ex-PM Hasina plans return despite death sentence."),
        ("KUALA LUMPUR", "Malaysia to return 6,803 Myanmar nationals."),
    ]),
]

MARKETS = ("MARKETS \u2014 S&P 500 +4.73%  \u00b7  Nasdaq +6.51%  \u00b7  "
           "Nikkei +3.91%  \u00b7  Brent $86.70  \u00b7  Gold $3,620")


# ------------------------------------------------------------------- layout
def draw_hero(img, d, x, y, w, h, headline, caption, illustrator):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    # Render the illustration on its own layer so nothing can spill
    # over the headline or outside the panel.
    illus = Image.new("RGB", (w - 12, 96), PAPER)
    idraw = ImageDraw.Draw(illus)
    illustrator(idraw, 0, 0, w - 12, 96)
    img.paste(illus, (x + 6, y + 6))
    hy = y + 110
    lines, hf = fit_lines(d, headline, font(SERIF_B, 19), w - 16, 2)
    for i, ln in enumerate(lines):
        d.text((x + 8, hy + i * 23), ln, font=hf, fill=INK)
    cy = hy + len(lines) * 23 + 4
    clines, cf = fit_lines(d, caption, font(SANS, 13), w - 16, 2)
    for i, ln in enumerate(clines):
        d.text((x + 8, cy + i * 16), ln, font=cf, fill=(52, 48, 44))
    return h


def draw_brief_line(d, x, y, max_w, lead, clause, size=14):
    """One brief line; shrink the font until it fits. Returns font size used."""
    while size > 11:
        lf, cf = font(SANS_B, size), font(SANS, size)
        total = text_w(d, lead + " \u2014 ", lf) + text_w(d, clause, cf)
        if total <= max_w:
            break
        size -= 0.5
    d.text((x, y), lead + " \u2014 ", font=lf, fill=INK)
    d.text((x + text_w(d, lead + " \u2014 ", lf), y), clause, font=cf,
           fill=(52, 48, 44))
    return size


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    center(d, W / 2, 26, "THE DAILY NEWS SUMMARY \u2014 ONE PAGE, THE WHOLE PLANET",
           font(SANS_B, 15), MUTED)
    center(d, W / 2, 52, "THE WORLD IN ONE DAY", font(SERIF_B, 60), INK)
    center(d, W / 2, 126, "TUESDAY 24 NOVEMBER 2026", font(SANS_B, 24), RED)
    rule(d, M, W - M, 160, 2)
    rule(d, M, W - M, 166, 4)

    # hero grid 2x2
    pw, ph, gap = (CW - 12) // 2, 210, 12
    for i, (headline, caption, illustrator) in enumerate(HEROES):
        hx = M + (i % 2) * (pw + gap)
        hy = 180 + (i // 2) * (ph + gap)
        draw_hero(img, d, hx, hy, pw, ph, headline, caption, illustrator)

    # world in brief
    by = 180 + 2 * ph + gap + 14
    d.text((M, by), "WORLD IN BRIEF", font=font(SANS_B, 20), fill=RED)
    rule(d, M, W - M, by + 28, 2)
    col_w = pw
    col_x = [M, M + pw + gap]
    # columns: A = AMERICAS + EUROPE, B = MIDDLE EAST & AFRICA + ASIA-PACIFIC
    columns = [BRIEFS[0:2], BRIEFS[2:4]]
    ly = by + 38
    max_bottom = 0
    for ci, groups in enumerate(columns):
        y = ly
        for region, items in groups:
            d.text((col_x[ci], y), region, font=font(SANS_B, 14), fill=RED)
            y += 20
            for lead, clause in items:
                draw_brief_line(d, col_x[ci], y, col_w, lead, clause)
                y += 18
            y += 2
        max_bottom = max(max_bottom, y)
    assert max_bottom < 962, f"brief overflow: bottom {max_bottom}"

    # markets footer
    rule(d, M, W - M, 968, 1, fill=MUTED)
    center(d, W / 2, 978, MARKETS, font(SANS, 13), MUTED)

    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img.save(out, format="PNG")
    print(f"wrote {out} {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
