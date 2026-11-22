#!/usr/bin/env python3
"""Draw the Saturday 21 November 2026 front page as a 1024x1024 PNG.

A single-column newspaper front page: masthead, dateline, one wide
lead panel on the market sell-off, then the remaining five stories in
a two-column grid (two rows of two, plus a full-width closing strip).
Every illustration is a hand-drawn PIL sketch -- a falling chart, a
blast, a pair of handcuffs, a globe, a shield and a magnifier -- so
the page contains no photographic or AI-generated imagery and all
type stays sharp.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(BASE, "entry.png")

W, H = 1024, 1024
EDGE = 42
INNER_W = W - 2 * EDGE
GAP = 20

SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

PAPER = (250, 247, 238)
CARD = (255, 255, 255)
INK = (16, 16, 16)
BODY = (70, 70, 70)
LINE = (180, 174, 158)
NAVY = (28, 58, 112)
LEAD_TINT = (232, 238, 248)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    out, cur = [], ""
    for word in text.split():
        cand = word if not cur else cur + " " + word
        if draw.textlength(cand, font=fnt) <= max_w or not cur:
            cur = cand
        else:
            out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def fit(draw, text, path, start, max_w, max_lines):
    """Shrink the point size until the text fits in max_lines lines."""
    size = start
    while size > 11:
        fnt = font(path, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 1
    fnt = font(path, size)
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip() + " \u2026"
    return fnt, lines


def put_lines(draw, lines, x, y, fnt, fill, step):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += step
    return y


def hline(draw, x0, x1, y, wdt=1, colour=INK):
    draw.line([(x0, y), (x1, y)], fill=colour, width=wdt)


# ---------------------------------------------------------------- icons

def icon_falling_chart(d, x, y, s, colour):
    d.line([(x, y + s), (x + s, y + s)], fill=colour, width=3)
    d.line([(x, y), (x, y + s)], fill=colour, width=3)
    pts = [(x + s * 0.06, y + s * 0.22), (x + s * 0.34, y + s * 0.44),
           (x + s * 0.58, y + s * 0.36), (x + s * 0.94, y + s * 0.80)]
    d.line(pts, fill=colour, width=5, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex, ey + 13), (ex - 13, ey - 3), (ex + 3, ey - 13)],
              fill=colour)


def icon_blast(d, x, y, s, colour):
    cx, cy = x + s / 2, y + s / 2
    for i in range(10):
        ang = math.radians(i * 36)
        r0, r1 = s * 0.14, s * 0.5
        d.line([(cx + r0 * math.cos(ang), cy + r0 * math.sin(ang)),
                (cx + r1 * math.cos(ang), cy + r1 * math.sin(ang))],
               fill=colour, width=4)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=colour)


def icon_cuffs(d, x, y, s, colour):
    r = s * 0.28
    d.ellipse([x + s * 0.02, y + s * 0.10, x + s * 0.02 + 2 * r,
               y + s * 0.10 + 2 * r], outline=colour, width=5)
    d.ellipse([x + s * 0.98 - 2 * r, y + s * 0.30,
               x + s * 0.98, y + s * 0.30 + 2 * r], outline=colour, width=5)
    d.line([(x + s * 0.30, y + s * 0.38), (x + s * 0.70, y + s * 0.58)],
           fill=colour, width=5)


def icon_globe(d, x, y, s, colour):
    d.ellipse([x, y, x + s, y + s], outline=colour, width=5)
    d.line([(x, y + s / 2), (x + s, y + s / 2)], fill=colour, width=3)
    d.arc([x + s * 0.28, y, x + s * 0.72, y + s], 0, 360,
          fill=colour, width=3)


def icon_shield(d, x, y, s, colour):
    pts = [(x + s * 0.5, y), (x + s * 0.95, y + s * 0.18),
           (x + s * 0.95, y + s * 0.55), (x + s * 0.5, y + s),
           (x + s * 0.05, y + s * 0.55), (x + s * 0.05, y + s * 0.18)]
    d.polygon(pts, outline=colour, width=5)
    d.line([(x + s * 0.32, y + s * 0.52), (x + s * 0.46, y + s * 0.66),
            (x + s * 0.70, y + s * 0.34)], fill=colour, width=5,
           joint="curve")


def icon_magnifier(d, x, y, s, colour):
    r = s * 0.30
    d.ellipse([x + s * 0.05, y + s * 0.05,
               x + s * 0.05 + 2 * r, y + s * 0.05 + 2 * r],
              outline=colour, width=5)
    d.line([(x + s * 0.58, y + s * 0.58), (x + s * 0.92, y + s * 0.92)],
           fill=colour, width=6)


ICONS = {
    "chart": icon_falling_chart,
    "blast": icon_blast,
    "cuffs": icon_cuffs,
    "globe": icon_globe,
    "shield": icon_shield,
    "lens": icon_magnifier,
}

LEAD = {
    "tag": "MARKETS  \u2022  GLOBAL SELL-OFF",
    "head": "AI SELL-OFF SINKS GLOBAL MARKETS",
    "text": ("The S&P 500 falls 3.7% and Japan's Nikkei falls 5.06% as "
             "fears grow that AI spending will not pay off."),
    "strip": "S&P 500  \u22123.7%      NIKKEI  \u22125.06%",
    "icon": "chart",
}

GRID = [
    {"tag": "WAR  \u2022  UKRAINE",
     "head": "MISSILE HITS ZELENSKYY'S HOMETOWN",
     "text": ("A Russian ballistic missile strikes Kryvyi Rih, killing 2 "
              "people and wounding dozens; Russia launched 3 missiles and "
              "148 drones overnight."),
     "icon": "blast"},
    {"tag": "MEXICO  \u2022  SINALOA",
     "head": "MEXICO CAPTURES CARTEL BOSS 'EL CHAPO ISIDRO'",
     "text": ("Mexican forces capture Fausto Isidro Meza Flores, an FBI "
              "most-wanted cartel boss, in Sinaloa."),
     "icon": "cuffs"},
    {"tag": "CLIMATE  \u2022  ANTALYA",
     "head": "COP31 TALKS RUN PAST DEADLINE",
     "text": ("Climate talks in Antalya overrun their Friday deadline, "
              "still divided over fossil fuels."),
     "icon": "globe"},
    {"tag": "WAR  \u2022  POLAND",
     "head": "RUSSIAN MISSILES LAND IN POLAND",
     "text": ("Missiles fall in south-east Poland during the attack on "
              "Ukraine, in what Warsaw calls a provocation; air defences "
              "were activated."),
     "icon": "shield"},
]

CLOSER = {
    "tag": "INVESTIGATION  \u2022  UNITED STATES",
    "head": "FBI PROBES HACK OF CRIME DATABASE",
    "text": ("The FBI investigates a suspected breach of a database used "
             "by US law enforcement agencies."),
    "icon": "lens",
}


def card_story(d, x, y, w, h, story, head_start, body_size, icon_size):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=1)
    pad = 16
    tx = x + pad
    tag_f = font(SANS_BOLD, 14)
    d.text((tx, y + 12), story["tag"], font=tag_f, fill=NAVY)
    tag_w = d.textlength(story["tag"], font=tag_f)
    d.line([(tx, y + 32), (tx + tag_w, y + 32)], fill=NAVY, width=2)
    ICONS[story["icon"]](d, x + w - pad - icon_size, y + 12, icon_size, INK)
    hf, hlines = fit(d, story["head"], SERIF_BOLD, head_start,
                     w - 2 * pad - icon_size - 10, 2)
    yy = put_lines(d, hlines, tx, y + 34, hf, INK, head_start + 5)
    bf, blines = fit(d, story["text"], SERIF_REG, body_size,
                     w - 2 * pad, 3)
    put_lines(d, blines, tx, yy + 4, bf, BODY, body_size + 6)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    title_f = font(SERIF_BOLD, 64)
    d.text((W // 2, 22), "The Morning Dispatch", font=title_f,
           fill=INK, anchor="ma")
    hline(d, EDGE, W - EDGE, 98, 3)
    hline(d, EDGE, W - EDGE, 104, 1)
    date_f = font(SANS_BOLD, 28)
    d.text((W // 2, 114), "SATURDAY  21 NOVEMBER 2026",
           font=date_f, fill=NAVY, anchor="ma")
    hline(d, EDGE, W - EDGE, 150, 3)
    hline(d, EDGE, W - EDGE, 154, 1)

    # lead panel
    lx, ly, lw, lh = EDGE, 170, INNER_W, 228
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=LEAD_TINT,
                outline=INK, width=2)
    tag_f = font(SANS_BOLD, 16)
    d.text((lx + 20, ly + 14), LEAD["tag"], font=tag_f, fill=NAVY)
    ICONS[LEAD["icon"]](d, lx + lw - 20 - 62, ly + 12, 62, NAVY)
    hf, hlines = fit(d, LEAD["head"], SERIF_BOLD, 40, lw - 40 - 82, 2)
    yy = put_lines(d, hlines, lx + 20, ly + 40, hf, INK, 46)
    bf, blines = fit(d, LEAD["text"], SERIF_REG, 18, lw - 40, 2)
    yy = put_lines(d, blines, lx + 20, yy + 6, bf, BODY, 24)
    strip_f = font(SANS_BOLD, 17)
    sy = ly + lh - 36
    hline(d, lx + 20, lx + lw - 20, sy - 8, 1, LINE)
    d.text((lx + 20, sy), LEAD["strip"], font=strip_f, fill=INK)

    # two-by-two grid
    col_w = (INNER_W - GAP) // 2
    row_h = 190
    top = 414
    for i, story in enumerate(GRID):
        r, c = divmod(i, 2)
        card_story(d, EDGE + c * (col_w + GAP), top + r * (row_h + 14),
                   col_w, row_h, story, head_start=24, body_size=17,
                   icon_size=50)

    # closing strip
    cx, cy, cw, ch = EDGE, 826, INNER_W, 118
    d.rectangle([cx, cy, cx + cw, cy + ch], fill=CARD, outline=LINE, width=1)
    d.rectangle([cx, cy, cx + 6, cy + ch], fill=NAVY)
    tag_f = font(SANS_BOLD, 14)
    d.text((cx + 22, cy + 12), CLOSER["tag"], font=tag_f, fill=NAVY)
    ICONS[CLOSER["icon"]](d, cx + cw - 22 - 54, cy + 30, 54, INK)
    hf, hlines = fit(d, CLOSER["head"], SERIF_BOLD, 27, cw - 44 - 74, 1)
    put_lines(d, hlines, cx + 22, cy + 36, hf, INK, 32)
    bf, blines = fit(d, CLOSER["text"], SERIF_REG, 16, cw - 44, 1)
    put_lines(d, blines, cx + 22, cy + 74, bf, BODY, 21)

    # footer repeats the date
    hline(d, EDGE, W - EDGE, 962, 3)
    foot_f = font(SANS_BOLD, 21)
    d.text((W // 2, 974), "21 NOVEMBER 2026  \u2022  THE MORNING DISPATCH",
           font=foot_f, fill=INK, anchor="ma")

    img.save(TARGET, format="PNG", optimize=True)
    print("wrote", TARGET, os.path.getsize(TARGET), "bytes")


if __name__ == "__main__":
    main()
