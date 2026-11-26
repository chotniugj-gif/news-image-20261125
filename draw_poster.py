#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news broadsheet.

The output is a fixed 1024x1024 PNG. Everything is drawn from constants in
this file: no clock, no randomness, no network, no downloaded assets.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
PAPER = (247, 241, 227)
INK = (20, 20, 20)
SOFT = (74, 70, 62)
ACCENT = (179, 35, 24)
BLUE = (31, 78, 120)
GOLD = (176, 124, 31)
RULE = (154, 145, 126)
PANEL = (252, 248, 238)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(size, *, serif=False, bold=False):
    if serif and bold:
        name = "DejaVuSerif-Bold.ttf"
    elif serif:
        name = "DejaVuSerif.ttf"
    elif bold:
        name = "DejaVuSans-Bold.ttf"
    else:
        name = "DejaVuSans.ttf"
    return ImageFont.truetype(str(FONT_DIR / name), size)


def text_width(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def wrap(draw, text, fnt, max_width, max_lines):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if text_width(draw, trial, fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and text_width(draw, last + "...", fnt) > max_width:
            last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
        lines[-1] = last + "..."
    return lines


def draw_wrapped(draw, x, y, text, fnt, fill, max_width, leading, max_lines):
    for line in wrap(draw, text, fnt, max_width, max_lines):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=RULE):
    draw.line((x0, y, x1, y), fill=fill, width=width)


def kicker(draw, x, y, text, fill=ACCENT):
    draw.text((x, y), text, font=font(13, bold=True), fill=fill)


def panel(draw, x, y, w, h):
    draw.rectangle((x, y, x + w, y + h), fill=PANEL, outline=RULE, width=1)


def draw_tanker(draw, x, y, scale, flame=True):
    hull = [
        (x, y + 34 * scale),
        (x + 18 * scale, y + 48 * scale),
        (x + 118 * scale, y + 48 * scale),
        (x + 138 * scale, y + 34 * scale),
        (x + 126 * scale, y + 28 * scale),
        (x + 14 * scale, y + 28 * scale),
    ]
    draw.polygon(hull, fill=INK)
    draw.rectangle((x + 88 * scale, y + 8 * scale, x + 112 * scale, y + 28 * scale), fill=INK)
    draw.rectangle((x + 24 * scale, y + 18 * scale, x + 78 * scale, y + 28 * scale), fill=(52, 52, 52))
    if flame:
        for dx, dy, s in ((42, 2, 18), (62, -8, 24), (82, 0, 16)):
            fx = x + dx * scale
            fy = y + dy * scale
            draw.polygon(
                [(fx, fy + s * scale), (fx + 7 * scale, fy), (fx + 14 * scale, fy + s * scale)],
                fill=ACCENT,
            )
            draw.polygon(
                [(fx + 4 * scale, fy + s * scale), (fx + 7 * scale, fy + 6 * scale), (fx + 10 * scale, fy + s * scale)],
                fill=GOLD,
            )


def lead_picture(draw, x, y, w, h):
    draw.rectangle((x, y, x + w, y + h), fill=(224, 232, 236), outline=RULE, width=1)
    horizon = y + h - 42
    draw.rectangle((x + 1, horizon, x + w - 1, y + h - 1), fill=(54, 96, 124))
    for i in range(5):
        yy = horizon + 8 + i * 7
        draw.line((x + 10 + (i % 2) * 14, yy, x + w - 18, yy), fill=(150, 190, 205), width=2)
    draw.ellipse((x + 18, y + 16, x + 52, y + 50), outline=ACCENT, width=3)
    draw.line((x + 35, y + 8, x + 35, y + 58), fill=ACCENT, width=2)
    draw.line((x + 10, y + 33, x + 60, y + 33), fill=ACCENT, width=2)
    draw_tanker(draw, x + 52, y + 52, 1.0, flame=True)
    draw_tanker(draw, x + 126, y + 98, 0.62, flame=True)
    draw.text((x + 10, y + h - 20), "STRAIT OF HORMUZ", font=font(11, bold=True), fill=(255, 255, 255))


def number_rail(draw, x, y, w, h):
    panel(draw, x, y, w, h)
    draw.rectangle((x, y, x + w, y + 30), fill=INK)
    draw.text((x + 12, y + 7), "THE DAY IN NUMBERS", font=font(15, bold=True), fill=(255, 255, 255))
    rows = [
        ("50,000", "Dow closes above the mark for the first time"),
        ("-6.16%", "Seoul shares slide; Nikkei falls 2.78%"),
        ("31", "dead in the Cairo fuel-tanker fire"),
        ("19", "civilians killed by Sudan drone strikes"),
        ("1st", "Pakistani astronaut reaches Tiangong"),
    ]
    yy = y + 42
    for number, label in rows:
        draw.text((x + 12, yy), number, font=font(25, bold=True), fill=ACCENT)
        draw_wrapped(draw, x + 118, yy + 2, label, font(13), INK, w - 130, 16, 2)
        yy += 40
        if number != rows[-1][0]:
            rule(draw, x + 12, yy - 6, x + w - 12, width=1)


def card(draw, x, y, w, h, region, headline, body, *, small=False, tag=""):
    panel(draw, x, y, w, h)
    draw.rectangle((x, y, x + w, y + 5), fill=ACCENT)
    kicker(draw, x + 10, y + 11, region)
    head_size = 20 if small else 22
    body_size = 13 if small else 14
    yy = draw_wrapped(
        draw,
        x + 10,
        y + 28,
        headline,
        font(head_size, serif=True, bold=True),
        INK,
        w - 20,
        head_size + 2,
        3 if small else 2,
    )
    body_top = yy + 3
    body_leading = body_size + 3
    room = (y + h - 28) - body_top
    max_body_lines = max(1, min(4, room // body_leading))
    draw_wrapped(draw, x + 10, body_top, body, font(body_size), SOFT, w - 20, body_leading, max_body_lines)
    if tag:
        rule(draw, x + 10, y + h - 24, x + w - 10, width=1)
        draw.text((x + 10, y + h - 19), tag, font=font(11, bold=True), fill=ACCENT)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    margin = 28

    draw.text((margin, 22), "THE WORLD IN ONE IMAGE", font=font(15, bold=True), fill=ACCENT)
    draw.text((W - margin - text_width(draw, "WORLD NEWS", font(15, bold=True)), 22), "WORLD NEWS", font=font(15, bold=True), fill=INK)
    weekday = "W E D N E S D A Y"
    draw.text(((W - text_width(draw, weekday, font(18, bold=True))) // 2, 48), weekday, font=font(18, bold=True), fill=SOFT)
    date = "25 NOVEMBER 2026"
    draw.text(((W - text_width(draw, date, font(64, serif=True, bold=True))) // 2, 72), date, font=font(64, serif=True, bold=True), fill=INK)
    sub = "Hormuz fire  •  Gaza strike  •  Dow 50,000  •  first Pakistani in orbit"
    draw.text(((W - text_width(draw, sub, font(17, bold=True))) // 2, 146), sub, font=font(17, bold=True), fill=BLUE)
    rule(draw, margin, 178, W - margin, width=3, fill=INK)
    rule(draw, margin, 184, W - margin, width=1)

    lead_x, lead_y, lead_w, lead_h = margin, 196, 640, 252
    panel(draw, lead_x, lead_y, lead_w, lead_h)
    draw.rectangle((lead_x, lead_y, lead_x + lead_w, lead_y + 6), fill=ACCENT)
    kicker(draw, lead_x + 14, lead_y + 16, "MIDDLE EAST  •  STRAIT OF HORMUZ")
    draw_wrapped(draw, lead_x + 14, lead_y + 38, "Tankers ablaze after mine strikes", font(38, serif=True, bold=True), INK, 372, 41, 3)
    draw_wrapped(
        draw,
        lead_x + 14,
        lead_y + 162,
        "Tehran says two oil carriers hit naval mines, exploded and burned in the chokepoint, raising fears for Gulf shipping.",
        font(16),
        SOFT,
        372,
        20,
        3,
    )
    lead_picture(draw, lead_x + 402, lead_y + 42, 224, 164)
    draw.text((lead_x + 14, lead_y + 226), "2 carriers  •  naval mines  •  shipping at risk", font=font(13, bold=True), fill=ACCENT)

    number_rail(draw, 684, lead_y, 312, lead_h)

    cards = [
        ("GAZA", "Hamas security chief killed in strike", "Israel killed Mohammad Abuelouf; his wife and two children also died.", "WIFE AND TWO CHILDREN KILLED"),
        ("UKRAINE", "Odesa strike, refineries hit", "Russian strike killed two near Odesa, hurt three incl. a child; drones hit Rosneft plants.", "SYZRAN  •  KUIBYSHEV"),
        ("SPACE", "First Pakistani reaches Tiangong", "Shenzhou-24 docked with China's station carrying Muhammad Zeeshan Ali, its first foreign astronaut.", "SHENZHOU-24  •  TIANGONG"),
        ("MARKETS", "Asia sinks as Dow makes history", "Seoul and Tokyo fell hard while the Dow closed above 50,000; Nvidia slid about 6% after a 31.5% surge.", "KOSPI -6.16%  •  NIKKEI -2.78%"),
        ("US COURTS", "Huawei convicted in Brooklyn", "A jury found the company guilty in a bank-fraud and trade-secrets case.", "BANK FRAUD  •  TRADE SECRETS"),
        ("CLIMATE", "Pope laments COP31 stalemate", "Leo XIV voiced concern after the climate talks failed to reach a deal.", "NO DEAL AT COP31"),
    ]
    col_x = [28, 355, 682]
    row_y = [458, 628]
    for idx, (region, headline, body, tag) in enumerate(cards):
        card(draw, col_x[idx % 3], row_y[idx // 3], 314, 160, region, headline, body, tag=tag)

    bottom = [
        ("PACIFIC", "Solomons pact bars foreign base", "Australia and the Solomons signed a treaty ruling out a foreign base.", "NO FOREIGN BASE"),
        ("SUDAN", "Drone strikes kill 19 civilians", "RSF attacks hit two cities, adding to the war's civilian toll.", "TWO CITIES HIT"),
        ("EGYPT", "Cairo tanker fire kills at least 31", "A fuel-tanker crash became a blaze in the capital.", "AT LEAST 31 DEAD"),
        ("SAUDI", "Houthi strikes hit oil and capital", "Ras Tanura refinery attacked; Riyadh tower strike injured 11.", "11 INJURED IN RIYADH"),
    ]
    bx = [28, 272, 516, 760]
    for idx, (region, headline, body, tag) in enumerate(bottom):
        card(draw, bx[idx], 798, 235, 156, region, headline, body, small=True, tag=tag)

    rule(draw, margin, 962, W - margin, width=2, fill=INK)
    footer = "Wednesday 25 November 2026  •  one day's world news, summed up in one image"
    draw.text(((W - text_width(draw, footer, font(15, bold=True))) // 2, 972), footer, font=font(15, bold=True), fill=INK)
    draw.text((margin, 994), "Hormuz • Gaza • Ukraine • Space • Markets • Courts • Climate • Pacific • Sudan • Egypt • Saudi", font=font(12), fill=SOFT)

    out = Path(__file__).with_name("entry.png")
    img.save(out, format="PNG", optimize=True, compress_level=9)


if __name__ == "__main__":
    main()
