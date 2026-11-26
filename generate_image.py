#!/usr/bin/env python3
"""Draw the 26 Nov 2026 newspaper front page (1024x1024) with PIL only.

Deterministic: same input always produces the same PNG bytes.
"""
from PIL import Image, ImageDraw, ImageFont
import math
import os

F = "/usr/share/fonts/truetype/liberation/"
SERIF_B = F + "LiberationSerif-Bold.ttf"
SERIF = F + "LiberationSerif-Regular.ttf"
SERIF_I = F + "LiberationSerif-Italic.ttf"
SANS_B = F + "LiberationSans-Bold.ttf"
SANS = F + "LiberationSans-Regular.ttf"

W = H = 1024
PAPER = (250, 247, 238)
INK = (18, 18, 18)
RED = (163, 22, 33)
GRAY = (90, 88, 82)
RULE = (30, 30, 30)
FAINT = (178, 174, 164)
SEA = (196, 214, 224)
LAND = (232, 222, 196)
FLAME = (214, 88, 26)
SMOKE = (120, 118, 112)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def font(path, size):
    return ImageFont.truetype(path, size)

def text_w(s, f):
    return d.textlength(s, font=f)

def center(s, y, f, fill=INK):
    d.text(((W - text_w(s, f)) / 2, y), s, font=f, fill=fill)

def wrap(s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if text_w(t, f) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def para(s, x, y, f, maxw, lh, fill=INK):
    for ln in wrap(s, f, maxw):
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y

M = 36
d.rectangle([14, 14, W - 14, H - 14], outline=RULE, width=3)
d.rectangle([20, 20, W - 20, H - 20], outline=RULE, width=1)

f_small = font(SANS, 15)
d.text((M, 30), "Vol. I · No. 26", font=f_small, fill=GRAY)
r = "WORLD EDITION"
d.text((W - M - text_w(r, f_small), 30), r, font=f_small, fill=GRAY)
c = "ONE PAGE · THE WHOLE WORLD"
d.text(((W - text_w(c, f_small)) / 2, 30), c, font=f_small, fill=GRAY)
d.line([M, 56, W - M, 56], fill=RULE, width=2)

center("THE DAILY GLOBE", 58, font(SERIF_B, 88))
d.line([M, 156, W - M, 156], fill=RULE, width=4)
d.line([M, 164, W - M, 164], fill=RULE, width=1)

f_date = font(SANS_B, 20)
d.text((M, 175), "Thursday, 26 November 2026", font=f_date, fill=INK)
f_motto = font(SERIF_I, 17)
m2 = "The day's world news, summed up on a single page"
d.text((W - M - text_w(m2, f_motto), 176), m2, font=f_motto, fill=GRAY)
d.line([M, 206, W - M, 206], fill=RULE, width=2)

# ---------- LEAD ----------
y = 218
f_kick = font(SANS_B, 17)
d.text((M, y), "STRAIT OF HORMUZ  ·  IRAN WAR", font=f_kick, fill=RED)
y += 28
f_head = font(SERIF_B, 57)
for ln in ["TANKERS ABLAZE IN THE", "STRAIT OF HORMUZ"]:
    assert text_w(ln, f_head) <= W - 2 * M, ln
    d.text((M, y), ln, font=f_head, fill=INK)
    y += 57
y += 4
f_deck = font(SERIF_I, 21)
y = para("Tehran says two oil tankers struck naval mines and caught fire — the latest in a "
         "string of such claims, none of them independently verified.",
         M, y, f_deck, W - 2 * M, 27)
y += 8

# body (left) + strait map visual (right)
row_y = y
f_body = font(SERIF, 18)
para("Iran's Revolutionary Guard said two oil tankers struck naval mines and exploded in the "
     "Strait of Hormuz, the world's busiest oil waterway, and caught fire. Tehran says shipping "
     "will not return to normal until its demands are met; earlier this month it offered to "
     "reopen the strait within 48 hours if Washington accepts its conditions. The claim is "
     "unverified; no casualties have been confirmed.", M, row_y, f_body, 540, 24)

vx0, vy0, vx1, vy1 = 612, row_y, W - M, row_y + 168
d.rectangle([vx0, vy0, vx1, vy1], outline=RULE, width=2)
# sea
d.rectangle([vx0 + 2, vy0 + 2, vx1 - 2, vy1 - 2], fill=SEA)
# land: Iran (top) and Oman (bottom)
d.polygon([(vx0 + 2, vy0 + 2), (vx1 - 2, vy0 + 2), (vx1 - 2, vy0 + 34),
           (vx0 + 150, vy0 + 52), (vx0 + 2, vy0 + 40)], fill=LAND)
d.polygon([(vx0 + 2, vy1 - 2), (vx1 - 2, vy1 - 2), (vx1 - 2, vy1 - 44),
           (vx0 + 190, vy1 - 26), (vx0 + 2, vy1 - 52)], fill=LAND)
d.text((vx0 + 14, vy0 + 8), "IRAN", font=font(SANS_B, 13), fill=GRAY)
d.text((vx0 + 14, vy1 - 22), "OMAN", font=font(SANS_B, 13), fill=GRAY)

def tanker(x, y, scale=1.0):
    # hull + superstructure + flame plume
    d.polygon([(x, y + 14 * scale), (x + 92 * scale, y + 14 * scale),
               (x + 80 * scale, y + 26 * scale), (x + 12 * scale, y + 26 * scale)],
              fill=INK)
    d.rectangle([x + 58 * scale, y, x + 76 * scale, y + 14 * scale], fill=INK)
    d.rectangle([x + 64 * scale, y - 6 * scale, x + 70 * scale, y], fill=INK)
    for dx, dy, s in [(18, -26, 16), (34, -38, 20), (52, -22, 13)]:
        d.polygon([(x + dx * scale, y + dy * scale + s),
                   (x + (dx + s * 0.55) * scale, y + dy * scale),
                   (x + (dx + s) * scale, y + dy * scale + s)], fill=FLAME)
    for dx, dy, r in [(26, -50, 7), (44, -58, 9), (60, -48, 6)]:
        d.ellipse([x + dx * scale - r, y + dy * scale - r,
                   x + dx * scale + r, y + dy * scale + r], fill=SMOKE)

tanker(vx0 + 30, vy0 + 96)
tanker(vx0 + 196, vy0 + 76, scale=0.85)
# mines in the channel
for mx, my in [(vx0 + 150, vy0 + 118), (vx0 + 262, vy0 + 96), (vx0 + 318, vy0 + 128)]:
    d.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=INK)
    for ang in (0, 45, 90, 135):
        a = math.radians(ang)
        d.line([mx + 5 * math.cos(a), my + 5 * math.sin(a),
                mx + 9 * math.cos(a), my + 9 * math.sin(a)], fill=INK, width=2)
d.text((vx0 + 8, vy1 - 40), "STRAIT OF HORMUZ — NOT TO SCALE", font=font(SANS_B, 12), fill=INK)

y = row_y + 178
d.line([M, y, W - M, y], fill=RULE, width=3)
y += 10

# ---------- SUB-STORY GRID ----------
col_w = (W - 2 * M - 24) / 2
f_k2 = font(SANS_B, 15)
f_h2 = font(SERIF_B, 26)
f_b2 = font(SERIF, 16)

stories = [
    ("WASHINGTON · TRADE", "Trump Unveils New Tariffs",
     "The U.S. proposes duties of 20–40% on 14 trading partners, after the Supreme Court "
     "struck down earlier tariffs. Nothing takes effect before a 25 January hearing."),
    ("SPACE · CHINA", "Pakistan's First Astronaut in Orbit",
     "Shenzhou-24 docked with the Tiangong station carrying Muhammad Zeeshan Ali, the first "
     "Pakistani in space, with two Chinese crew members."),
    ("CARTAGENA · COLOMBIA", "All Hostages Freed in Siege",
     "Troops stormed a supermarket in Cartagena and freed the last of more than 50 hostages "
     "seized after a failed armoured-car robbery. One captor was killed."),
    ("YEMEN · ENERGY", "Houthis Strike Saudi Refinery",
     "The Houthis say they hit the Ras Tanura oil refinery, causing fires. The Saudi-led "
     "coalition says air defences destroyed four drones over the site."),
]
gy = y
row_h = 108
for i, (kick, head, body) in enumerate(stories):
    cx0 = M + (i % 2) * (col_w + 24)
    cy0 = gy + (i // 2) * row_h
    d.text((cx0, cy0), kick, font=f_k2, fill=RED)
    d.text((cx0, cy0 + 20), head, font=f_h2, fill=INK)
    para(body, cx0, cy0 + 50, f_b2, col_w, 18)
    if i % 2 == 0:
        d.line([cx0 + col_w + 12, cy0 + 2, cx0 + col_w + 12, cy0 + row_h - 14], fill=FAINT, width=1)
    if i < 2:
        d.line([cx0, cy0 + row_h - 6, cx0 + col_w, cy0 + row_h - 6], fill=FAINT, width=1)
y = gy + 2 * row_h
d.line([M, y, W - M, y], fill=RULE, width=2)
y += 9

# wide story
d.text((M, y), "GAZA · WAR", font=f_k2, fill=RED)
d.text((M + 218, y - 5), "Israel Kills Hamas Security Chief", font=f_h2, fill=INK)
y += 22
y = para("An Israeli strike killed Hamas colonel Mohammad Abuelouf, who ran the militants' interior "
         "security service in northern Gaza, along with his wife and two children in Gaza City, "
         "medics said. It was the second senior Hamas security official killed in 24 hours.",
         M, y, f_b2, W - 2 * M, 19)
y += 8

# ALSO TODAY
d.rectangle([M, y, W - M, y + 26], fill=INK)
d.text((M + 12, y + 5), "ALSO TODAY", font=font(SANS_B, 16), fill=PAPER)
y += 32
f_tick = font(SERIF, 15)
ticker = ("COP31 climate talks collapse with no deal  ·  Dow back above 50,000 as Nasdaq slides  ·  "
          "Miss Universe: Jennifer Barreto of Puerto Rico, first mother to win  ·  "
          "Australia and Solomon Islands sign treaty barring foreign bases  ·  North Korea expels Swiss envoy")
y = para(ticker, M, y, f_tick, W - 2 * M, 20)
y += 4
d.line([M, y, W - M, y], fill=RULE, width=2)
f_foot = font(SERIF_I, 13)
center("Compiled from Reuters, Associated Press and AFP reports of 25–26 November 2026 · Every picture on this page was drawn for this page",
       y + 7, f_foot, fill=GRAY)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, optimize=True)
print("saved", out, os.path.getsize(out), "bytes; content ends y =", y + 24)
