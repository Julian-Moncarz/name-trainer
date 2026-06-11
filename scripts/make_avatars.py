#!/usr/bin/env python3
"""Generate a circular-friendly initials avatar for any people missing a photo.

Usage:
    python3 scripts/make_avatars.py "Ada Lovelace" "Alan Turing"
    # writes faces/ada_lovelace.png, faces/alan_turing.png

Requires Pillow:  uv pip install pillow   (or: pip install pillow)
Use these as a fallback when you can't find a real photo. The app shows whatever
image path you put in people.js, so .png avatars and .jpg photos both work.
"""
import sys, os, re, hashlib, colorsys
from PIL import Image, ImageDraw, ImageFont

FACES = os.path.join(os.path.dirname(__file__), '..', 'faces')

def slug(name):
    return re.sub(r'[^a-z0-9]+', '_', name.lower()).strip('_')

def font(size):
    for p in ['/System/Library/Fonts/Helvetica.ttc',
              '/System/Library/Fonts/Supplemental/Arial.ttf',
              '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
              '/Library/Fonts/Arial.ttf']:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def make(name, size=400):
    os.makedirs(FACES, exist_ok=True)
    initials = ''.join(w[0] for w in re.findall(r'[A-Za-z]+', name)[:2]).upper() or '?'
    h = int(hashlib.md5(name.encode()).hexdigest(), 16)
    r, g, b = colorsys.hsv_to_rgb((h % 360) / 360.0, 0.55, 0.62)
    img = Image.new('RGB', (size, size), (int(r*255), int(g*255), int(b*255)))
    dr = ImageDraw.Draw(img)
    f = font(int(size * 0.46))
    bb = dr.textbbox((0, 0), initials, font=f)
    dr.text(((size - (bb[2]-bb[0]))/2 - bb[0], (size - (bb[3]-bb[1]))/2 - bb[1]),
            initials, font=f, fill=(255, 255, 255))
    out = os.path.join(FACES, slug(name) + '.png')
    img.save(out, 'PNG')
    return out

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    for n in sys.argv[1:]:
        print('wrote', make(n))
