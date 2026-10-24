# -*- coding: utf-8 -*-
"""Sestaví HTML pro tisk: A2 (1 list) a 2× A3 na výšku s lepicím pruhem."""
import build as B
svg = open("board.svg", encoding="utf-8").read()
inner = svg[svg.index(">", svg.index("<svg")) + 1: svg.rindex("</svg>")]
W, H, S = B.W, B.H, B.SEAM
OV = 8.0  # lepicí přesah na listu 1
INK = "#3a2716"

def board_svg(x0, w, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{H}mm" viewBox="{x0} 0 {w} {H}">'
            f'{inner}{extra}</svg>')

head = """<!doctype html><html><head><meta charset="utf-8"><style>
@page{margin:0} html,body{margin:0;padding:0}
.page{position:relative;overflow:hidden;page-break-after:always;background:#fff}
.page:last-child{page-break-after:auto}
.abs{position:absolute} svg{display:block}
.t{font-family:Carlito,sans-serif;color:%s;font-size:9pt;position:absolute;white-space:nowrap}
</style><style>@font-face{font-family:'Carlito';src:url('file:///usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf');}
@font-face{font-family:'Carlito';font-weight:bold;src:url('file:///usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf');}</style></head><body>""" % INK

# ---------- A2: deska roztažená na celý formát A2 na šířku
k = 594 / W
a2 = head + (f'<div class="page" style="width:594mm;height:420mm">'
             f'<div class="abs" style="left:0;top:{(420 - H * k) / 2}mm">'
             f'<svg xmlns="http://www.w3.org/2000/svg" width="594mm" height="{H * k}mm" viewBox="0 0 {W} {H}">{inner}</svg></div></div>')
open("print_a2.html", "w", encoding="utf-8").write(a2 + "</body></html>")

# ---------- 2× A3 na výšku
def marks(x, label, cut):
    """Čára spoje a registrační křížky v horním a dolním okraji (souřadnice listu v mm)."""
    o = []
    for y0, y1, cy in ((0, 13.2, 8.5), (406.8, 420, 411.5)):
        o.append(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke="#000" stroke-width="0.25" stroke-dasharray="{"1.2 0.8" if cut else "2.5 1"}"/>')
        o.append(f'<circle cx="{x}" cy="{cy}" r="2.2" fill="none" stroke="#000" stroke-width="0.2"/>')
        o.append(f'<line x1="{x - 3.4}" y1="{cy}" x2="{x + 3.4}" y2="{cy}" stroke="#000" stroke-width="0.2"/>')
    return "".join(o)

def corners():
    """Stejné rohové značky na obou listech: obsah obou stránek má pak shodný rozměr,
    takže případné „přizpůsobení stránce“ v tiskárně změní oba listy stejně."""
    o = []
    for x, dx in ((3, 1), (294, -1)):
        for y, dy in ((3, 1), (417, -1)):
            o.append(f'<path d="M{x},{y + 6 * dy}V{y}H{x + 6 * dx}" fill="none" stroke="#000" stroke-width="0.25"/>')
    return "".join(o)


def scale_bar(x, y):
    o = [f'<rect x="{x}" y="{y}" width="50" height="2" fill="none" stroke="#000" stroke-width="0.2"/>']
    for i in range(0, 50, 10):
        o.append(f'<rect x="{x + i}" y="{y}" width="5" height="2" fill="#000"/>')
    o.append(f'<text x="{x + 52}" y="{y + 1.8}" font-family="Carlito" font-size="2.6" fill="#000">kontrola měřítka: tento proužek musí mít přesně 50 mm</text>')
    return "".join(o)

L1, L2, TOP = 6.0, 14.0, 14.0
# list 1 – levá polovina + 8 mm lepicí pruh za čarou spoje
glue = (f'<rect x="{S}" y="0" width="{OV}" height="{H}" fill="url(#gl)" />'
        f'<defs><pattern id="gl" width="3" height="3" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
        f'<rect width="3" height="3" fill="#fff" fill-opacity="0.35"/><line x1="0" y1="0" x2="0" y2="3" stroke="#000" stroke-opacity="0.35" stroke-width="0.6"/></pattern></defs>'
        + "".join(f'<text transform="translate({S + OV / 2 + 1},{y}) rotate(90)" font-family="Carlito" font-weight="bold" font-size="3" text-anchor="middle" fill="#000">LEPIDLO · sem přilož list 2</text>' for y in (60, 196, 332)))
p1 = (f'<div class="page" style="width:297mm;height:420mm">'
      f'<div class="abs" style="left:{L1}mm;top:{TOP}mm;width:{S + OV}mm;height:{H}mm;overflow:hidden">{board_svg(0, S + OV, glue)}</div>'
      f'<svg class="abs" style="left:0;top:0" width="297mm" height="420mm" viewBox="0 0 297 420">'
      f'{marks(L1 + S, "A", False)}'
      f'<text x="{L1}" y="6" font-family="Carlito" font-weight="bold" font-size="4" fill="#000">LIST 1 ze 2 – LEVÁ polovina · Cesta šťastným životem</text>'
      f'<text x="{L1}" y="11" font-family="Carlito" font-size="2.9" fill="#000">Tiskni oba listy najednou, A3 na výšku, SKUTEČNÁ VELIKOST 100 % (vypni „přizpůsobit“). Proužek dole = 50 mm. Šrafovaný pruh je lepicí.</text>'
      f'{corners()}{scale_bar(L1, 410)}'
      f'<text x="{L1 + S - 2}" y="418" font-family="Carlito" font-size="2.6" text-anchor="end" fill="#000">čára spoje ▸ zde začíná list 2</text>'
      f'</svg></div>')
# list 2 – pravá polovina; levý bílý okraj se odstřihne přesně po čáře spoje
p2 = (f'<div class="page" style="width:297mm;height:420mm">'
      f'<div class="abs" style="left:{L2}mm;top:{TOP}mm;width:{W - S}mm;height:{H}mm;overflow:hidden">{board_svg(S, W - S)}</div>'
      f'<svg class="abs" style="left:0;top:0" width="297mm" height="420mm" viewBox="0 0 297 420">'
      f'{marks(L2, "A", True)}'
      f'<text x="{L2 + 3}" y="6" font-family="Carlito" font-weight="bold" font-size="4" fill="#000">LIST 2 ze 2 – PRAVÁ polovina</text>'
      f'<text x="{L2 + 3}" y="11" font-family="Carlito" font-size="2.9" fill="#000">✂ Odstřihni levý bílý okraj přesně po přerušované čáře. Pak list přilož na lepicí pruh listu 1 tak, aby se kryly křížky nahoře i dole.</text>'
      f'<text x="{L2 - 2}" y="9" font-family="Carlito" font-size="5" text-anchor="end" fill="#000">✂</text>'
      f'<text x="{L2 - 2}" y="414" font-family="Carlito" font-size="5" text-anchor="end" fill="#000">✂</text>'
      f'{corners()}{scale_bar(L2 + 3, 410)}'
      f'</svg></div>')
open("print_2xA3.html", "w", encoding="utf-8").write(head + p1 + p2 + "</body></html>")
print("ok")
