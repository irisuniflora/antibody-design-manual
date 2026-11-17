# -*- coding: utf-8 -*-
"""
PPT에서 추출한 원본 스크린샷에 빨간 박스 + 번호 배지를 입혀 images/ 에 저장.
좌표는 0~1 비율이므로 원본 해상도가 바뀌어도 동작한다.
재실행: python annotate.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "src")      # 원본 스크린샷
DST  = os.path.join(HERE, "images")   # 주석 입힌 결과
RED  = (224, 49, 49)

# out_name: (src_file, [(x0,y0,x1,y1), ...])   좌표는 비율
JOBS = {
 "01-lab": ("s01_1.png", [
     (.012,.138,.128,.170),
     (.149,.195,.246,.225),
     (.651,.187,.986,.365)]),
 "02-search-rfantibody": ("s02_1.png", [
     (.322,.077,.673,.129),
     (.324,.143,.498,.198)]),
 "03-rfab-framework": ("s03_1.png", [
     (.200,.193,.395,.227),
     (.200,.274,.395,.308),
     (.199,.355,.555,.391),
     (.199,.563,.555,.598),
     (.915,.940,.964,.975)]),
 "04-rfab-target": ("s04_1.png", [
     (.199,.215,.551,.263),
     (.197,.352,.232,.384),
     (.199,.488,.551,.689),
     (.199,.731,.551,.762)]),
 "05-rfab-params": ("s05_1.png", [
     (.289,.293,.371,.349),
     (.374,.293,.457,.349),
     (.460,.293,.543,.349),
     (.460,.387,.543,.444),
     (.912,.940,.963,.975)]),
 "06-result-list": ("s06_1.png", [
     (.550,.318,.583,.865),
     (.600,.383,.960,.417),
     (.600,.432,.960,.765)]),
 "07-conf-distribution": ("s07_1.png", [
     (.059,.229,.122,.253),
     (.057,.255,.361,.395),
     (.057,.464,.361,.938),
     (.820,.235,.960,.466)]),
 "08-conf-detail": ("s08_1.png", [
     (.084,.227,.123,.250),
     (.059,.425,.252,.450),
     (.060,.519,.361,.692),
     (.377,.297,.521,.410)]),
 "09-sequence-copy": ("s09_1.png", [
     (.103,.843,.195,.884),
     (.613,.742,.736,.779)]),
 "10-search-tap": ("s10_1.png", [
     (.085,.159,.503,.227)]),
 "11-tap-input": ("s11_1.png", [
     (.194,.194,.392,.230),
     (.206,.562,.264,.590),
     (.271,.549,.550,.735)]),
 "12-tap-chain": ("s12_1.png", [
     (.195,.301,.552,.350),
     (.193,.414,.552,.450),
     (.193,.498,.552,.534),
     (.911,.943,.962,.977)]),
 "08b-metric-detail-tabs": ("21-metric-detail-interface.png", [
     (.014,.021,.635,.083,'r'),
     (.014,.245,.988,.892,'b')]),
 "11b-file-picker-best": ("22-file-picker-best.png", [
     (.022,.345,.112,.390),
     (.190,.642,.973,.683)]),
 "13-tap-metrics": ("20-tap-metrics.png", [
     (.306,.473,.451,.794),
     (.454,.473,.583,.794),
     (.587,.473,.905,.794),
     (.936,.448,.958,.920)]),
 "14-search-immuscope": ("s14_1.png", [
     (.084,.281,.515,.380)]),
 "15-immuscope-sequence": ("s15_1.png", [
     (.024,.290,.167,.324),
     (.208,.294,.939,.369)]),
 "16-immuscope-allele": ("s16_1.png", [
     (.195,.191,.839,.221),
     (.196,.264,.955,.298),
     (.196,.339,.955,.381),
     (.914,.939,.965,.972)]),
}

# 주석 없이 그대로 복사할 결과 플롯
COPY = {
 "13a-tap-cdrlen":  "s13_4.png",
 "13b-tap-psh":     "s13_2.png",
 "13c-tap-ppc":     "s13_3.png",
 "13d-tap-pnc":     "s13_1.png",
 "13e-tap-sfvcsp":  "s13_5.png",
 "17-immuscope-im": "s17_2.png",
 "18-immuscope-cd4":"s17_1.png",
 "19-immuscope-el": "s18_1.png",
}

def font(size):
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\malgunbd.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def annotate(src, boxes, out):
    im = Image.open(src).convert("RGB")
    W, H = im.size
    d = ImageDraw.Draw(im)
    lw = max(3, round(W / 450))          # 선 두께
    r  = max(14, round(W / 68))          # 배지 반지름
    f  = font(round(r * 1.25))
    for i, box in enumerate(boxes, 1):
        x0, y0, x1, y1 = box[:4]
        side = box[4] if len(box) > 4 else None   # 'l'(기본) 'r' 't' 'b'
        X0, Y0, X1, Y1 = x0 * W, y0 * H, x1 * W, y1 * H
        d.rounded_rectangle([X0, Y0, X1, Y1], radius=lw * 2, outline=RED, width=lw)
        # 배지 위치: 기본은 박스 바깥 왼쪽, 공간이 없으면 위쪽. side로 직접 지정 가능.
        if side == 'r':   cx, cy = X1 + r * 1.15, (Y0 + Y1) / 2
        elif side == 't': cx, cy = (X0 + X1) / 2, Y0 - r * 1.15
        elif side == 'b': cx, cy = (X0 + X1) / 2, Y1 + r * 1.15
        elif side == 'l' or X0 > r * 1.4:
            cx, cy = X0 - r * 1.15, (Y0 + Y1) / 2
        else:
            cx, cy = X0 + r, max(r + 2, Y0 - r * 1.15)
        cx = min(max(cx, r + 2), W - r - 2)
        cy = min(max(cy, r + 2), H - r - 2)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
        t = str(i)
        bb = d.textbbox((0, 0), t, font=f)
        d.text((cx - (bb[2] - bb[0]) / 2 - bb[0], cy - (bb[3] - bb[1]) / 2 - bb[1]),
               t, font=f, fill="white")
    im.save(out, "PNG", optimize=True)
    return im.size

os.makedirs(DST, exist_ok=True)
for name, (sf, boxes) in JOBS.items():
    size = annotate(os.path.join(SRC, sf), boxes, os.path.join(DST, name + ".png"))
    print(f"{name}.png  <- {sf}  {size}  boxes={len(boxes)}")
for name, sf in COPY.items():
    im = Image.open(os.path.join(SRC, sf)).convert("RGB")
    im.save(os.path.join(DST, name + ".png"), "PNG", optimize=True)
    print(f"{name}.png  <- {sf}  {im.size}  (주석 없음)")
