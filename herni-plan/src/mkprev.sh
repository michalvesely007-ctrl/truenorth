#!/bin/bash
# vloží board.svg přímo do HTML (aby se načetl podklad i písma) a vyrenderuje náhled
cd "$(dirname "$0")"
python3 - <<'PY'
s=open('board.svg',encoding='utf-8').read()
h=open('prev.html',encoding='utf-8').read().replace('<!--SVG-->',s)
open('prev_inline.html','w',encoding='utf-8').write(h)
PY
P=/tmp/claude-0/-home-user-truenorth/155948e4-cd73-5832-8f65-9a8a5a3ced04/scratchpad
timeout 120 node shot.js prev_inline.html $P/prev.png 554 392 && python3 -c "
from PIL import Image; im=Image.open('$P/prev.png'); im.resize((1800,int(1800*im.size[1]/im.size[0]))).save('$P/prev_s.png')"
