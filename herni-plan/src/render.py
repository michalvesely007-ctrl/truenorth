# -*- coding: utf-8 -*-
"""Vykreslí herní plán do SVG (mm) a uloží layout.json s kontrolními daty."""
import json, math, html, sys
import numpy as np
import build as B
from content import EV

INK = "#3a2716"
TAN = "#e6cfa2"
GREEN = "#2e7a43"
GREEN_D = "#1f5a30"
CREAM = "#fffaf0"
GOLD = "#e8b443"
DEAD = "#cdb48c"
FONT_CSS = """
@font-face{font-family:'Carlito';src:url('file:///usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf');}
@font-face{font-family:'Carlito';font-weight:bold;src:url('file:///usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf');}
@font-face{font-family:'Carlito';font-style:italic;src:url('file:///usr/share/fonts/truetype/crosextra/Carlito-Italic.ttf');}
@font-face{font-family:'Caladea';font-weight:bold;font-style:italic;src:url('file:///usr/share/fonts/truetype/crosextra/Caladea-BoldItalic.ttf');}
@font-face{font-family:'Caladea';font-weight:bold;src:url('file:///usr/share/fonts/truetype/crosextra/Caladea-Bold.ttf');}
text{font-family:'Carlito',sans-serif;}
"""

# ---------------------------------------------------------------- pevné zóny
TITLE = (318, 6, 548, 42)            # kartuš s názvem
LEGEND = (8, 6, 112, 56)            # legenda a stručná pravidla
DICE = (240, 196, 304, 222)          # prostor pro hod kostkou
START = (40, 342, 13)               # střed a poloměr startu
# hlavy postav v podkladu – popisky ani štítky je nesmějí zakrýt
HEADS = [(8, 106, 27, 124), (25, 176, 43, 194), (17, 266, 42, 296), (229, 288, 246, 305),
         (255, 296, 273, 313), (68, 310, 83, 325), (430, 342, 447, 360), (518, 246, 535, 262)]
SOFT = []                            # měkké zóny – doplní se hlavami postav níže


def esc(s):
    return html.escape(s, quote=False)


def hairy(cx, cy, r, n=None, col=INK, w=0.16, l=1.0):
    n = n or int(2 * math.pi * r / 0.85)
    d = []
    for k in range(n):
        a = 2 * math.pi * k / n
        c, s = math.cos(a), math.sin(a)
        d.append(f"M{cx + c * (r + 0.15):.2f},{cy + s * (r + 0.15):.2f}L{cx + c * (r + l):.2f},{cy + s * (r + l):.2f}")
    return f'<path d="{"".join(d)}" stroke="{col}" stroke-width="{w}" fill="none"/>'


def tile_svg(t):
    x, y, r = t["x"], t["y"], t["r"]
    k = t["kind"]
    o = []
    if k == "finish":
        rays = []
        for i in range(32):
            a = 2 * math.pi * i / 32
            rr = r + (6 if i % 2 == 0 else 3.5)
            rays.append(f"{x + math.cos(a) * rr:.2f},{y + math.sin(a) * rr:.2f}")
            a2 = a + math.pi / 32
            rays.append(f"{x + math.cos(a2) * (r + 0.8):.2f},{y + math.sin(a2) * (r + 0.8):.2f}")
        o.append(f'<polygon points="{" ".join(rays)}" fill="{GOLD}" stroke="{INK}" stroke-width="0.3"/>')
        o.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff3cf" stroke="{INK}" stroke-width="0.6"/>')
        o.append(f'<circle cx="{x}" cy="{y}" r="{r - 1.4}" fill="none" stroke="{INK}" stroke-width="0.3"/>')
        o.append(f'<text x="{x}" y="{y - 1.2}" font-size="6.2" font-weight="bold" text-anchor="middle" fill="{INK}">CÍL</text>')
        o.append(f'<text x="{x}" y="{y + 4.6}" font-size="3.6" font-weight="bold" text-anchor="middle" fill="{INK}">150</text>')
        return "".join(o)
    o.append(hairy(x, y, r))
    if k in ("brown", "bbrown"):
        o.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{TAN}" stroke="{INK}" stroke-width="0.4"/>')
        col = INK
    elif k == "dead":
        o.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="url(#hatch)" stroke="{INK}" stroke-width="0.4" stroke-dasharray="1.2 0.6"/>')
        col = INK
    else:
        fill = GREEN
        o.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="0.5"/>')
        o.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r - 0.95}" fill="none" stroke="#fff" stroke-width="0.35"/>')
        if k == "fork":
            o.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r + 1.6}" fill="none" stroke="{INK}" stroke-width="0.55" stroke-dasharray="0.9 0.6"/>')
        if k == "dead_end":
            o.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r - 1.9}" fill="none" stroke="#fff" stroke-width="0.25" stroke-dasharray="0.6 0.5"/>')
        col = "#fff"
    fs = 3.5 if t["trunk"] else 2.9
    lab = t["label"]
    if k == "fork":
        # symbol rozcestí nad číslem
        o.append(f'<path d="M{x:.2f},{y - 1.2:.2f}v-1.6M{x:.2f},{y - 2.8:.2f}l-1.3,-1.1M{x:.2f},{y - 2.8:.2f}l1.3,-1.1" stroke="#fff" stroke-width="0.45" fill="none" stroke-linecap="round"/>')
        o.append(f'<text x="{x:.2f}" y="{y + 2.9:.2f}" font-size="{fs}" font-weight="bold" text-anchor="middle" fill="{col}">{lab}</text>')
    else:
        o.append(f'<text x="{x:.2f}" y="{y + fs * 0.35:.2f}" font-size="{fs}" font-weight="bold" text-anchor="middle" fill="{col}">{lab}</text>')
    return "".join(o)


def poly(points, **kw):
    attrs = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in kw.items())
    d = "M" + "L".join(f"{p[0]:.2f},{p[1]:.2f}" for p in points)
    return f'<path d="{d}" fill="none" {attrs}/>'


def pill(x, y, text, size=2.6, fill=CREAM, col=INK, bold=True):
    w = B.tw(text, "b" if bold else "r", size) + 2.4
    h = size + 1.6
    return (f'<rect x="{x - w / 2:.2f}" y="{y - h / 2:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{h / 2:.2f}" fill="{fill}" stroke="{INK}" stroke-width="0.3"/>'
            f'<text x="{x:.2f}" y="{y + size * 0.35:.2f}" font-size="{size}" font-weight="{"bold" if bold else "normal"}" text-anchor="middle" fill="{col}">{esc(text)}</text>'), (x - w / 2, y - h / 2, x + w / 2, y + h / 2)


def place_tag(txt, f, t1, tiles, others, side):
    """Štítek směru u začátku větve – hledá místo, kde nic nepřekrývá."""
    best = None
    dx, dy = t1["x"] - f["x"], t1["y"] - f["y"]
    ln = math.hypot(dx, dy) or 1
    ux, uy = dx / ln, dy / ln
    for along in (0.5, 1.0, 1.5, 2.0, 0.0):
        for off in (7, 9, 11, 13, -7, -9, -11, -13, 16, -16):
            sgn = 1 if side != "R" else -1
            px = f["x"] + ux * ln * along + (-uy) * 0 + uy * off * sgn
            py = f["y"] + uy * ln * along - ux * off * sgn
            svg, rect = pill(px, py, txt, size=2.5)
            if any(rect_circle(rect, t["x"], t["y"], t["r"] + 1.2) for t in tiles):
                continue
            if any(rr_overlap(rect, o) for o in others):
                continue
            d = abs(off) + along * 3
            if best is None or d < best[0]:
                best = (d, svg, rect)
    if best is None:
        return pill(f["x"] + uy * 9, f["y"] - ux * 9, txt, size=2.5)
    return best[1], best[2]


def rect_circle(r, cx, cy, rad):
    nx = min(max(cx, r[0]), r[2]); ny = min(max(cy, r[1]), r[3])
    return (nx - cx) ** 2 + (ny - cy) ** 2 < rad * rad


def rr_overlap(a, b, pad=1.0):
    return not (a[2] + pad <= b[0] or b[2] + pad <= a[0] or a[3] + pad <= b[1] or b[3] + pad <= a[1])


def label_svg(t, c):
    r = c["rect"]
    lay = c["lay"]
    o = []
    o.append(f'<line x1="{c["start"][0]:.2f}" y1="{c["start"][1]:.2f}" x2="{c["a"][0]:.2f}" y2="{c["a"][1]:.2f}" stroke="{INK}" stroke-width="0.45"/>')
    o.append(f'<circle cx="{c["start"][0]:.2f}" cy="{c["start"][1]:.2f}" r="0.75" fill="{INK}"/>')
    o.append(f'<circle cx="{c["a"][0]:.2f}" cy="{c["a"][1]:.2f}" r="0.55" fill="{INK}"/>')
    o.append(f'<rect x="{r[0]:.2f}" y="{r[1]:.2f}" width="{lay["w"]:.2f}" height="{lay["h"]:.2f}" rx="1.2" fill="{CREAM}" fill-opacity="0.94" stroke="{INK}" stroke-width="0.3"/>')
    x0 = r[0] + B.PAD
    y = r[1] + B.PAD + B.FS * 0.82
    # odznak s číslem pole
    bw = lay["badge_w"]
    o.append(f'<rect x="{x0:.2f}" y="{y - B.FS * 0.82:.2f}" width="{bw:.2f}" height="{B.FS * 1.08:.2f}" rx="0.7" fill="{GREEN}"/>')
    o.append(f'<text x="{x0 + bw / 2:.2f}" y="{y:.2f}" font-size="{B.FS:.3f}" font-weight="bold" text-anchor="middle" fill="#fff">{esc(t["label"])}</text>')
    first = True
    for line in lay["title"]:
        xs = x0 + (bw + 1.0 if first else 0)
        o.append(text_line(xs, y, line))
        y += B.LH
        first = False
    y += 0.5
    for line in lay["body"]:
        o.append(text_line(x0, y, line))
        y += B.LH
    return "".join(o)


def text_line(x, y, words):
    spans = []
    for i, runs in enumerate(words):
        for j, (w, st) in enumerate(runs):
            attr = {"b": ' font-weight="bold"', "i": ' font-style="italic"', "r": ""}[st]
            tail = " " if (j == len(runs) - 1 and i < len(words) - 1) else ""
            spans.append(f'<tspan{attr}>{esc(w)}{tail}</tspan>')
    return f'<text x="{x:.2f}" y="{y:.2f}" font-size="{B.FS:.3f}" fill="{INK}" xml:space="preserve">{"".join(spans)}</text>'


def main(out_svg="board.svg", out_json="layout.json", bg="podklad_150dpi.jpg"):
    tiles, branches, ev_tile, curve = B.build_geometry()
    by_label = {t["label"]: t for t in tiles}
    by_ev = {t["ev"]: t for t in tiles if t["ev"]}
    trunk = [t for t in tiles if t["trunk"]]

    o_conn, o_tags, tag_rects = [], [], []
    head_rects = list(HEADS)
    # spojnice hlavní trasy (jen mezi sousedy, ne přes rozcestí se slučováním)
    for a, b in zip(trunk, trunk[1:]):
        if a["ev"] in ("3", "17", "58"):
            continue
        o_conn.append(poly([(a["x"], a["y"]), (b["x"], b["y"])], stroke=INK, stroke_width=1.6, stroke_linecap="round"))
    for br in branches:
        f = by_ev[br["fork"]]
        seq = [f] + [by_label[l] for l in br["tiles"]]
        if br["join"]:
            seq.append(by_ev[br["join"]])
        dash = {"stroke_dasharray": "2 1"} if br["back"] else {}
        for a, b in zip(seq, seq[1:]):
            o_conn.append(poly([(a["x"], a["y"]), (b["x"], b["y"])], stroke=INK, stroke_width=1.3, stroke_linecap="round", **dash))
        t1 = by_label[br["tiles"][0]]
        # štítek směru na začátku větve
        fork_ev = br["fork"]
        if fork_ev == "3":
            txt = {"L": "5–6 ◄ ENVIRO", "S": "3–4 ▲ ESF", "R": "LES ► 1–2"}[br["side"]]
        elif fork_ev == "21":
            txt = {"L": "ANO ◄ VLEVO", "R": "NE ► VPRAVO"}[br["side"]]
        else:
            txt = {"L": "LICHÁ ◄ VLEVO", "R": "SUDÁ ► VPRAVO"}[br["side"]]
        svg, rect = place_tag(txt, f, t1, tiles, tag_rects + head_rects, br["side"])
        o_tags.append(svg)
        tag_rects.append(rect)
        if br["back"]:
            end = by_label[br["tiles"][-1]]
            # závora na konci slepé cesty
            ex, ey = end["tx"], end["ty"]
            cx, cy = end["x"] + ex * (end["r"] + 2.6), end["y"] + ey * (end["r"] + 2.6)
            pxn, pyn = -ey, ex
            bar = [(cx + pxn * 5, cy + pyn * 5), (cx - pxn * 5, cy - pyn * 5)]
            o_tags.append(poly(bar, stroke=INK, stroke_width=2.2))
            o_tags.append(poly(bar, stroke="#fff", stroke_width=1.4, stroke_dasharray="1.2 1.2"))
            back_t = by_ev[br["back"]]
            # štítek návratu za závorou
            tx_, ty_ = cx + ex * 5.2, cy + ey * 5.2
            svg2, rect2 = pill(tx_, ty_, f"SLEPÁ ↩ zpět na {back_t['label']}", size=2.5, fill="#f3d9d0")
            o_tags.append(svg2)
            tag_rects.append(rect2)

    zones = [TITLE, LEGEND, DICE, (START[0] - START[2] - 2, START[1] - START[2] - 2, START[0] + START[2] + 2, START[1] + START[2] + 2)]
    zones += tag_rects + HEADS[:2]   # Michal a Katka (horolezci) musí zůstat vidět
    fin = by_ev["60"]
    zones.append((fin["x"] - 19, fin["y"] - 19, fin["x"] + 19, fin["y"] + 19))
    prio = ["8", "E2", "E4", "L3", "V2", "V4", "5", "N4"]
    best = None
    import random
    rnd = random.Random(7)
    for it in range(150):
        placed = B.place_labels(tiles, ev_tile, zones, soft_zones=SOFT + HEADS, priority=prio, noise=(0 if it < 10 else 3 + (it % 5) * 3), seed=it)
        miss = [k for k, v in placed.items() if v is None]
        if best is None or len(miss) < best[0]:
            best = (len(miss), placed, list(prio), it)
        if not miss:
            break
        if False:
            placed = B.place_labels(tiles, ev_tile, zones, soft_zones=SOFT + HEADS, priority=prio, repair=True)
            miss = [k for k, v in placed.items() if v is None]
            if len(miss) < best[0]:
                best = (len(miss), placed)
            if not miss:
                break
        prio = miss + [p for p in prio if p not in miss]
        if it % 4 == 3:
            rnd.shuffle(prio)
    if best[0]:
        _, _, bp, bit = best
        rp = B.place_labels(tiles, ev_tile, zones, soft_zones=SOFT + HEADS, priority=bp,
                            noise=(0 if bit < 10 else 3 + (bit % 5) * 3), seed=bit, repair=True)
        if sum(v is None for v in rp.values()) < best[0]:
            best = (sum(v is None for v in rp.values()), rp)
    placed = best[1]

    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{B.W}mm" height="{B.H}mm" viewBox="0 0 {B.W} {B.H}">')
    o.append(f"<style>{FONT_CSS}</style>")
    o.append('<defs><pattern id="hatch" width="1.6" height="1.6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
             f'<rect width="1.6" height="1.6" fill="{DEAD}"/><line x1="0" y1="0" x2="0" y2="1.6" stroke="{INK}" stroke-width="0.45"/></pattern></defs>')
    o.append(f'<image href="{bg}" x="0" y="0" width="{B.W}" height="{B.H}" preserveAspectRatio="none"/>')
    o.extend(o_conn)
    # start
    sx, sy, sr = START
    t1 = by_label["1"]
    o.append(poly([(sx, sy), (t1["x"], t1["y"])], stroke=INK, stroke_width=1.6))
    o.append(hairy(sx, sy, sr, l=1.6, w=0.2))
    o.append(f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="#2c8c8c" stroke="{INK}" stroke-width="0.6"/>')
    o.append(f'<circle cx="{sx}" cy="{sy}" r="{sr - 1.3}" fill="none" stroke="#fff" stroke-width="0.35"/>')
    o.append(f'<text x="{sx}" y="{sy + 1.6}" font-size="5.2" font-weight="bold" text-anchor="middle" fill="#fff">START</text>')
    for t in tiles:
        o.append(tile_svg(t))
    o.extend(o_tags)
    for t in tiles:
        if t["ev"] and placed.get(t["label"]):
            o.append(label_svg(t, placed[t["label"]]))
    o.append(decorations())
    o.append("</svg>")
    open(out_svg, "w", encoding="utf-8").write("\n".join(o))
    data = dict(tiles=[{k: (float(v) if isinstance(v, (np.floating,)) else v) for k, v in t.items()} for t in tiles],
                branches=branches, ev_tile=ev_tile,
                labels={k: (None if v is None else dict(rect=v["rect"], a=v["a"], start=v["start"], w=v["lay"]["w"], h=v["lay"]["h"],
                                                          lines=len(v["lay"]["title"]) + len(v["lay"]["body"])))
                        for k, v in placed.items()},
                zones=zones)
    json.dump(data, open(out_json, "w", encoding="utf-8"), ensure_ascii=False, default=float, indent=1)
    missing = [k for k, v in placed.items() if v is None]
    print("popisky:", len(placed), "neumístěno:", missing)


def decorations():
    o = []
    x0, y0, x1, y1 = TITLE
    o.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="3" fill="{CREAM}" fill-opacity="0.93" stroke="{INK}" stroke-width="0.5"/>')
    o.append(f'<rect x="{x0 + 1.2}" y="{y0 + 1.2}" width="{x1 - x0 - 2.4}" height="{y1 - y0 - 2.4}" rx="2.2" fill="none" stroke="{INK}" stroke-width="0.25"/>')
    cx = (x0 + x1) / 2
    o.append(f'<text x="{cx}" y="{y0 + 17}" font-family="Caladea" font-size="14" font-weight="bold" font-style="italic" text-anchor="middle" fill="{INK}">Cesta šťastným životem</text>')
    o.append(f'<text x="{cx}" y="{y0 + 25.5}" font-size="5" font-style="italic" text-anchor="middle" fill="{INK}">150 herních polí · 150 let šťastného života</text>')
    o.append(f'<text x="{cx}" y="{y0 + 32.5}" font-size="4.2" font-weight="bold" text-anchor="middle" fill="{INK}">Na rozcestí hoď: LICHÁ (1·3·5) ◄ VLEVO   ·   SUDÁ (2·4·6) ► VPRAVO</text>')
    # prostor pro hod kostkou
    x0, y0, x1, y1 = DICE
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{(x1 - x0) / 2}" ry="{(y1 - y0) / 2}" fill="{CREAM}" fill-opacity="0.55" stroke="{INK}" stroke-width="0.5" stroke-dasharray="2 1.2"/>')
    o.append(f'<text x="{cx}" y="{cy - 1}" font-family="Caladea" font-size="5" font-weight="bold" font-style="italic" text-anchor="middle" fill="{INK}">Sem házej kostkou</text>')
    o.append(f'<text x="{cx}" y="{cy + 5}" font-size="3.4" text-anchor="middle" fill="{INK}">lichá ◄ vlevo · sudá ► vpravo</text>')
    for k, (dx, pipn) in enumerate(((-25.5, 5), (25.5, 2))):
        bx, by = cx + dx - 3, cy - 3
        o.append(f'<rect x="{bx}" y="{by}" width="6" height="6" rx="1.1" fill="#fff" stroke="{INK}" stroke-width="0.35"/>')
        pips = {5: [(1.5, 1.5), (4.5, 1.5), (3, 3), (1.5, 4.5), (4.5, 4.5)], 2: [(1.5, 1.5), (4.5, 4.5)]}[pipn]
        for px_, py_ in pips:
            o.append(f'<circle cx="{bx + px_}" cy="{by + py_}" r="0.55" fill="{INK}"/>')
    # legenda
    x0, y0, x1, y1 = LEGEND
    o.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="2.5" fill="{CREAM}" fill-opacity="0.93" stroke="{INK}" stroke-width="0.4"/>')
    o.append(f'<text x="{x0 + 4}" y="{y0 + 6}" font-size="3.6" font-weight="bold" fill="{INK}">Legenda</text>')
    items = [("brown", "běžné hnědé pole – bez úkolu"),
             ("green", "zelené akční pole – přečti popisek u pole"),
             ("fork", "rozcestí – hoď kostkou a vyber směr"),
             ("dead", "pole slepé cesty (šrafované)"),
             ("dead_end", "konec slepé cesty – vrať se na rozcestí")]
    yy = y0 + 12
    for kind, txt in items:
        o.append(tile_svg(dict(x=x0 + 8, y=yy, r=3.4, kind=kind, label="", trunk=True)))
        o.append(f'<text x="{x0 + 15}" y="{yy + 1.1}" font-size="{B.FS:.3f}" fill="{INK}">{esc(txt)}</text>')
        yy += 8.0
    return "".join(o)


if __name__ == "__main__":
    main()
