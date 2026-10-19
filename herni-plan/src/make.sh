#!/bin/bash
# Přegeneruje celý herní plán. PYTHONHASHSEED fixuje pořadí při rozmisťování popisků.
set -e
cd "$(dirname "$0")"
export PYTHONHASHSEED=1
python3 prep_bg.py
python3 render.py
python3 check.py | tee ../tisk/kontrola_vystup.txt
python3 pages.py
node shot.js print_a2.html ../tisk/Cesta_stastnym_zivotem_A2.pdf 594 420
node shot.js print_2xA3.html ../tisk/Cesta_stastnym_zivotem_2xA3.pdf 297 420
python3 rules.py
node pdf_a4.js rules.html ../tisk/Cesta_stastnym_zivotem_pravidla_A4.pdf
pdftoppm -r 60 -jpeg -jpegopt quality=85 ../tisk/Cesta_stastnym_zivotem_A2.pdf ../tisk/nahled
mv ../tisk/nahled-1.jpg ../tisk/Cesta_stastnym_zivotem_nahled.jpg
python3 checklist.py
