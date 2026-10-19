# -*- coding: utf-8 -*-
"""Kontrolní seznam polí (markdown) z aktuálního layout.json."""
import json
from content import EV
d = json.load(open("layout.json", encoding="utf-8"))
T = d["ev_tile"]
rows = ["| Pole na plánu | Událost (id ze zadání) | Text pole |", "|---|---|---|"]
rows += [f"| {t['label']} | {t['ev']} | {EV[t['ev']][0]} |" for t in d["tiles"] if t["ev"]]
md = f"""# Cesta šťastným životem – kontrolní seznam

Vygenerováno skriptem `src/checklist.py`; výstup automatických kontrol je v `kontrola_vystup.txt`.

* Očíslovaná pole hlavní trasy: **150** (1–150, souvisle)
* Zelená pole: **69** (55 na hlavní trase + 14 ve větvích) = 68 polí ze zadání + Ladakh
* Závěrečné větve: P1 + **8** hnědých, O1 + **10** hnědých, obě do cíle 150
* Překryvy políček, popisků a vodicích čar: **0**; popisky se vyhýbají hlavám postav v podkladu (kde to jde) a nepřechází přes spoj listů A3
* Písmo popisků 8 pt při tisku 2× A3 (100 %), na A2 8,6 pt

## Časová posloupnost cest
Nový Zéland po přijímacím pohovoru do Nadace Partnerství (pole {T['22']}) → Madagaskar při narození syna ({T['23']}) → Annapurna před třemi lety ({T['26']}) → Kanada a Aljaška v rámci sabatiklu ({T['25']}) → Ladakh letos, šestitisícovka ({T['LA']})

Zápisky za čokoládu ({T['8']}) a „Dívka si myslí, že ji balím“ ({T['9']}) jsou dvě zelená pole hned za sebou.

## Mapa polí
""" + "\n".join(rows) + "\n"
open("../tisk/kontrolni_seznam.md", "w", encoding="utf-8").write(md)
