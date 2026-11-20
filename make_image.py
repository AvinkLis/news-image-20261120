#!/usr/bin/env python3
"""Draw the front page of THE DAILY PICTURE for Friday, 20 November 2026.

A newspaper front page, 1024x1024 PNG, drawn entirely in code with Pillow.
No network, no external assets, no photographs. Deterministic: the same
code always produces the same bytes.
"""

import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- constants

W, H = 1024, 1024
MARGIN = 36
CONTENT_W = W - 2 * MARGIN  # 952

PAPER = (247, 243, 234)
PANEL_BG = (239, 234, 222)
SKY = (216, 226, 233)
INK = (26, 26, 26)
GRAY = (96, 91, 82)
ACCENT = (139, 30, 30)
BLUE = (38, 70, 110)
GOLD = (176, 141, 60)
GREEN = (46, 110, 60)
ORANGE = (214, 110, 30)
YELLOW = (232, 178, 60)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, path, text, size, max_width):
    """Largest font size <= `size` for which `text` fits in `max_width`."""
    while size > 8:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 1
    return font(path, 8)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit in max_width."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= max_width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, max_width, fill=INK, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centered(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=fill)


def rule(draw, x0, x1, y, width=1, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ------------------------------------------------------------------- panels

def panel(draw, x, y, w, h):
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=PANEL_BG,
                   outline=(150, 143, 128), width=1)


def draw_court(draw, x, y, w, h):
    """Court building with pediment, columns and scales of justice."""
    panel(draw, x, y, w, h)
    # Ground line and steps.
    base = y + h - 16
    draw.rectangle([x + 18, base - 6, x + w - 18, base], fill=INK)
    draw.rectangle([x + 28, base - 12, x + w - 28, base - 6], fill=INK)
    # Columns.
    col_top = y + 52
    col_bot = base - 12
    n_cols = 5
    span = w - 70
    for i in range(n_cols):
        cx = x + 35 + i * span / (n_cols - 1)
        draw.rectangle([cx - 7, col_top, cx + 7, col_bot], fill=INK)
    # Architrave and pediment.
    draw.rectangle([x + 22, col_top - 10, x + w - 22, col_top], fill=INK)
    draw.polygon([(x + 18, col_top - 10), (x + w / 2, y + 14),
                  (x + w - 18, col_top - 10)], fill=INK)
    # Small round window in the pediment.
    draw.ellipse([x + w / 2 - 7, y + 26, x + w / 2 + 7, y + 40],
                 fill=PAPER)
    # Door.
    draw.rectangle([x + w / 2 - 13, col_bot - 34, x + w / 2 + 13, col_bot],
                   fill=PAPER, outline=INK, width=2)
    # Scales of justice, bottom-right corner.
    sx, sy = x + w - 52, y + h - 46
    draw.line([(sx, sy - 26), (sx, sy + 2)], fill=GOLD, width=3)
    draw.line([(sx - 16, sy - 26), (sx + 16, sy - 26)], fill=GOLD, width=3)
    for dx in (-16, 16):
        draw.line([(sx + dx, sy - 26), (sx + dx - 6, sy - 12)],
                  fill=GOLD, width=2)
        draw.line([(sx + dx, sy - 26), (sx + dx + 6, sy - 12)],
                  fill=GOLD, width=2)
        draw.arc([sx + dx - 8, sy - 14, sx + dx + 8, sy + 2],
                 start=0, end=180, fill=GOLD, width=2)
    draw.ellipse([sx - 3, sy - 30, sx + 3, sy - 24], fill=GOLD)
    draw.line([(sx - 10, sy + 2), (sx + 10, sy + 2)], fill=GOLD, width=3)


def draw_kyiv(draw, x, y, w, h):
    """Kyiv skyline at night: dark towers, missile trails, smoke."""
    panel(draw, x, y, w, h)
    draw.rectangle([x + 1, y + 1, x + w - 2, y + int(h * 0.62)],
                   fill=SKY)
    # Missile trails (accent red-orange streaks with bright heads).
    trails = [
        ((x + 90, y + 18), (x + 210, y + 78)),
        ((x + 470, y + 8), (x + 560, y + 66)),
        ((x + 760, y + 26), (x + 660, y + 82)),
    ]
    for (x0, y0), (x1, y1) in trails:
        draw.line([(x0, y0), (x1, y1)], fill=ORANGE, width=3)
        draw.ellipse([x0 - 5, y0 - 5, x0 + 5, y0 + 5], fill=YELLOW)
        draw.ellipse([x1 - 3, y1 - 3, x1 + 3, y1 + 3], fill=ACCENT)
    # Smoke puffs.
    for cx, cy, r in [(x + 230, y + 66, 9), (x + 585, y + 56, 8),
                      (x + 640, y + 74, 10)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(190, 186, 176))
    # Skyline silhouettes.
    ground = y + h - 1
    towers = [
        (0.00, 0.42, 0.10, 0.30), (0.09, 0.30, 0.07, 0.42),
        (0.15, 0.50, 0.11, 0.22), (0.25, 0.36, 0.08, 0.36),
        (0.32, 0.55, 0.12, 0.17), (0.43, 0.28, 0.09, 0.44),
        (0.51, 0.46, 0.10, 0.26), (0.60, 0.34, 0.08, 0.38),
        (0.67, 0.52, 0.11, 0.20), (0.77, 0.38, 0.09, 0.34),
        (0.85, 0.48, 0.08, 0.24), (0.92, 0.40, 0.08, 0.32),
    ]
    for fx, fy, fw, fh in towers:
        tx = x + fx * w
        tw = fw * w
        ty = y + fy * h
        draw.rectangle([tx, ty, tx + tw, ground], fill=INK)
    # Lit windows.
    for fx, fy in [(0.03, 0.50), (0.11, 0.40), (0.18, 0.58), (0.27, 0.44),
                   (0.36, 0.60), (0.45, 0.36), (0.53, 0.54), (0.62, 0.42),
                   (0.70, 0.58), (0.80, 0.46), (0.87, 0.54), (0.94, 0.48)]:
        wx, wy = x + fx * w, y + fy * h
        draw.rectangle([wx, wy, wx + 5, wy + 7], fill=YELLOW)
    # Red alert beacon on the tallest tower.
    bx, by = x + 0.47 * w, y + 0.28 * h
    draw.ellipse([bx - 5, by - 12, bx + 5, by - 2], fill=ACCENT)
    draw.line([(bx, by - 2), (bx, by + 4)], fill=ACCENT, width=2)


def draw_riyadh(draw, x, y, w, h):
    """Tall tower silhouette with a blast starburst at its crown."""
    panel(draw, x, y, w, h)
    cx = x + w * 0.42
    # Tower: tapered shaft with a spire.
    draw.polygon([(cx - 20, y + h - 6), (cx - 9, y + 26),
                  (cx + 9, y + 26), (cx + 20, y + h - 6)], fill=INK)
    draw.polygon([(cx - 4, y + 26), (cx, y + 8), (cx + 4, y + 26)],
                 fill=INK)
    for wy in range(y + 34, y + h - 12, 10):
        draw.rectangle([cx - 8, wy, cx + 8, wy + 3], fill=YELLOW)
    # Blast starburst at the crown.
    bx, by = cx, y + 14
    for ang in range(0, 360, 30):
        rad = math.radians(ang)
        x1 = bx + 16 * math.cos(rad)
        y1 = by + 16 * math.sin(rad)
        draw.line([(bx, by), (x1, y1)], fill=ORANGE, width=3)
    draw.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=ACCENT)
    # Low buildings at the base.
    draw.rectangle([x + w - 66, y + h - 30, x + w - 8, y + h - 6],
                   fill=GRAY)
    draw.rectangle([x + 8, y + h - 22, x + 52, y + h - 6], fill=GRAY)


def draw_genoa(draw, x, y, w, h):
    """Runway, grounded plane silhouette and two drones above."""
    panel(draw, x, y, w, h)
    # Runway strip.
    draw.polygon([(x + 8, y + h - 14), (x + w - 8, y + h - 26),
                  (x + w - 8, y + h - 12), (x + 8, y + h - 6)],
                 fill=GRAY)
    for i in range(5):
        dx = x + 22 + i * 38
        draw.line([(dx, y + h - 16), (dx + 16, y + h - 19)],
                  fill=PAPER, width=2)
    # Plane silhouette on the runway.
    px, py = x + w * 0.34, y + h - 30
    draw.ellipse([px - 34, py - 6, px + 34, py + 6], fill=INK)
    draw.polygon([(px + 6, py - 4), (px + 26, py - 22), (px + 32, py - 22),
                  (px + 18, py - 2)], fill=INK)
    draw.polygon([(px - 2, py + 2), (px - 18, py + 16), (px - 12, py + 16),
                  (px + 6, py + 4)], fill=INK)
    draw.polygon([(px + 26, py - 4), (px + 40, py - 12), (px + 40, py - 4)],
                 fill=INK)
    # Two drones with rotor lines.
    for dx, dy in [(x + w * 0.72, y + 16), (x + w * 0.88, y + 30)]:
        draw.ellipse([dx - 7, dy - 5, dx + 7, dy + 5], fill=INK)
        draw.line([(dx - 14, dy - 8), (dx + 14, dy - 8)], fill=INK, width=2)
        draw.line([(dx - 14, dy + 8), (dx + 14, dy + 8)], fill=INK, width=2)
        draw.line([(dx, dy + 5), (dx, dy + 14)], fill=INK, width=2)
        draw.ellipse([dx - 3, dy + 14, dx + 3, dy + 20], fill=ACCENT)


def draw_hormuz(draw, x, y, w, h):
    """Tanker on the sea, fire on deck, spiked mine in the water."""
    panel(draw, x, y, w, h)
    sea_y = y + int(h * 0.58)
    draw.rectangle([x + 1, sea_y, x + w - 2, y + h - 2], fill=(196, 214, 226))
    for wx in range(x + 8, x + w - 8, 26):
        draw.arc([wx, sea_y + 12, wx + 22, sea_y + 26], start=180,
                 end=360, fill=BLUE, width=2)
    # Tanker hull and superstructure.
    hx, hy = x + 14, sea_y - 14
    draw.polygon([(hx, hy), (hx + w * 0.62, hy),
                  (hx + w * 0.70, hy + 16), (hx, hy + 16)], fill=INK)
    draw.rectangle([hx + 8, hy - 20, hx + 44, hy], fill=INK)
    draw.rectangle([hx + 48, hy - 14, hx + 56, hy], fill=INK)
    for wx in range(hx + 60, hx + int(w * 0.60), 18):
        draw.rectangle([wx, hy - 8, wx + 8, hy - 2], fill=GOLD)
    # Fire on deck.
    fx, fy = hx + int(w * 0.34), hy - 4
    draw.polygon([(fx - 12, fy), (fx - 4, fy - 22), (fx + 2, fy - 8),
                  (fx + 8, fy - 26), (fx + 14, fy)], fill=ORANGE)
    draw.polygon([(fx - 5, fy), (fx, fy - 12), (fx + 6, fy)], fill=YELLOW)
    # Spiked mine in the water.
    mx, my = x + w * 0.84, sea_y + 16
    for ang in range(0, 360, 45):
        rad = math.radians(ang)
        draw.line([(mx, my),
                   (mx + 13 * math.cos(rad), my + 13 * math.sin(rad))],
                  fill=INK, width=2)
    draw.ellipse([mx - 9, my - 9, mx + 9, my + 9], fill=INK)


def draw_dana(draw, x, y, w, h):
    """Storm cloud, driving rain, houses and an evacuation arrow."""
    panel(draw, x, y, w, h)
    # Cloud: overlapping ellipses.
    for cx, cy, rx, ry in [(x + 52, y + 22, 30, 16), (x + 92, y + 14, 36, 20),
                           (x + 132, y + 24, 30, 15)]:
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=GRAY)
    draw.rectangle([x + 30, y + 22, x + 156, y + 34], fill=GRAY)
    # Rain, slanting.
    for i in range(8):
        rx = x + 34 + i * 18
        draw.line([(rx, y + 38), (rx - 6, y + 52)], fill=BLUE, width=2)
    # Houses at the bottom left.
    for hx in (x + 14, x + 52):
        draw.rectangle([hx, y + h - 22, hx + 28, y + h - 6], fill=INK)
        draw.polygon([(hx - 3, y + h - 22), (hx + 14, y + h - 34),
                      (hx + 31, y + h - 22)], fill=ACCENT)
    # Evacuation arrow to the right.
    ax, ay = x + w - 78, y + h - 22
    draw.line([(ax, ay), (ax + 52, ay)], fill=GREEN, width=4)
    draw.polygon([(ax + 52, ay), (ax + 40, ay - 8), (ax + 40, ay + 8)],
                 fill=GREEN)


def draw_lebanon(draw, x, y, w, h):
    """Hills, a small facility and a blast above it."""
    panel(draw, x, y, w, h)
    # Hills.
    draw.polygon([(x + 1, y + h - 2), (x + w * 0.30, y + 30),
                  (x + w * 0.62, y + h - 2)], fill=(120, 116, 106))
    draw.polygon([(x + w * 0.45, y + h - 2), (x + w * 0.78, y + 38),
                  (x + w - 2, y + h - 2)], fill=GRAY)
    # Facility building.
    fx, fy = x + w * 0.42, y + h - 34
    draw.rectangle([fx, fy, fx + 52, y + h - 6], fill=INK)
    draw.rectangle([fx + 8, fy - 10, fx + 20, fy], fill=INK)
    draw.rectangle([fx + 30, fy + 8, fx + 44, fy + 20], fill=YELLOW)
    # Blast starburst above the facility.
    bx, by = fx + 26, fy - 22
    for ang in range(0, 360, 30):
        rad = math.radians(ang)
        draw.line([(bx, by),
                   (bx + 15 * math.cos(rad), by + 15 * math.sin(rad))],
                  fill=ORANGE, width=3)
    draw.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=ACCENT)


def draw_market(draw, x, y, w, h):
    """Two lines on a chart: Anthropic rising, the S&P 500 falling."""
    panel(draw, x, y, w, h)
    ox, oy = x + 16, y + h - 14  # origin
    draw.line([(ox, y + 10), (ox, oy)], fill=INK, width=2)
    draw.line([(ox, oy), (x + w - 10, oy)], fill=INK, width=2)
    # Grid lines.
    for gy in (y + 22, y + 34, y + 46):
        draw.line([(ox, gy), (x + w - 10, gy)], fill=(200, 194, 182),
                  width=1)
    # Rising green line (Anthropic IPO, +17%).
    rise = [(ox + 6, oy - 6), (ox + 30, oy - 10), (ox + 54, oy - 14),
            (ox + 78, oy - 20), (ox + 102, oy - 28), (ox + 126, oy - 36)]
    draw.line(rise, fill=GREEN, width=3)
    for px, py in rise:
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=GREEN)
    # Falling red line (S&P 500, -2.0%, fifth straight drop).
    fall = [(ox + 6, oy - 4), (ox + 30, oy - 7), (ox + 54, oy - 10),
            (ox + 78, oy - 13), (ox + 102, oy - 16), (ox + 126, oy - 20)]
    draw.line(fall, fill=ACCENT, width=3)
    for px, py in fall:
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=ACCENT)
    # Tiny labels.
    lbl = font(SANS_B, 11)
    draw.text((ox + 130, y + 4), "+17%", font=lbl, fill=GREEN)
    draw.text((ox + 130, y + 20), "-2.0%", font=lbl, fill=ACCENT)


def draw_cop31(draw, x, y, w, h):
    """Globe beside a factory smokestack with drifting smoke."""
    panel(draw, x, y, w, h)
    # Globe.
    gx, gy, gr = x + 48, y + h // 2 + 2, 24
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(196, 214, 226),
                 outline=BLUE, width=2)
    draw.ellipse([gx - 10, gy - gr, gx + 10, gy + gr], outline=BLUE, width=1)
    draw.line([(gx - gr, gy), (gx + gr, gy)], fill=BLUE, width=1)
    draw.arc([gx - gr + 4, gy - 12, gx + gr - 4, gy + 12], start=180,
             end=360, fill=BLUE, width=1)
    # Smokestack and factory.
    fx = x + w - 96
    draw.polygon([(fx, y + h - 6), (fx + 6, y + 16), (fx + 22, y + 16),
                  (fx + 28, y + h - 6)], fill=INK)
    draw.rectangle([fx + 32, y + h - 26, fx + 78, y + h - 6], fill=INK)
    draw.rectangle([fx + 40, y + h - 18, fx + 52, y + h - 8], fill=YELLOW)
    # Smoke puffs drifting right.
    for cx, cy, r in [(fx + 14, y + 10, 6), (fx + 30, y + 6, 8),
                      (fx + 50, y + 10, 6)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GRAY)


# -------------------------------------------------------------------- page

def build():
    """Draw the front page and write entry.png next to this file."""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ------------------------------------------------------
    rule(d, MARGIN, W - MARGIN, 24, width=2)
    title_f = fit_font(d, SERIF_B, "THE DAILY PICTURE", 64, CONTENT_W)
    centered(d, W // 2, 34, "THE DAILY PICTURE", title_f)
    date_f = font(SANS_B, 20)
    centered(d, W // 2, 104, "FRIDAY, 20 NOVEMBER 2026", date_f, fill=ACCENT)
    small_f = font(SANS, 13)
    d.text((MARGIN, 106), "EST. 2026", font=small_f, fill=GRAY)
    d.text((W - MARGIN - d.textlength("NO. 324", font=small_f), 106),
           "NO. 324", font=small_f, fill=GRAY)
    rule(d, MARGIN, W - MARGIN, 132, width=4)
    rule(d, MARGIN, W - MARGIN, 138, width=1)

    # ---- Lead story: ICJ genocide ruling -------------------------------
    lead_x, lead_w = MARGIN, 628
    y = 152
    kick_f = font(SANS_B, 15)
    d.text((lead_x, y), "THE HAGUE  ·  WORLD COURT", font=kick_f, fill=ACCENT)
    y = 176
    head_f = fit_font(d, SERIF_B, "MYANMAR COMMITTED GENOCIDE", 36, lead_w)
    line_h = int(head_f.size * 1.24)
    for line in ["MYANMAR COMMITTED GENOCIDE",
                 "AGAINST THE ROHINGYA,",
                 "WORLD COURT RULES"]:
        d.text((lead_x, y), line, font=head_f, fill=INK)
        y += line_h
    y += 6
    stand_f = font(SERIF, 17)
    y = text_block(d, lead_x, y,
                   "The court's first genocide finding against a state, "
                   "over the 2017 military campaign in Rakhine. Rohingya "
                   "refugees in Bangladesh cheered the verdict.",
                   stand_f, lead_w, leading=21)
    # Court illustration, right of the lead headline.
    court_x, court_w = 680, W - MARGIN - 680  # 308
    draw_court(d, court_x, 152, court_w, 150)
    cap_f = font(SERIF, 13)
    text_block(d, court_x, 308,
               "The International Court of Justice in The Hague.",
               cap_f, court_w, fill=GRAY, leading=16)

    rule(d, MARGIN, W - MARGIN, 360, width=2)

    # ---- Second lead: Kyiv ---------------------------------------------
    y = 374
    d.text((MARGIN, y), "KYIV  ·  UKRAINE", font=kick_f, fill=ACCENT)
    y = 398
    kyiv_head_f = font(SERIF_B, 28)
    d.text((MARGIN, y), "RUSSIAN MISSILES ROCK KYIV OVERNIGHT",
           font=kyiv_head_f, fill=INK)
    y = 436
    sub_f = font(SERIF, 17)
    y = text_block(d, MARGIN, y,
                   "Retaliation after Ukraine struck the Crimean Bridge a "
                   "third time in four days. Air alerts across the capital; "
                   "the Austrian and Dutch embassies were damaged.",
                   sub_f, CONTENT_W, leading=21)
    y += 4
    draw_kyiv(d, MARGIN, y, CONTENT_W, 116)
    y += 116 + 6
    text_block(d, MARGIN, y,
               "Missile trails over the Kyiv skyline as air alerts sound.",
               cap_f, CONTENT_W, fill=GRAY, leading=16)
    y += 22
    rule(d, MARGIN, W - MARGIN, y, width=2)
    y += 10

    # ---- Around the world ----------------------------------------------
    sec_f = font(SANS_B, 14)
    sec_label = "—  AROUND THE WORLD  —"
    centered(d, W // 2, y, sec_label, sec_f)
    y += 26

    def item(x, iy, w, draw_fn, headline, caption, icon_h=64):
        draw_fn(d, x, iy, w, icon_h)
        hy = iy + icon_h + 6
        hf = font(SANS_B, 15)
        hy = text_block(d, x, hy, headline, hf, w, leading=18)
        cf = font(SERIF, 12)
        text_block(d, x, hy + 2, caption, cf, w, fill=GRAY, leading=15)

    gap = 16
    col_w4 = (CONTENT_W - 3 * gap) // 4  # 226
    row_a_y = y
    x4 = [MARGIN + i * (col_w4 + gap) for i in range(4)]
    item(x4[0], row_a_y, col_w4, draw_riyadh,
         "Houthi missile hits Riyadh's tallest tower",
         "Strikes hit four Saudi targets, the Houthis say.")
    item(x4[1], row_a_y, col_w4, draw_genoa,
         "Drones shut Genoa airport",
         "Flights suspended after unidentified drones over the runway.")
    item(x4[2], row_a_y, col_w4, draw_hormuz,
         "Tanker burns after hitting mine near Hormuz",
         "Fire east of the Strait of Hormuz after a mine strike.")
    item(x4[3], row_a_y, col_w4, draw_dana,
         "India evacuates 80,000 as Storm Dana nears",
         "More than 80,000 moved to safety ahead of landfall.")

    row_b_y = row_a_y + 158
    col_w3 = (CONTENT_W - 2 * gap) // 3  # 306
    x3 = [MARGIN + i * (col_w3 + gap) for i in range(3)]
    item(x3[0], row_b_y, col_w3, draw_lebanon,
         "Israeli strike hits Hezbollah site in Lebanon",
         "Airstrike hits a missile facility in eastern Lebanon.",
         icon_h=56)
    item(x3[1], row_b_y, col_w3, draw_market,
         "Anthropic IPO soars 17% as Wall Street slides",
         "Record $81.3bn listing briefly tops $2tn; S&P 500 falls 2.0%, "
         "a fifth straight drop.",
         icon_h=56)
    item(x3[2], row_b_y, col_w3, draw_cop31,
         "COP31 draft drops fossil fuels, outcry follows",
         "Draft deal omits fossil fuels entirely, drawing an outcry.",
         icon_h=56)

    # ---- Footer ----------------------------------------------------------
    foot_f = font(SANS, 11)
    centered(d, W // 2, H - 22,
             "THE DAILY PICTURE — Friday, 20 November 2026 — "
             "The day's world news, drawn in one page.",
             foot_f, fill=GRAY)

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG")
    return out


if __name__ == "__main__":
    print(build())
