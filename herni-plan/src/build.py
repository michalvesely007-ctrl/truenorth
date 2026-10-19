# -*- coding: utf-8 -*-
"""Generátor herního plánu „Cesta k šťastnému životu?“.

Výstup: board.svg (rozměr desky v mm) + layout.json pro kontroly.
Všechny souřadnice jsou v milimetrech konečného tisku (2× A3 / 100 %).
"""
import json, math, re, html
import numpy as np
from PIL import ImageFont
from content import EV, FORKS
from numbering import build as build_numbering

W, H = 554.0, 392.0           # deska v mm
PT = 25.4 / 72                # 1 pt v mm
FS = 8 * PT                   # 8 pt
LH = FS * 1.13                # řádkování
PAD = 1.3
PITCH = 12.6                  # rozteč polí hlavní trasy
R_T = 5.7                     # poloměr pole hlavní trasy
R_B = 5.1                     # poloměr pole ve větvi
SEAM = W / 2                  # spoj listů A3

FONT_DIR = "/usr/share/fonts/truetype/crosextra/"
F_REG = FONT_DIR + "Carlito-Regular.ttf"
F_BOLD = FONT_DIR + "Carlito-Bold.ttf"
F_IT = FONT_DIR + "Carlito-Italic.ttf"
_fonts = {k: ImageFont.truetype(v, 1000) for k, v in
          dict(r=F_REG, b=F_BOLD, i=F_IT).items()}


def tw(text, style="r", fs=FS):
    return _fonts[style].getlength(text) / 1000 * fs


# ---------------------------------------------------------------- geometrie
def catmull(points, n=40):
    pts = np.array(points, float)
    pts = np.vstack([pts[0] * 2 - pts[1], pts, pts[-1] * 2 - pts[-2]])
    out = []
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(pts[-2])
    return np.array(out)


class Curve:
    def __init__(self, pts):
        self.p = np.asarray(pts, float)
        d = np.linalg.norm(np.diff(self.p, axis=0), axis=1)
        self.s = np.concatenate([[0], np.cumsum(d)])
        self.L = self.s[-1]

    def at(self, s):
        s = min(max(s, 0), self.L)
        i = int(np.searchsorted(self.s, s, side="right") - 1)
        i = min(i, len(self.p) - 2)
        t = (s - self.s[i]) / max(self.s[i + 1] - self.s[i], 1e-9)
        pt = self.p[i] + (self.p[i + 1] - self.p[i]) * t
        tg = self.p[i + 1] - self.p[i]
        tg = tg / np.linalg.norm(tg)
        return pt, tg


def left_normal(tg):
    # obrazovkové souřadnice (y dolů): vlevo od směru (dx,dy) je (dy,-dx)
    return np.array([tg[1], -tg[0]])


# Hlavní trasa – ručně laděné body (mm). Klikatá cesta krajinou:
# start dole vlevo u turisty, cíl nahoře vlevo pod horami.
WAYPOINTS = [
    (66, 350), (100, 350), (135, 350), (170, 350), (205, 350), (236, 356),
    (262, 366), (300, 362), (338, 346), (372, 344), (408, 358), (446, 364),
    (482, 352), (512, 326), (520, 296), (506, 268), (476, 254),
    (440, 262), (404, 276), (368, 272), (338, 252), (306, 240), (272, 250),
    (240, 266), (204, 266), (172, 248), (142, 236), (110, 240), (80, 252),
    (54, 238), (40, 210), (48, 182), (74, 168),
    (106, 174), (140, 186), (174, 182), (204, 164), (236, 152), (270, 160),
    (302, 176), (336, 178), (368, 160), (398, 146), (432, 150), (466, 162),
    (496, 150), (514, 124), (508, 96), (482, 80), (450, 84),
    (418, 98), (384, 102), (352, 88), (320, 76), (286, 82), (252, 98),
    (218, 102), (186, 88), (156, 78), (124, 82), (94, 96), (70, 118), (60, 134),
]


def build_geometry():
    trunk, branches, ev_tile = build_numbering()
    curve = Curve(catmull(WAYPOINTS, 60))
    # pozice podél trasy (v roztečích); za rozcestím se slučujícími větvemi mezera
    gap_after = {"3": 7, "17": 5, "58": 9}
    s = 0.0
    for t in trunk:
        t["s"] = s
        s += PITCH * gap_after.get(t["ev"], 1) if t["ev"] in gap_after else PITCH
    need = trunk[-1]["s"]
    if need > curve.L:
        raise SystemExit(f"trasa krátká: potřeba {need:.0f} mm, k dispozici {curve.L:.0f} mm")
    tiles = []
    for t in trunk:
        p, tg = curve.at(t["s"])
        kind = "brown"
        if t["ev"]:
            kind = "fork" if t["ev"] in FORKS else "green"
        if t["ev"] == "60":
            kind = "finish"
        tiles.append(dict(label=str(t["num"]), ev=t["ev"], x=p[0], y=p[1],
                          tx=tg[0], ty=tg[1], kind=kind, r=R_T, s=t["s"], trunk=True))
    by_ev = {t["ev"]: t for t in tiles if t["ev"]}
    by_ev["60"]["r"] = 11.5

    branch_out = []
    order = [b for b in branches if "join" in b] + [b for b in branches if "back" in b]
    for b in order:
        f = by_ev[b["fork"]]
        n = len(b["tiles"])
        side = {"L": 1, "R": -1, "S": 0}[b["side"]]
        if "join" in b:
            j = by_ev[b["join"]]
            s0, s1 = f["s"], j["s"]
            amp = SPEC_AMP.get(b["code"], 17.0)
            pts = []
            for u in np.linspace(0, 1, 120):
                p, tg = curve.at(s0 + (s1 - s0) * u)
                pts.append(p + left_normal(tg) * side * amp * math.sin(math.pi * u) ** 0.45)
            bc = Curve(pts)
            a0 = f["r"] + R_B + (5.0 if side else 1.5)
            a1 = j["r"] + R_B + (5.0 if side else 1.5)
            usable = bc.L - a0 - a1
            pos = [a0 + usable * k / max(n - 1, 1) for k in range(n)]
        else:
            # slepá odbočka: oblouk vlevo z rozcestí; natočení a zakřivení se hledá
            # tak, aby měla co největší odstup od ostatních polí
            p0, tg0 = curve.at(f["s"])
            step = 2 * R_B + 1.4
            pos = [f["r"] + R_B + 2.0 + step * k for k in range(n)]
            OX = np.array([t["x"] for t in tiles if t is not f]); OY = np.array([t["y"] for t in tiles if t is not f])
            best = None
            for off in range(-75, 76, 5):
                for curv in range(-45, 46, 5):
                    ang = math.atan2(tg0[1], tg0[0]) - math.pi / 2 + math.radians(off)
                    pts = [p0.copy()]; q = p0.copy()
                    for k in range(int((pos[-1] + 16) / 0.5)):
                        q = q + np.array([math.cos(ang), math.sin(ang)]) * 0.5
                        ang += math.radians(curv) * 0.5 / PITCH
                        pts.append(q.copy())
                    bc_ = Curve(pts)
                    P = np.array([bc_.at(sp)[0] for sp in pos + [pos[-1] + 9, pos[-1] + 15]])
                    if (P[:, 0] < 10).any() or (P[:, 0] > W - 10).any() or (P[:, 1] < 10).any() or (P[:, 1] > H - 10).any():
                        continue
                    dmin = np.min(np.hypot(P[:, 0:1] - OX[None, :], P[:, 1:2] - OY[None, :]))
                    soft = sum(((P[:, 0] > z[0]) & (P[:, 0] < z[2]) & (P[:, 1] > z[1]) & (P[:, 1] < z[3])).sum() for z in SPUR_AVOID)
                    sc = min(dmin, 30) - abs(off) * 0.03 - abs(curv) * 0.02 - soft * 4
                    if best is None or sc > best[0]:
                        best = (sc, bc_)
            bc = best[1]
        bt = []
        for k, (tdef, sp) in enumerate(zip(b["tiles"], pos)):
            p, tg = bc.at(sp)
            kind = "bgreen" if tdef["ev"] else "bbrown"
            if "back" in b:
                kind = "dead_end" if tdef["ev"] else "dead"
            bt.append(dict(label=tdef["code"], ev=tdef["ev"], x=p[0], y=p[1], tx=tg[0],
                           ty=tg[1], kind=kind, r=R_B, trunk=False, branch=b["code"]))
        tiles.extend(bt)
        branch_out.append(dict(code=b["code"], name=b["name"], fork=b["fork"],
                               join=b.get("join"), back=b.get("back"), side=b["side"],
                               curve=bc.p[::3].tolist(), tiles=[t["label"] for t in bt]))
    return tiles, branch_out, ev_tile, curve


# amplitudy větví (mm) a parametry slepých odboček (natočení°, zakřivení° na rozteč)
SPEC_AMP = {"L": 24, "V": 24, "E": 0, "CZ": 16, "EU": 16, "P": 38, "O": 27}
SPUR_AVOID = [(0, 105, 52, 240), (205, 298, 290, 336)]
SPURS = {"B": (-35, 30), "N": (25, -30), "F": (-30, 25), "S": (20, -25), "Z": (0, 30)}


# ---------------------------------------------------------------- texty
def expand(text, ev_tile):
    def n(m):
        return ev_tile[m.group(1)]

    def r(m):
        code = m.group(1)
        last = {"L": 4, "E": 5, "V": 5, "CZ": 3, "EU": 3, "B": 4, "N": 4, "F": 4,
                "S": 4, "Z": 4, "P": 9, "O": 11}[code]
        return f"{code}1–{code}{last}"
    text = re.sub(r"\{N:([^}]+)\}", n, text)
    text = re.sub(r"\{R:([^}]+)\}", r, text)
    return text


def rich_tokens(text, base="r"):
    """Rozdělí text s **tučným** na slova (slovo, styl, přilepit_k_předchozímu)."""
    out = []
    prev_space = True
    for raw in re.split(r"(\*\*.+?\*\*)", text):
        if not raw:
            continue
        style, part = base, raw
        if raw.startswith("**"):
            part, style = raw[2:-2], "b"
        glue = bool(out) and not prev_space and not part.startswith(" ")
        first = True
        for w in part.split(" "):
            if w:
                out.append((w, style, glue and first))
                first = False
        prev_space = part.endswith(" ")
    return out


def wrap(tokens, width, first_indent=0.0):
    # slepené tokeny (interpunkce za tučným) se zalamují spolu s předchozím slovem
    merged = []
    for tok in tokens:
        w, st = tok[0], tok[1]
        if len(tok) > 2 and tok[2] and merged:
            merged[-1].append((w, st))
        else:
            merged.append([(w, st)])
    lines, cur, x = [], [], first_indent
    sp = tw(" ")
    for runs in merged:
        ww = sum(tw(w, st) for w, st in runs)
        add = ww if not cur else sp + ww
        if cur and x + add > width:
            lines.append(cur)
            cur, x = [runs], ww
        else:
            cur.append(runs)
            x += add
    if cur:
        lines.append(cur)
    return lines


def layout_label(tile, ev_tile, width):
    title, task_kind, task = EV[tile["ev"]]
    badge_w = tw(tile["label"], "b") + 2.2
    inner = width - 2 * PAD
    tl = wrap(rich_tokens(title, "b"), inner, badge_w + 1.0)
    kt = [(task_kind + ":", "i", False)] + rich_tokens(expand(task, ev_tile))
    bl = wrap(kt, inner)
    h = 2 * PAD + LH * (len(tl) + len(bl)) + 0.5
    return dict(w=width, h=h, title=tl, body=bl, badge_w=badge_w)


# ---------------------------------------------------------------- umístění popisků
def seg_rect_hit(p, q, r, pad=0.0):
    """Protíná úsečka p-q obdélník r=(x0,y0,x1,y1)?"""
    x0, y0, x1, y1 = r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad
    for t in np.linspace(0, 1, 24):
        x = p[0] + (q[0] - p[0]) * t
        y = p[1] + (q[1] - p[1]) * t
        if x0 <= x <= x1 and y0 <= y <= y1:
            return True
    return False


def rect_circle(r, cx, cy, rad):
    nx = min(max(cx, r[0]), r[2])
    ny = min(max(cy, r[1]), r[3])
    return (nx - cx) ** 2 + (ny - cy) ** 2 < rad * rad


def rect_rect(a, b, pad=0.0):
    return not (a[2] + pad <= b[0] or b[2] + pad <= a[0] or a[3] + pad <= b[1] or b[3] + pad <= a[1])


def seg_seg(p1, p2, p3, p4):
    def ccw(a, b, c):
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])
    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)


def nearest_on_rect(r, x, y):
    return (min(max(x, r[0]), r[2]), min(max(y, r[1]), r[3]))


def place_labels(tiles, ev_tile, zones, soft_zones=(), widths=(31, 36, 41, 47, 55, 64, 74, 84), priority=()):
    greens = [t for t in tiles if t["ev"]]
    TX = np.array([t["x"] for t in tiles]); TY = np.array([t["y"] for t in tiles])
    TR = np.array([t["r"] for t in tiles])
    TCLR = 1.0 + 1.6
    angs = np.radians(np.arange(0, 360, 6))
    dists = np.array([1.2, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66])
    data = {}
    for t in greens:
        lays = [layout_label(t, ev_tile, w) for w in widths]
        rows = []
        for li, lay in enumerate(lays):
            w, h = lay["w"], lay["h"]
            A, D = np.meshgrid(angs, dists)
            A = A.ravel(); D = D.ravel()
            ux, uy = np.cos(A), np.sin(A)
            ext = np.abs(ux) * w / 2 + np.abs(uy) * h / 2
            cx = t["x"] + ux * (t["r"] + 1.0 + D + ext)
            cy = t["y"] + uy * (t["r"] + 1.0 + D + ext)
            rows.append(np.stack([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2,
                                  np.full_like(cx, li), D], axis=1))
        C = np.vstack(rows)
        x0, y0, x1, y1 = C[:, 0], C[:, 1], C[:, 2], C[:, 3]
        m = (x0 >= 5) & (y0 >= 5) & (x1 <= W - 5) & (y1 <= H - 5)
        m &= ~((x0 < SEAM + 2.5) & (x1 > SEAM - 2.5))
        for z in zones:
            m &= (x1 + 1.0 <= z[0]) | (z[2] + 1.0 <= x0) | (y1 + 1.0 <= z[1]) | (z[3] + 1.0 <= y0)
        C = C[m]
        x0, y0, x1, y1 = C[:, 0:1], C[:, 1:2], C[:, 2:3], C[:, 3:4]
        nx = np.clip(TX[None, :], x0, x1); ny = np.clip(TY[None, :], y0, y1)
        hit = ((nx - TX[None, :]) ** 2 + (ny - TY[None, :]) ** 2) < (TR[None, :] + TCLR) ** 2
        C = C[~hit.any(axis=1)]
        ax = np.clip(t["x"], C[:, 0], C[:, 2]); ay = np.clip(t["y"], C[:, 1], C[:, 3])
        vx, vy = ax - t["x"], ay - t["y"]
        dl = np.hypot(vx, vy) + 1e-9
        sx = t["x"] + vx / dl * t["r"]; sy = t["y"] + vy / dl * t["r"]
        ex, ey = ax - sx, ay - sy
        L2 = ex * ex + ey * ey + 1e-9
        tt = np.clip(((TX[None, :] - sx[:, None]) * ex[:, None] + (TY[None, :] - sy[:, None]) * ey[:, None]) / L2[:, None], 0, 1)
        qx = sx[:, None] + ex[:, None] * tt; qy = sy[:, None] + ey[:, None] * tt
        self_mask = (np.abs(TX - t["x"]) < 1e-6) & (np.abs(TY - t["y"]) < 1e-6)
        lh = (((qx - TX[None, :]) ** 2 + (qy - TY[None, :]) ** 2) < (TR[None, :] + 0.6) ** 2) & ~self_mask[None, :]
        keep = ~lh.any(axis=1)
        C, ax, ay, sx, sy, dl = C[keep], ax[keep], ay[keep], sx[keep], sy[keep], dl[keep]
        area = (C[:, 2] - C[:, 0]) * (C[:, 3] - C[:, 1])
        soft = np.zeros(len(C))
        for z in soft_zones:
            soft += 8 * ~((C[:, 2] <= z[0]) | (z[2] <= C[:, 0]) | (C[:, 3] <= z[1]) | (z[3] <= C[:, 1]))
        score = dl + area * 0.004 + soft + np.where(C[:, 5] <= 3, 0, 2)
        order = np.argsort(score)
        data[t["label"]] = dict(t=t, lays=lays, C=C[order], seg=np.stack([sx, sy, ax, ay], 1)[order],
                                alive=np.ones(len(order), bool))
    placed = {}
    remaining = set(data)
    ts = np.linspace(0, 1, 16)

    def kill(d, r, seg):
        C, S = d["C"], d["seg"]
        pad = 1.2
        ov = ~((C[:, 2] + pad <= r[0]) | (r[2] + pad <= C[:, 0]) | (C[:, 3] + pad <= r[1]) | (r[3] + pad <= C[:, 1]))
        px = S[:, 0:1] + (S[:, 2:3] - S[:, 0:1]) * ts; py = S[:, 1:2] + (S[:, 3:4] - S[:, 1:2]) * ts
        l1 = ((px >= r[0] - .4) & (px <= r[2] + .4) & (py >= r[1] - .4) & (py <= r[3] + .4)).any(axis=1)
        qx = seg[0] + (seg[2] - seg[0]) * ts; qy = seg[1] + (seg[3] - seg[1]) * ts
        l2 = ((qx[None, :] >= C[:, 0:1] - .4) & (qx[None, :] <= C[:, 2:3] + .4) & (qy[None, :] >= C[:, 1:2] - .4) & (qy[None, :] <= C[:, 3:4] + .4)).any(axis=1)

        def ccw(ax_, ay_, bx, by, cx, cy):
            return (cy - ay_) * (bx - ax_) > (by - ay_) * (cx - ax_)
        p1x, p1y, p2x, p2y = S[:, 0], S[:, 1], S[:, 2], S[:, 3]
        p3x, p3y, p4x, p4y = seg
        cr = (ccw(p1x, p1y, p3x, p3y, p4x, p4y) != ccw(p2x, p2y, p3x, p3y, p4x, p4y)) & \
             (ccw(p1x, p1y, p2x, p2y, p3x, p3y) != ccw(p1x, p1y, p2x, p2y, p4x, p4y))
        d["alive"] &= ~(ov | l1 | l2 | cr)

    while remaining:
        pr = [k for k in priority if k in remaining]
        lab = pr[0] if pr else min(remaining, key=lambda k: int(data[k]["alive"].sum()))
        d = data[lab]
        remaining.discard(lab)
        idx = np.flatnonzero(d["alive"])
        if len(idx) == 0:
            print("NELZE UMÍSTIT popisek", lab, EV[d["t"]["ev"]][0])
            placed[lab] = None
            continue
        i = idx[0]
        r = tuple(d["C"][i, :4]); seg = d["seg"][i]
        lay = d["lays"][int(d["C"][i, 4])]
        placed[lab] = dict(rect=r, lay=lay, start=(seg[0], seg[1]), a=(seg[2], seg[3]))
        for k in remaining:
            kill(data[k], r, seg)
    return placed
