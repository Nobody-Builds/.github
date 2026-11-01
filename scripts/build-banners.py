"""Builds profile/assets/banner-{light,dark}.png from the Nobody Builds design kit.

    python scripts/build-banners.py <path to Nobody-Builds-Design>

The builder is pasted at its native size (never upscaled), per mascot/README.md.
"""
import io
import sys
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

KIT = Path(sys.argv[1]).resolve()
OUT = Path(__file__).resolve().parent.parent / "profile" / "assets"

NIGHT_SHIFT, BLUEPRINT, HARD_HAT = "#172033", "#2457A6", "#FDC521"
SKY, BUTTER, PAPER, MUTED = "#CFE0F7", "#FFE8A3", "#F5F7FB", "#4A5568"
W, H = 1600, 480


def font(name, size):
    """Pillow can't read WOFF/WOFF2, so decode the webfont to plain TrueType in memory."""
    tt = TTFont(KIT / "fonts" / name)
    tt.flavor = None
    buf = io.BytesIO()
    tt.save(buf)
    buf.seek(0)
    return ImageFont.truetype(buf, size)


def banner(bg, ink, accent, sub, builder, name):
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, W - 1, H - 1), radius=28, fill=bg)

    d.text((72, 92), "nobody builds", font=font("Gilroy-Bold.woff", 34), fill=ink, anchor="ls")
    head = font("Gilroy-Bold.woff", 84)
    d.text((72, 200), "Nobody asked.", font=head, fill=ink, anchor="ls")
    d.text((72, 290), "I built it anyway.", font=head, fill=accent, anchor="ls")
    d.text((72, 350), "Shaan Shoukath's personal org for open source nobody needed.",
           font=font("Gilroy-Medium.woff", 28), fill=sub, anchor="ls")

    pill = font("Gilroy-SemiBold.woff", 22)
    x = 72
    for label, fill in (("Open source", SKY), ("Forked, then made mine", BUTTER), ("Tokens burned: yes", HARD_HAT)):
        w = d.textlength(label, font=pill) + 44
        d.rounded_rectangle((x, 384, x + w, 428), radius=22, fill=fill)
        d.text((x + w / 2, 406), label, font=pill, fill=NIGHT_SHIFT, anchor="mm")
        x += w + 12

    art = Image.open(KIT / "mascot" / builder).convert("RGBA")
    img.alpha_composite(art, (W - art.width - 110, (H - art.height) // 2))
    img.save(OUT / name, optimize=True)


OUT.mkdir(parents=True, exist_ok=True)
banner(PAPER, NIGHT_SHIFT, BLUEPRINT, MUTED, "builder.png", "banner-light.png")
banner(NIGHT_SHIFT, PAPER, HARD_HAT, SKY, "dark/builder.png", "banner-dark.png")
