#!/usr/bin/env python3
"""Draws the slide diagrams for the WebRTC lightning talk as SVG."""
import math
from pathlib import Path

OUT = Path(__file__).parent
INK = "#1f2937"
MUTE = "#6b7280"
BLUE = "#2563eb"
BLUE_LT = "#dbeafe"
RED = "#dc2626"
GREEN = "#16a34a"
AMBER = "#d97706"
AMBER_LT = "#fef3c7"
FONT = "font-family='Helvetica Neue, Helvetica, Arial, sans-serif'"

HEAD = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}' "
        "width='{w}' height='{h}' {font}>\n"
        "<defs>\n"
        "<marker id='arr' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto-start-reverse'>"
        "<path d='M0 0L10 5L0 10z' fill='{ink}'/></marker>\n"
        "<marker id='arrb' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto-start-reverse'>"
        "<path d='M0 0L10 5L0 10z' fill='{blue}'/></marker>\n"
        "<marker id='arrr' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto-start-reverse'>"
        "<path d='M0 0L10 5L0 10z' fill='{red}'/></marker>\n"
        "<marker id='arrg' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto-start-reverse'>"
        "<path d='M0 0L10 5L0 10z' fill='#16a34a'/></marker>\n"
        "<marker id='arra' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto-start-reverse'>"
        "<path d='M0 0L10 5L0 10z' fill='#d97706'/></marker>\n"
        "<marker id='arrm' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto-start-reverse'>"
        "<path d='M0 0L10 5L0 10z' fill='#6b7280'/></marker>\n"
        "<marker id='arrl' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto-start-reverse'>"
        "<path d='M0 0L10 5L0 10z' fill='#cbd5e1'/></marker>\n"
        "</defs>\n")


def svg(name, w, h, body):
    s = HEAD.format(w=w, h=h, font=FONT, ink=INK, blue=BLUE, red=RED) + body + "</svg>\n"
    (OUT / name).write_text(s)


def text(x, y, s, size=18, fill=INK, anchor="middle", weight="normal", style="normal"):
    return (f"<text x='{x}' y='{y}' font-size='{size}' fill='{fill}' text-anchor='{anchor}' "
            f"font-weight='{weight}' font-style='{style}'>{s}</text>\n")


def laptop(cx, cy, label, scale=1.0, color=BLUE):
    """A little laptop glyph centred at (cx, cy) with a label below."""
    w, h = 70 * scale, 44 * scale
    x, y = cx - w / 2, cy - h / 2
    s = f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='4' fill='white' stroke='{INK}' stroke-width='2'/>\n"
    s += f"<rect x='{x+5*scale}' y='{y+5*scale}' width='{w-10*scale}' height='{h-14*scale}' rx='2' fill='{color}' opacity='0.18'/>\n"
    s += f"<rect x='{x-8*scale}' y='{y+h}' width='{w+16*scale}' height='{6*scale}' rx='2' fill='{INK}'/>\n"
    if label:
        s += text(cx, cy + h / 2 + 28 * scale, label, size=17 * scale)
    return s


def person(cx, cy, label, r=16, fill=BLUE_LT, stroke=BLUE, label_dy=None, label_size=15):
    s = f"<circle cx='{cx}' cy='{cy-r*0.45}' r='{r*0.45}' fill='{fill}' stroke='{stroke}' stroke-width='2'/>\n"
    s += (f"<path d='M{cx-r} {cy+r} a{r} {r} 0 0 1 {2*r} 0 z' fill='{fill}' stroke='{stroke}' stroke-width='2'/>\n")
    if label:
        s += text(cx, cy + r + (label_dy or 20), label, size=label_size)
    return s


def arrow(x1, y1, x2, y2, color=INK, width=2.5, dash=None, marker="arr", both=False):
    d = f" stroke-dasharray='{dash}'" if dash else ""
    ms = " marker-start='url(#%s)'" % marker if both else ""
    return (f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{color}' stroke-width='{width}'{d} "
            f"marker-end='url(#{marker})'{ms}/>\n")


def box(x, y, w, h, label, sub=None, fill="white", stroke=INK, size=18, rx=8, dashed=False):
    d = " stroke-dasharray='6 5'" if dashed else ""
    s = f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{rx}' fill='{fill}' stroke='{stroke}' stroke-width='2'{d}/>\n"
    cy = y + h / 2
    if sub:
        s += text(x + w / 2, cy - 4, label, size=size, weight="bold")
        s += text(x + w / 2, cy + 18, sub, size=size - 4, fill=MUTE)
    else:
        s += text(x + w / 2, cy + size * 0.35, label, size=size, weight="bold")
    return s


# 1. The simple picture --------------------------------------------------
b = laptop(150, 150, "your browser", 1.4)
b += laptop(810, 150, "their browser", 1.4)
b += arrow(215, 150, 740, 150, BLUE, 5, marker="arrb")
b += text(480, 130, "video", size=22, fill=BLUE, weight="bold")
b += text(150, 75, "camera", size=17, fill=MUTE)
b += text(810, 75, "screen", size=17, fill=MUTE)
svg("01-simple.svg", 960, 260, b)

# 2. The map -----------------------------------------------------------
b = f"<rect x='20' y='20' width='920' height='400' rx='14' fill='#f8fafc' stroke='{INK}' stroke-width='2'/>\n"
# grid
for gx in range(20, 941, 46):
    b += f"<line x1='{gx}' y1='20' x2='{gx}' y2='420' stroke='#e5e7eb' stroke-width='1'/>\n"
for gy in range(20, 421, 46):
    b += f"<line x1='20' y1='{gy}' x2='940' y2='{gy}' stroke='#e5e7eb' stroke-width='1'/>\n"
b += text(40, 48, "the map", size=16, fill=MUTE, anchor="start", style="italic")
# meeting room
b += f"<rect x='560' y='110' width='340' height='270' rx='10' fill='{AMBER_LT}' stroke='{AMBER}' stroke-width='2.5'/>\n"
b += text(730, 140, "meeting room", size=18, fill=AMBER, weight="bold")
b += text(730, 162, "everyone in here sees everyone", size=14, fill=MUTE)
for (px, py) in [(640, 240), (730, 220), (820, 250), (690, 320), (790, 330)]:
    b += person(px, py, None, r=16, fill=AMBER_LT, stroke=AMBER)
# you and Sam, with offer/accept
b += person(150, 250, "you", r=20)
b += person(400, 250, "Sam", r=20)
b += arrow(185, 240, 360, 240, BLUE, 3, marker="arrb")
b += text(272, 228, "offer video", size=15, fill=BLUE)
b += arrow(365, 262, 190, 262, GREEN, 3, dash="6 4", marker="arrg")
b += text(272, 290, "accept", size=15, fill=GREEN)
# legend
b += text(40, 390, "walk up to someone → offer your video → they accept", size=15, fill=INK, anchor="start")
b += text(40, 410, "step into a room → everyone in the room sees you", size=15, fill=INK, anchor="start")
svg("02-map.svg", 960, 440, b)

# 3. The bouncer --------------------------------------------------------
def house(x, y, w, h, who, side):
    s = f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='10' fill='white' stroke='{INK}' stroke-width='2.5'/>\n"
    s += text(x + w / 2, y - 14, who, size=22, weight="bold")
    s += laptop(x + w / 2, y + 70, None, 1.0)
    s += text(x + w / 2, y + 120, "home / office", size=13, fill=MUTE)
    # the router is the doorman on the wall facing the internet
    dx = x + w if side == "left" else x
    s += f"<rect x='{dx-28}' y='{y+h-130}' width='56' height='130' rx='6' fill='{INK}'/>\n"
    s += text(dx, y + h - 72, "router", size=14, fill="white", weight="bold")
    s += text(dx, y + h - 52, "(the", size=12, fill="white")
    s += text(dx, y + h - 36, "bouncer)", size=12, fill="white")
    return s

b = house(60, 70, 240, 280, "you", "left")
b += house(660, 70, 240, 280, "Sam", "right")
# outbound OK
b += arrow(300, 140, 440, 140, GREEN, 3.5, marker="arrg")
b += text(370, 128, "going out: fine", size=15, fill=GREEN)
b += arrow(660, 140, 520, 140, GREEN, 3.5, marker="arrg")
b += text(590, 128, "going out: fine", size=15, fill=GREEN)
# inbound blocked
b += arrow(445, 290, 335, 290, RED, 3.5, marker="arrr")
b += text(390, 326, "✕  nobody comes in", size=15, fill=RED, weight="bold")
b += arrow(515, 290, 625, 290, RED, 3.5, marker="arrr")
b += text(570, 326, "✕  nobody comes in", size=15, fill=RED, weight="bold")
b += text(480, 222, "the internet", size=18, fill=MUTE, style="italic")
svg("03-bouncer.svg", 960, 380, b)

# 4. STUN / TURN ----------------------------------------------------------
b = ""
# STUN half
b += text(40, 40, "STUN", size=24, fill=BLUE, weight="bold", anchor="start")
b += text(118, 40, "“Can you read my house number to me?”", size=18, fill=INK, anchor="start", style="italic")
b += laptop(110, 130, "you", 1.1)
b += box(390, 100, 150, 60, "friend", "STUN server", fill=BLUE_LT, stroke=BLUE, size=17)
b += arrow(150, 120, 385, 120, INK, 2.5)
b += text(268, 110, "“where am I?”", size=14, fill=MUTE)
b += arrow(385, 142, 155, 142, BLUE, 2.5, marker="arrb")
b += text(268, 170, "“you’re at 203.0.113.7”", size=14, fill=BLUE)
b += text(620, 128, "→ now you can tell Sam where to knock", size=16, fill=MUTE, anchor="start")
b += f"<line x1='40' y1='215' x2='920' y2='215' stroke='#e5e7eb' stroke-width='2'/>\n"
# TURN half
b += text(40, 260, "TURN", size=24, fill=AMBER, weight="bold", anchor="start")
b += text(118, 260, "“The door’s locked from outside. Can you carry the letters?”", size=18, fill=INK, anchor="start", style="italic")
b += laptop(110, 350, "you", 1.1)
b += laptop(850, 350, "Sam", 1.1)
b += box(390, 320, 180, 60, "friend", "TURN relay", fill=AMBER_LT, stroke=AMBER, size=17)
b += arrow(150, 340, 385, 340, INK, 2.5)
b += arrow(385, 362, 155, 362, INK, 2.5)
b += arrow(810, 340, 575, 340, INK, 2.5)
b += arrow(575, 362, 805, 362, INK, 2.5)
b += text(268, 325, "sealed letters", size=13, fill=MUTE)
b += text(692, 325, "sealed letters", size=13, fill=MUTE)
b += text(480, 418, "both of you walk out to the friend; nobody has to open their door", size=15, fill=MUTE, style="italic")
svg("04-stun-turn.svg", 960, 440, b)

# 5. Mesh: you send nine copies -------------------------------------------
names = ["Sam", "Ana", "Lee", "Kim", "Raj", "Jo", "Max", "Eva", "Dev"]
b = ""
b += laptop(130, 230, "you", 1.5)
b += text(130, 322, "camera + screen", size=15, fill=MUTE)
for i, n in enumerate(names):
    y = 40 + i * 50
    b += arrow(190, 230, 445, y + 2, BLUE, 2.5, marker="arrb")
    b += person(470, y, n, r=12, label_dy=6, label_size=0)
    b += text(492, y + 6, n, size=15, anchor="start")
b += text(330, 475, "9 separate copies, 9 separate encoders", size=15, fill=BLUE, weight="bold")
# the sums
x0 = 600
b += f"<rect x='{x0-20}' y='60' width='360' height='300' rx='10' fill='#f8fafc' stroke='#e5e7eb' stroke-width='2'/>\n"
rows = [("9 × your camera", "≈ 10–13 Mbps up", INK),
        ("9 × your screen", "≈ 20–30 Mbps up", INK),
        ("", "", None),
        ("you, sending", "≈ 40 Mbps up", RED),
        ("your home internet", "≈ 10–20 Mbps up", GREEN)]
y = 105
for lab, val, col in rows:
    if col is None:
        b += f"<line x1='{x0}' y1='{y-20}' x2='{x0+320}' y2='{y-20}' stroke='{INK}' stroke-width='1.5'/>\n"
        y += 10
        continue
    w = "bold" if col in (RED, GREEN) else "normal"
    b += text(x0, y, lab, size=17, fill=col, anchor="start", weight=w)
    b += text(x0 + 320, y, val, size=17, fill=col, anchor="end", weight=w)
    y += 48
b += text(x0 + 160, 335, "…and all nine of them are doing the same thing", size=14, fill=MUTE, style="italic")
svg("05-mesh.svg", 960, 500, b)

# 6. The mail room (SFU) ----------------------------------------------------
b = ""
cx, cy = 440, 240
b += box(cx - 90, cy - 50, 180, 100, "SFU", "the mail room", fill=AMBER_LT, stroke=AMBER, size=22)
R = 165
people = ["you"] + names
for i, n in enumerate(people):
    a = -math.pi / 2 + i * 2 * math.pi / len(people)
    ca, sa = math.cos(a), math.sin(a)
    px, py = cx + R * ca, cy + R * sa
    isyou = n == "you"
    b += person(px, py, None, r=14, fill=(BLUE_LT if isyou else "white"), stroke=(BLUE if isyou else INK))
    # label outward, along the spoke
    lx, ly = cx + (R + 38) * ca, cy + (R + 38) * sa + 5
    b += text(lx, ly, n, size=15, weight=("bold" if isyou else "normal"), fill=(BLUE if isyou else INK))
    # arrow between box edge and person edge
    # box edge along this spoke: intersect ray with the 180x100 rect
    tx = (90 / abs(ca)) if ca else 1e9
    ty = (50 / abs(sa)) if sa else 1e9
    t = min(tx, ty) + 6
    bx, by = cx + t * ca, cy + t * sa
    sx, sy = px - 24 * ca, py - 24 * sa
    if isyou:
        b += arrow(sx, sy, bx, by, BLUE, 3.5, marker="arrb")
    else:
        b += arrow(bx, by, sx, sy, INK, 2, marker="arr")
b += text(cx + 16, 150, "you send ONE copy", size=15, fill=BLUE, weight="bold", anchor="start")
b += text(700, 80, "the server makes the copies", size=15, fill=MUTE, anchor="start")
b += text(700, 102, "and delivers them only to people", size=15, fill=MUTE, anchor="start")
b += text(700, 124, "who accepted, or are in the room", size=15, fill=MUTE, anchor="start")
# sums
b += f"<rect x='680' y='300' width='260' height='130' rx='10' fill='#f8fafc' stroke='#e5e7eb' stroke-width='2'/>\n"
b += text(700, 338, "you, sending", size=16, anchor="start")
b += text(920, 338, "≈ 4 Mbps up", size=16, anchor="end", fill=GREEN, weight="bold")
b += text(920, 358, "(was 40)", size=13, anchor="end", fill=MUTE)
b += text(700, 398, "encoders running", size=16, anchor="start")
b += text(920, 398, "2", size=16, anchor="end", fill=GREEN, weight="bold")
b += text(920, 418, "(was 18)", size=13, anchor="end", fill=MUTE)
svg("06-sfu.svg", 960, 480, b)

# 7. The real picture ------------------------------------------------------
b = ""
b += box(330, 30, 300, 70, "signaling server", "“Sam, JJ offered you video. Accept?”", fill="white", stroke=INK, size=18)
b += laptop(140, 250, "your browser", 1.3)
b += laptop(820, 250, "Sam's browser", 1.3)
# signaling links
b += arrow(170, 215, 345, 100, MUTE, 2, dash="6 5", marker="arrm", both=True)
b += arrow(790, 215, 615, 100, MUTE, 2, dash="6 5", marker="arrm", both=True)
# STUN/TURN
b += box(395, 170, 170, 64, "STUN / TURN", "address + letters", fill=BLUE_LT, stroke=BLUE, size=16)
b += arrow(195, 240, 392, 205, BLUE, 2, marker="arrb")
b += arrow(765, 240, 568, 205, BLUE, 2, marker="arrb")
# SFU
b += box(380, 330, 200, 90, "SFU", "the mail room", fill=AMBER_LT, stroke=AMBER, size=20)
b += arrow(195, 275, 378, 370, AMBER, 4, marker="arra")
b += arrow(582, 370, 765, 275, AMBER, 4, marker="arra")
b += text(360, 440, "one copy in", size=14, fill=AMBER, weight="bold", anchor="end")
b += text(600, 440, "copies out, only to the list", size=14, fill=AMBER, weight="bold", anchor="start")
# the ghost of slide 1
b += arrow(215, 150, 745, 150, "#cbd5e1", 4, dash="3 8", marker="arrl")
b += text(480, 140, "the arrow we imagined", size=13, fill="#94a3b8", style="italic")
svg("07-real.svg", 960, 450, b)

print("done")
