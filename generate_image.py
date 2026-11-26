#!/usr/bin/env python3
"""Draw THE DAILY GLOBE front page for 26 November 2026 as a 1024x1024 PNG.

Everything on the page is drawn with Pillow primitives: masthead, lead story
with a hand-drawn map of the Strait of Hormuz, a 2x2 grid of short stories,
one wide Gaza story, an ALSO TODAY band and a sources footer. Run it with
`python3 generate_image.py` and it writes entry.png next to this file.
"""

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
PAPER = (248, 243, 230)
INK = (20, 20, 20)
RED = (163, 18, 18)
SEA = (178, 205, 219)
SAND = (224, 201, 143)
FLAME = (232, 116, 18)
EMBER = (240, 178, 44)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_IT = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, width):
    """Split text into lines that fit `width` pixels in font `fnt`."""
    lines, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if fnt.getlength(trial) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def para(canvas, x, y, width, text, fnt, fill=INK, leading=24):
    """Draw wrapped text; return the y just below the last line."""
    for line in wrap(text, fnt, width):
        canvas.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centred(canvas, cx, y, text, fnt, fill=INK):
    canvas.text((cx - fnt.getlength(text) / 2, y), text, font=fnt, fill=fill)


def tanker(canvas, x, y, scale=1.0):
    """A small tanker hull with flames above it, drawn at (x, y)."""
    hull_w, hull_h = int(74 * scale), int(16 * scale)
    canvas.rectangle([x, y, x + hull_w, y + hull_h], fill=(38, 38, 38))
    canvas.rectangle([x + int(48 * scale), y - int(10 * scale),
                      x + int(66 * scale), y], fill=(90, 90, 90))
    for dx, h in ((-6, 26), (14, 34), (34, 28), (52, 20)):
        fx = x + int(dx * scale)
        canvas.polygon([(fx, y), (fx + int(13 * scale), y),
                        (fx + int(6 * scale), y - int(h * scale))],
                       fill=FLAME)
        canvas.polygon([(fx + 3, y), (fx + int(10 * scale), y),
                        (fx + int(6 * scale), y - int(h * 0.55 * scale))],
                       fill=EMBER)


def mine(canvas, cx, cy, r=7):
    """A spiked naval mine centred on (cx, cy)."""
    import math
    for k in range(8):
        ang = math.pi * k / 4
        canvas.line([cx + int(0.8 * r * math.cos(ang)),
                     cy + int(0.8 * r * math.sin(ang)),
                     cx + int(1.7 * r * math.cos(ang)),
                     cy + int(1.7 * r * math.sin(ang))],
                    fill=INK, width=2)
    canvas.ellipse([cx - r, cy - r, cx + r, cy + r], fill=INK)


def draw_map(canvas, x0, y0, x1, y1):
    """The strait illustration: Iran above, Oman below, two burning tankers.

    The channel runs diagonally from the upper left (Persian Gulf side) to
    the lower right (Gulf of Oman side). Labels sit in clear water or on
    land, well away from the tankers, mines and caption.
    """
    canvas.rectangle([x0, y0, x1, y1], fill=SEA, outline=INK, width=2)
    # Iran: the land mass along the top edge, its coast sloping down right.
    canvas.polygon([(x0, y0), (x1, y0), (x1, y0 + 110), (x0 + 236, y0 + 98),
                    (x0 + 116, y0 + 84), (x0, y0 + 72)], fill=SAND)
    # Oman: the land mass along the bottom edge, its coast sloping down right.
    canvas.polygon([(x0, y1), (x1, y1), (x1, y1 - 54), (x0 + 216, y1 - 66),
                    (x0 + 96, y1 - 78), (x0, y1 - 84)], fill=SAND)
    label = font(SANS_BOLD, 22)
    canvas.text((x0 + 24, y0 + 14), "IRAN", font=label, fill=INK)
    canvas.text((x0 + 276, y0 + 170), "OMAN", font=font(SANS_BOLD, 18),
                fill=INK)
    small = font(SERIF_IT, 13)
    canvas.text((x0 + 10, y0 + 104), "Persian Gulf", font=small,
                fill=(40, 70, 90))
    canvas.text((x0 + 248, y0 + 150), "Gulf of Oman", font=small,
                fill=(40, 70, 90))
    tanker(canvas, x0 + 116, y0 + 108)
    tanker(canvas, x0 + 196, y0 + 128, scale=0.85)
    mine(canvas, x0 + 88, y0 + 136, r=6)
    mine(canvas, x0 + 294, y0 + 118, r=7)
    caption = font(SERIF_IT, 14)
    centred(canvas, (x0 + x1) / 2, y1 - 26,
            "Strait of Hormuz: two tankers ablaze.",
            caption, fill=INK)


def draw_grid_story(canvas, x, y, w, kicker, headline, body):
    kick = font(SANS_BOLD, 15)
    head = font(SANS_BOLD, 22)
    text = font(SANS, 14)
    canvas.text((x, y), kicker, font=kick, fill=RED)
    y = para(canvas, x, y + 20, w, headline, head, leading=26)
    para(canvas, x, y + 2, w, body, text, leading=18)


def main():
    sheet = Image.new("RGB", (PAGE, PAGE), PAPER)
    pen = ImageDraw.Draw(sheet)
    pen.rectangle([14, 14, PAGE - 14, PAGE - 14], outline=INK, width=2)

    # ---- Masthead ----
    centred(pen, PAGE / 2, 26, "THE DAILY GLOBE",
            font(SERIF_BOLD, 80))
    pen.line([40, 124, PAGE - 40, 124], fill=INK, width=1)
    meta = font(SANS, 15)
    pen.text((40, 132), "Vol. CXII — No. 330", font=meta, fill=INK)
    centred(pen, PAGE / 2, 132, "Thursday, 26 November 2026",
            font(SANS_BOLD, 16))
    right = "WORLD EDITION"
    pen.text((PAGE - 40 - meta.getlength(right), 132), right,
             font=meta, fill=INK)
    pen.line([40, 156, PAGE - 40, 156], fill=INK, width=4)
    pen.line([40, 162, PAGE - 40, 162], fill=INK, width=1)

    # ---- Lead headline + deck ----
    centred(pen, PAGE / 2, 172, "TWO TANKERS ABLAZE",
            font(SERIF_BOLD, 42))
    centred(pen, PAGE / 2, 220, "AS MINES CLOSE HORMUZ",
            font(SERIF_BOLD, 42))
    centred(pen, PAGE / 2, 272,
            "Iran says ships hit mines on an unauthorised route; the claims are unverified.",
            font(SERIF_IT, 16))

    # ---- Lead text (left) + strait map (right) ----
    body = font(SANS, 17)
    y = 300
    y = para(pen, 40, y, 556,
             "Two oil tankers caught fire early on Wednesday after striking "
             "naval mines in the Strait of Hormuz, Iran's Revolutionary Guard "
             "navy said.", body, leading=23)
    y = para(pen, 40, y + 8, 556,
             "The Guard said the tankers took an unauthorised route with "
             "tracking switched off. The claims could not be verified; no "
             "casualties were confirmed.", body, leading=23)
    y = para(pen, 40, y + 8, 556,
             "Tehran told Washington, via Qatari mediators, it could reopen "
             "the strait in 48 hours if its conditions are met. Washington "
             "calls them unrealistic.", body, leading=23)
    draw_map(pen, 624, 300, 984, 524)

    pen.line([40, 536, PAGE - 40, 536], fill=INK, width=2)

    # ---- 2 x 2 grid of short stories ----
    draw_grid_story(
        pen, 40, 548, 452, "TRADE",
        "Trump unveils new tariffs on 14 nations",
        "Washington proposes duties of 20% to 40% after the Supreme Court "
        "struck down the old tariffs. Nothing takes effect before a public "
        "hearing on 25 January.")
    draw_grid_story(
        pen, 532, 548, 452, "SPACE",
        "Pakistan's first astronaut reaches Tiangong",
        "Shenzhou-24 docked on 25 November carrying Muhammad Zeeshan Ali, "
        "the first Pakistani in orbit and the first foreign visitor to "
        "China's space station.")
    pen.line([40, 682, PAGE - 40, 682], fill=INK, width=1)
    draw_grid_story(
        pen, 40, 694, 452, "COLOMBIA",
        "All 50-plus hostages freed in Cartagena",
        "Troops stormed a supermarket where gunmen held shoppers after a "
        "failed armoured-truck robbery. One gunman was killed.")
    draw_grid_story(
        pen, 532, 694, 452, "ENERGY",
        "Houthis claim refinery hit; four drones downed",
        "Yemen's Houthis say they struck the Ras Tanura refinery and fires "
        "broke out. The Saudi-led coalition says it shot down four drones; "
        "satellite images show black smoke.")

    pen.line([40, 828, PAGE - 40, 828], fill=INK, width=2)

    # ---- Wide Gaza story ----
    pen.text((40, 840), "GAZA  —  ",
             font=font(SANS_BOLD, 15), fill=RED)
    pen.text((40 + font(SANS_BOLD, 15).getlength("GAZA  —  "), 840),
             "Second Hamas security chief killed in Gaza in a day",
             font=font(SANS_BOLD, 20), fill=INK)
    para(pen, 40, 866, 944,
         "Col. Mohammad Abuelouf died with his wife and two daughters in a "
         "strike on Gaza City, a day after his commander was killed.",
         font(SANS, 15), leading=19)

    # ---- ALSO TODAY band ----
    pen.rectangle([40, 906, PAGE - 40, 980], fill=INK)
    para(pen, 56, 914, 912,
         "ALSO TODAY:  COP31 climate talks collapse in Antalya  •  Dow back "
         "above 50,000, closing at 50,018.70  •  Jennifer Barreto of Puerto "
         "Rico becomes the first mother to win Miss Universe  •  Solomon "
         "Islands signs Australia pact barring foreign bases  •  North Korea "
         "expels Swiss envoy",
         font(SANS, 15), fill=(245, 245, 245), leading=19)

    # ---- Footer ----
    centred(pen, PAGE / 2, 988,
            "Sources: Reuters  •  AP  •  AFP — reporting of 25–26 November 2026",
            font(SANS, 12), fill=(90, 90, 90))

    sheet.save("entry.png")
    print("wrote entry.png (1024x1024)")


if __name__ == "__main__":
    main()
