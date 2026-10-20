# -*- coding: utf-8 -*-
"""Kontroly před tiskem – čte layout.json a content.py."""
import json, math, re, itertools
from content import EV, TRUNK, BRANCHES, FORKS
import build as B

d = json.load(open("layout.json", encoding="utf-8"))
tiles, labels = d["tiles"], d["labels"]
err = []
trunk = [t for t in tiles if t["trunk"]]
greens = [t for t in tiles if t["ev"]]
print("Očíslovaná pole hlavní trasy:", len(trunk), "(1 až", max(int(t["label"]) for t in trunk), ")")
print("Zelená pole celkem:", len(greens), "| na hlavní trase:", sum(1 for t in trunk if t["ev"]),
      "| ve větvích:", sum(1 for t in tiles if t["ev"] and not t["trunk"]))
if len(trunk) != 150: err.append("hlavní trasa nemá 150 polí")
if len(greens) != 69: err.append("zelených polí není 69")
if sorted(int(t["label"]) for t in trunk) != list(range(1, 151)): err.append("číslování 1–150 není souvislé")
# překryv políček
for a, b in itertools.combinations(tiles, 2):
    if math.hypot(a["x"] - b["x"], a["y"] - b["y"]) < a["r"] + b["r"] - 0.05:
        err.append(f"překryv políček {a['label']} × {b['label']}")
# popisky
rects = {k: v["rect"] for k, v in labels.items() if v}
missing = [k for k, v in labels.items() if not v]
if missing: err.append(f"neumístěné popisky {missing}")
for (ka, a), (kb, b) in itertools.combinations(rects.items(), 2):
    if not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1]):
        err.append(f"překryv popisků {ka} × {kb}")
for k, r in rects.items():
    for t in tiles:
        nx = min(max(t["x"], r[0]), r[2]); ny = min(max(t["y"], r[1]), r[3])
        if math.hypot(nx - t["x"], ny - t["y"]) < t["r"] + 1.0:
            err.append(f"popisek {k} zasahuje do pole {t['label']}")
    if r[0] < 5 or r[1] < 5 or r[2] > B.W - 5 or r[3] > B.H - 5: err.append(f"popisek {k} u okraje")
    if r[0] < B.SEAM < r[2]: err.append(f"popisek {k} přes spoj A3")
    for z in d["zones"]:
        if not (r[2] <= z[0] or z[2] <= r[0] or r[3] <= z[1] or z[3] <= r[1]):
            err.append(f"popisek {k} v pevné zóně {z}")
for k_, v in labels.items():
    if not v:
        continue
    t = next(t for t in tiles if t["label"] == k_)
    ln = math.hypot(v["a"][0] - v["start"][0], v["a"][1] - v["start"][1])
    if ln < 2.5:
        err.append(f"vodicí čára k poli {k_} je moc krátká ({ln:.1f} mm)")
    if abs(math.hypot(v["start"][0] - t["x"], v["start"][1] - t["y"]) - t["r"]) > 0.05:
        err.append(f"vodicí čára popisku {k_} nezačíná na svém poli")
lens_ = [math.hypot(v["a"][0] - v["start"][0], v["a"][1] - v["start"][1]) for v in labels.values() if v]
print(f"Vodicí čáry: {len(lens_)} (každý popisek má svou), délka {min(lens_):.1f}–{max(lens_):.1f} mm")
lines = [v["lines"] for v in labels.values() if v]
print(f"Popisky: {len(rects)} umístěno, řádků {min(lines)}–{max(lines)}, písmo 8 pt (={B.FS:.2f} mm)")
# větve
for b in d["branches"]:
    n = len(b["tiles"])
    kind = "slepá → zpět na " + str(d["ev_tile"][b["back"]]) if b["back"] else "spojení na " + d["ev_tile"][b["join"]]
    print(f"  větev {b['code']:>2} z pole {d['ev_tile'][b['fork']]:>3} ({'vlevo' if b['side']=='L' else 'vpravo' if b['side']=='R' else 'rovně'}): {n} polí, {kind}")
P = next(b for b in d["branches"] if b["code"] == "P"); O = next(b for b in d["branches"] if b["code"] == "O")
browns_p = sum(1 for l in P["tiles"] if not next(t for t in tiles if t["label"] == l)["ev"])
browns_o = sum(1 for l in O["tiles"] if not next(t for t in tiles if t["label"] == l)["ev"])
print("Závěr: za 59P hnědých", browns_p, "| za 59O hnědých", browns_o)
if (browns_p, browns_o) != (8, 10): err.append("závěrečné větve nemají 8/10 hnědých")
# strana větví: vlevo = kladný směr levé normály
for b in d["branches"]:
    f = next(t for t in tiles if t["label"] == d["ev_tile"][b["fork"]])
    t1 = next(t for t in tiles if t["label"] == b["tiles"][min(1, len(b['tiles'])-1)])
    ln = (f["ty"], -f["tx"])
    side = (t1["x"] - f["x"]) * ln[0] + (t1["y"] - f["y"]) * ln[1]
    if b["side"] == "L" and side <= 0: err.append(f"větev {b['code']} není vlevo")
    if b["side"] == "R" and side >= 0: err.append(f"větev {b['code']} není vpravo")
# ANO/NE a hádací otázky
for k, (title, kind, task) in EV.items():
    txt = title + " " + task
    if "ANO" in task or "hádají" in task:
        ok = ("ANO:" in task and "NE:" in task) or ("Správná odpověď" in task and "Špatná odpověď" in task)
        print(f"  otázka {k:>3}: {'OK' if ok else 'CHYBÍ ÚČINEK'}")
        if not ok: err.append(f"otázka {k} bez obou účinků")
    for m in re.findall(r"\{N:([^}]+)\}", task):
        if m not in d["ev_tile"]: err.append(f"odkaz na neexistující pole {m}")
eff = {}
for k, (_, _, task) in EV.items():
    for m in re.findall(r"(Posunu se o \d|posunu se o \d|Vrátím se o \d|vrátím se o \d|Stojím (?:jedno|dvě) kol[oa]|Zůstávám tu jedno kolo|přesný počet|házím znovu|o tolik se posunu)", task):
        eff.setdefault(m.lower(), []).append(d["ev_tile"][k])
print("Herní účinky:")
for k, v in sorted(eff.items()):
    print(f"  {k}: pole {', '.join(v)}")
print("\nCHYBY:" if err else "\nVŠECHNY KONTROLY PROŠLY", *err[:40], sep="\n  ")
