# -*- coding: utf-8 -*-
"""Úprava podkladu: horolezci ve výbavě podle fotky (Michal a Katka), zvětšení na 150 dpi."""
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
from scipy import ndimage

im = Image.open("podklad_original.png").convert("RGB")
a = np.asarray(im).astype(np.float32) / 255.0
hsv = np.asarray(im.convert("HSV")).astype(np.float32)
H, S, V = hsv[..., 0] * 360 / 255, hsv[..., 1] / 255, hsv[..., 2] / 255
yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]


def box(x0, y0, x1, y1):
    return (xx >= x0) & (xx < x1) & (yy >= y0) & (yy < y1)


def big_parts(mask, min_px=12):
    """Všechny větší souvislé části masky (pro trička rozdělená popruhy)."""
    lab, n = ndimage.label(mask)
    keep = np.zeros_like(mask)
    for i in range(1, n + 1):
        part = lab == i
        if part.sum() >= min_px:
            keep |= part
    return ndimage.binary_fill_holes(ndimage.binary_closing(keep, iterations=1))


def main_part(mask, close=1):
    """Ponechá největší souvislou oblast masky (odstraní tečky v pozadí) a vyplní díry."""
    lab, n = ndimage.label(mask)
    if n == 0:
        return mask
    sizes = ndimage.sum(mask, lab, range(1, n + 1))
    m = lab == (int(np.argmax(sizes)) + 1)
    m = ndimage.binary_closing(m, iterations=close)
    return ndimage.binary_fill_holes(m)


def recolor(mask, rgb, keep_shading=True):
    """Přebarví masku na cílovou barvu se zachováním světla a stínů."""
    tgt = np.array(rgb, np.float32) / 255.0
    lum = a[..., 0] * 0.3 + a[..., 1] * 0.59 + a[..., 2] * 0.11
    ref = np.median(lum[mask]) if mask.any() else 0.5
    k = np.clip(lum / max(ref, 1e-3), 0.35, 1.6)[..., None]
    out = np.clip(tgt[None, None, :] * k, 0, 1)
    a[mask] = out[mask]


# --- Michal (horní lezec): modrá helma, světle modré tričko, brýle s červenými skly
helmet = main_part(box(30, 287, 61, 308) & (S < 0.28) & (V > 0.55))
recolor(helmet, (40, 78, 196))
shirt = main_part(box(14, 318, 58, 374) & (((H < 28) | (H > 340)) & (S > 0.4) & (V > 0.3)))
recolor(shirt, (128, 166, 214))

# --- Katka (dolní lezkyně): šedá helma se žlutým okrajem, tyrkysové tričko
helmet2 = main_part(box(74, 463, 104, 484) & (H > 185) & (H < 235) & (S > 0.35))
recolor(helmet2, (122, 126, 132))
shirt2 = big_parts(box(58, 490, 102, 534) & (H > 262) & (H < 345) & (S > 0.15) & (V > 0.15))
recolor(shirt2, (52, 196, 220))

img = Image.fromarray((a * 255).astype(np.uint8))
d = ImageDraw.Draw(img)
# žlutý okraj helmy Katky – spodní hrana hlavní části helmy, vyhlazená
cols = [x for x in range(74, 104) if helmet2[:, x].sum() >= 4]
if cols:
    pts = [(x, int(np.max(np.where(helmet2[:, x])[0]))) for x in cols]
    ys = np.convolve([p[1] for p in pts], np.ones(3) / 3, mode="same")
    ys[0], ys[-1] = pts[0][1], pts[-1][1]
    d.line([(x, float(y)) for (x, _), y in zip(pts, ys)], fill=(232, 176, 40), width=2)
# sportovní brýle Michala: kreslené ve 4× rozlišení kvůli hladkým hranám
X0, Y0, K = 32, 302, 4
patch = img.crop((X0, Y0, X0 + 24, Y0 + 12)).resize((24 * K, 12 * K), Image.LANCZOS)
pd = ImageDraw.Draw(patch)
def R(x0, y0, x1, y1):
    return ((x0 - X0) * K, (y0 - Y0) * K, (x1 - X0) * K, (y1 - Y0) * K)
pd.rounded_rectangle(R(36, 305, 43.6, 310.4), radius=7, fill=(25, 22, 22))
pd.rounded_rectangle(R(44.4, 305, 51.8, 310.4), radius=7, fill=(25, 22, 22))
pd.line([R(43.4, 306.2, 44.6, 306.2)[:2], R(43.4, 306.2, 44.6, 306.2)[2:]], fill=(25, 22, 22), width=4)
pd.line([R(33.8, 306.6, 36.2, 306.2)[:2], R(33.8, 306.6, 36.2, 306.2)[2:]], fill=(25, 22, 22), width=3)
pd.rounded_rectangle(R(36.8, 305.8, 42.9, 309.6), radius=5, fill=(222, 64, 52))
pd.rounded_rectangle(R(45.1, 305.8, 51.0, 309.6), radius=5, fill=(222, 64, 52))
pd.line([R(37.6, 306.5, 40.2, 306.5)[:2], R(37.6, 306.5, 40.2, 306.5)[2:]], fill=(255, 170, 120), width=2)
pd.line([R(45.9, 306.5, 48.4, 306.5)[:2], R(45.9, 306.5, 48.4, 306.5)[2:]], fill=(255, 170, 120), width=2)
img.paste(patch.resize((24, 12), Image.LANCZOS), (X0, Y0))
img.save("podklad_upraveny.png")

W = round(554 / 25.4 * 150); Hh = round(392 / 25.4 * 150)
big = img.resize((W, Hh), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
wash = Image.blend(big, Image.new("RGB", big.size, (246, 236, 210)), 0.22)
ImageEnhance.Color(wash).enhance(0.92).save("podklad_150dpi.jpg", quality=88)
print("ok", int(helmet.sum()), int(shirt.sum()), int(helmet2.sum()), int(shirt2.sum()))
