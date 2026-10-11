"""Create a size proof from magnet artwork, without altering its pixels.

This is an RGB size proof, not a bleed/cutting production master.
"""

import argparse
from pathlib import Path

from PIL import Image

from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas


ROOT = Path(__file__).resolve().parents[1]
VARIANTS = {
    "coracao": (75, 75, "75mm"),
    "retangular": (90, 60, "90x60mm"),
    "estrela": (90, 90, "90mm"),
}


def create_pdf(variant="coracao"):
    width_mm, height_mm, suffix = VARIANTS[variant]
    width, height = width_mm * mm, height_mm * mm
    artwork = ROOT / f"materiais/imanes/moniquinha-shine-iman-{variant}-avatar.png"
    output = artwork.with_name(f"{artwork.stem}-{suffix}.pdf")
    with Image.open(artwork) as image:
        pixel_width, pixel_height = image.size
    scale = min(width / pixel_width, height / pixel_height)
    image_width, image_height = pixel_width * scale, pixel_height * scale
    canvas = Canvas(str(output), pagesize=(width, height), pageCompression=1)
    canvas.setTitle(f"Moniquinha Shine - iman {variant} com avatar - prova {width_mm} x {height_mm} mm")
    canvas.setAuthor("Moniquinha Shine")
    canvas.setSubject("Prova de tamanho, RGB, sem sangria nem linha vetorial de corte")
    canvas.drawImage(
        ImageReader(str(artwork)),
        (width - image_width) / 2,
        (height - image_height) / 2,
        image_width,
        image_height,
        mask="auto",
    )
    canvas.showPage()
    canvas.save()
    print(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", choices=VARIANTS, default="coracao")
    create_pdf(parser.parse_args().variant)
