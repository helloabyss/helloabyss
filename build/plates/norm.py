"""House grade for This Week in Tech plates.

Every plate is generated WELL EXPOSED, then normalised here. Grading in post
rather than prompting for darkness is deliberate: asking the model for
"near-black" returns near-empty frames (measured: 99% of pixels below
luminance 40). Normalising instead gives every plate the same luminance and
saturation, which is what makes episodes look like siblings.
"""
from PIL import Image, ImageEnhance, ImageOps
import colorsys

TARGET_LUM = 35.0          # mean luminance, 0-255

def meanlum(im):
    px = list(im.resize((100, 178)).getdata())
    return sum(0.2126*r + 0.7152*g + 0.0722*b for r, g, b in px) / len(px)

def meansat(im):
    px = list(im.resize((100, 178)).getdata())
    return sum(colorsys.rgb_to_hsv(r/255, g/255, b/255)[1] for r, g, b in px) / len(px)

def house(src):
    im = Image.open(src).convert('RGB')
    im = ImageOps.autocontrast(im, cutoff=(1, 1))

    # soft-knee highlight rolloff - without this a bright screen or window
    # clips and no gamma can recover it (measured: 32% blown pixels)
    knee = []
    for i in range(256):
        v = i / 255.0
        v = v if v < 0.62 else 0.62 + (v - 0.62) * 0.42
        knee.append(max(0, min(255, int(v * 255))))
    im = im.point(knee * 3)

    s = meansat(im)
    if s > 0.001:
        im = ImageEnhance.Color(im).enhance(min(1.0, 0.16 / s))
    im = ImageEnhance.Contrast(im).enhance(1.12)

    # solve gamma for the target luminance, per plate
    lo, hi = 0.35, 3.2
    for _ in range(18):
        gm = (lo + hi) / 2
        lut = [max(0, min(255, int(((i/255.0) ** gm) * 255))) for i in range(256)]
        if meanlum(im.point(lut * 3)) > TARGET_LUM:
            lo = gm
        else:
            hi = gm
    gm = (lo + hi) / 2
    lut = [max(0, min(255, int(((i/255.0) ** gm) * 255))) for i in range(256)]
    im = im.point(lut * 3)

    # cool the shadows, leave the warm highlight as the amber accent
    r, g, b = im.split()
    b = b.point([max(0, min(255, int(x * 0.90))) for x in range(256)])
    g = g.point([max(0, min(255, int(x * 0.975))) for x in range(256)])
    return Image.merge('RGB', (r, g, b))
