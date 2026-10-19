# -*- coding: utf-8 -*-
"""Přiřadí čísla polí hlavní trasy a kódy políček větví."""
from content import TRUNK, BRANCHES, EV, FORKS

def build():
    trunk = []          # list of dict(num, ev or None)
    ev_tile = {}        # event id -> tile label
    n = 0
    for ev, browns in TRUNK:
        n += 1
        trunk.append(dict(num=n, ev=ev))
        ev_tile[ev] = str(n)
        for _ in range(browns or 0):
            n += 1
            trunk.append(dict(num=n, ev=None))
    branches = []
    for b in BRANCHES:
        tiles = []
        for i, ev in enumerate(b["tiles"], 1):
            code = f'{b["code"]}{i}'
            tiles.append(dict(code=code, ev=ev))
            if ev:
                ev_tile[ev] = code
        branches.append(dict(b, tiles=tiles))
    return trunk, branches, ev_tile

if __name__ == "__main__":
    trunk, branches, ev_tile = build()
    greens = [t for t in trunk if t["ev"]] + [t for b in branches for t in b["tiles"] if t["ev"]]
    print("trunk tiles:", len(trunk), "trunk greens:", sum(1 for t in trunk if t['ev']))
    print("branch tiles:", sum(len(b['tiles']) for b in branches))
    print("green total:", len(greens), "events defined:", len(EV))
    assert set(EV) == {t['ev'] for t in greens}
    print(ev_tile)
