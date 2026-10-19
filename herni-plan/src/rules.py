# -*- coding: utf-8 -*-
"""Pravidla hry (A4) – čísla polí se berou z aktuálního rozložení."""
import json
from numbering import build
_, _, T = build()
n = lambda e: T[e]
html = f"""<!doctype html><html lang="cs"><head><meta charset="utf-8"><style>
@page{{size:A4;margin:10mm 12mm}}
@font-face{{font-family:'Carlito';src:url('file:///usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf');}}
@font-face{{font-family:'Carlito';font-weight:bold;src:url('file:///usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf');}}
@font-face{{font-family:'Carlito';font-style:italic;src:url('file:///usr/share/fonts/truetype/crosextra/Carlito-Italic.ttf');}}
body{{font-family:Carlito,sans-serif;font-size:9.5pt;line-height:1.26;color:#3a2716;margin:0}}
h1{{font-size:21pt;font-style:italic;margin:0 0 1mm}} .sub{{font-style:italic;font-size:12pt;margin-bottom:2mm}}
h2{{font-size:12.5pt;margin:2.6mm 0 1mm;border-bottom:0.3mm solid #3a2716}}
ul,ol{{margin:0.5mm 0 1mm 5mm;padding-left:3mm}} li{{margin:0.4mm 0}}
table{{border-collapse:collapse;width:100%;font-size:8.8pt;margin-top:1mm}}
th,td{{border:0.25mm solid #8a7356;padding:1mm 1.4mm;vertical-align:top;text-align:left}} th{{background:#efe3c8}}
.cols{{column-count:2;column-gap:7mm}} .box{{background:#f6eedc;border:0.3mm solid #3a2716;border-radius:2mm;padding:2mm 3mm;margin:2mm 0}}
.leg span{{display:inline-block;width:4mm;height:4mm;border-radius:50%;border:0.35mm solid #3a2716;vertical-align:-0.8mm;margin-right:1.5mm}}
</style></head><body>
<h1>Cesta šťastným životem</h1>
<div class="sub">150 herních polí · 150 let šťastného života · pravidla hry</div>
<div class="cols">
<h2>Potřebuješ</h2>
<ul><li>herní plán (A2, nebo slepené 2× A3), 1 kostku, figurku pro každého hráče, 2–6 hráčů</li></ul>
<h2>Cíl hry</h2>
<p>Dojít ze STARTU do cíle <b>Šťastný život? (pole {n('60')})</b>. Kdo tam dorazí první, vyhrává – i když se teprve časem ukáže, která cesta tam skutečně vede.</p>
<h2>Průběh tahu</h2>
<ol>
<li>Hoď kostkou a posuň figurku o tolik polí dopředu.</li>
<li><b>Hnědé pole</b> – nic se neděje.</li>
<li><b>Zelené pole</b> – přečti nahlas popisek u pole se stejným číslem, splň úkol a proveď účinek (posun, návrat, stání).</li>
<li>Pole, na které tě účinek posune, se už znovu neplní – úkol plníš jen na poli, kde skončil tvůj hod.</li>
<li>Když úkol nejde udělat, splníš jen uvedený pohybový pokyn.</li>
</ol>
<h2>Odpovědi a otázky</h2>
<ul><li><b>„Odpovím“</b> – odpovídáš jednou větou nebo ANO/NE; účinek obou odpovědí je napsaný u pole.</li>
<li><b>„Ostatní hádají“</b> – ostatní tipují tvou odpověď; u pole je napsáno, co se stane při správném a špatném tipu.</li></ul>
<h2>Rozcestí</h2>
<ul><li>Na rozcestí (zelené pole s tečkovaným kruhem a symbolem ⑂) se <b>vždy zastav</b>, i když ti hod vychází dál. Platí to i pro posun z úkolu.</li>
<li>Hoď kostkou: <b>lichá (1·3·5) = VLEVO</b>, <b>sudá (2·4·6) = VPRAVO</b> – vlevo a vpravo z pohledu hráče, který jde po cestě. Směr ukazují štítky u začátku větví.</li>
<li>Výjimky jsou napsané přímo u pole: pole {n('3')} (1–2 les / 3–4 ESF / 5–6 environmentalistika) a pole {n('21')} (rozhoduje odpověď ANO/NE na otázku o eurovém obědě).</li>
<li>Při dalším tahu pokračuješ zvolenou větví.</li></ul>
<h2>Slepé cesty</h2>
<ul><li>Šrafovaná pole vedou na slepou cestu. Na posledním zeleném poli (za ním je závora) se zastavíš, i když ti hod vychází dál, a splníš úkol.</li>
<li>Pak se vrátíš na rozcestí uvedené na štítku <i>„SLEPÁ ↩ zpět na …“</i>. Při dalším tahu pokračuješ hlavní cestou dál – na rozcestí už znovu nevybíráš.</li></ul>
<h2>Návraty, stání a házení znovu</h2>
<ul><li><b>Vrátím se o X</b> – couvej po cestě, kterou jsi přišel/přišla (i do větve, ze které jsi vyšel/vyšla). Nikdy ne před START a nikdy do slepé cesty.</li>
<li><b>Stojím / zůstávám jedno (dvě) kola</b> – vynecháš tolik svých tahů.</li>
<li><b>Ladakh (pole {n('LA')})</b>: padne-li 6, posuneš se o 6 a házíš znovu.</li></ul>
<h2>Cíl</h2>
<p>Do cíle musíš hodit <b>přesný počet</b>. Když přehodíš, zůstaneš stát a čekáš na další tah.</p>
</div>
<h2>Přehled rozcestí</h2>
<table><tr><th>Pole</th><th>Volba</th><th>Vlevo</th><th>Vpravo / rovně</th><th>Kde se cesty spojí / návrat</th></tr>
<tr><td>{n('3')}</td><td>1–2 / 3–4 / 5–6</td><td>5–6 environmentalistika: V1–V5</td><td>3–4 ESF rovně: E1–E5 · 1–2 lesník vpravo: L1–L4</td><td>všechny tři na poli {n('7')}</td></tr>
<tr><td>{n('22')}</td><td>lichá / sudá</td><td>Nový Zéland – slepá cesta N1–N4</td><td>domů, pole {n('8')}</td><td>z N4 zpět na {n('22')}</td></tr>
<tr><td>{n('17')}</td><td>lichá / sudá</td><td>české stromy CZ1–CZ3</td><td>Evropa EU1–EU3</td><td>obě na poli {n('20')}</td></tr>
<tr><td>{n('21')}</td><td>ANO / NE</td><td>ANO: Brusel – slepá cesta B1–B4</td><td>NE: pole {n('30')}</td><td>z B4 zpět na {n('21')}</td></tr>
<tr><td>{n('33')}</td><td>lichá / sudá</td><td>další firma – slepá cesta F1–F4</td><td>pole {n('34')}</td><td>z F4 zpět na {n('33')}</td></tr>
<tr><td>{n('37')}</td><td>lichá / sudá</td><td>sociální podnik – slepá cesta S1–S4</td><td>JIC, pole {n('38')}</td><td>z S4 zpět na {n('37')}</td></tr>
<tr><td>{n('54')}</td><td>lichá / sudá</td><td>zahraničí – slepá cesta Z1–Z4</td><td>česká cesta, pole {n('25')}</td><td>z Z4 zpět na {n('54')}</td></tr>
<tr><td>{n('58')}</td><td>lichá / sudá</td><td>Podnikání s přesahem P1–P9 (P1 + 8 hnědých)</td><td>OwnerCompass O1–O11 (O1 + 10 hnědých)</td><td>obě do cíle {n('60')}</td></tr>
</table>
<div class="box leg"><b>Legenda:</b>&nbsp;
<span style="background:#e6cfa2"></span>hnědé pole &nbsp;
<span style="background:#2e7a43"></span>zelené akční pole (dvojitý kruh) &nbsp;
<span style="background:#2e7a43;outline:0.4mm dotted #3a2716;outline-offset:0.5mm"></span>rozcestí &nbsp;
<span style="background:repeating-linear-gradient(45deg,#cdb48c 0 0.6mm,#3a2716 0.6mm 0.9mm)"></span>slepá cesta (šrafy) &nbsp;
<span style="background:#e8b443"></span>cíl
<br>Plán je čitelný i černobíle: typ pole rozlišuje také kruh, šrafy, symbol ⑂ a závora na konci slepé cesty.</div>
<h2>Tisk na 2× A3</h2>
<ol><li>Vytiskni soubor <i>Cesta_stastnym_zivotem_2xA3.pdf</i> na A3 na výšku ve <b>skutečné velikosti 100 %</b>. Proužek dole musí měřit přesně 50 mm.</li>
<li>Na listu 2 odstřihni levý bílý okraj přesně po přerušované čáře (✂).</li>
<li>List 1 natři lepidlem na šrafovaném pruhu a přilož list 2 tak, aby se jeho hrana kryla s čárou spoje a křížky nahoře i dole.</li></ol>
</body></html>"""
open("rules.html", "w", encoding="utf-8").write(html)
