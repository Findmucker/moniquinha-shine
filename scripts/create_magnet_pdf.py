"""Create a 75 mm size proof from the magnet artwork, without altering its pixels.

This is an RGB size proof, not a bleed/cutting production master.
"""

from pathlib import Path

from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas


ROOT = Path(__file__).resolve().parents[1]
ARTWORK = ROOT / "materiais/imanes/moniquinha-shine-iman-coracao-avatar.png"
OUTPUT = ARTWORK.with_name("moniquinha-shine-iman-coracao-avatar-75mm.pdf")


def create_pdf():
    size = 75 * mm
    canvas = Canvas(str(OUTPUT), pagesize=(size, size), pageCompression=1)
    canvas.setTitle("Moniquinha Shine - iman em coracao com avatar - prova 75 mm")
    canvas.setAuthor("Moniquinha Shine")
    canvas.setSubject("Prova de tamanho, RGB, sem sangria nem linha vetorial de corte")
    canvas.drawImage(ImageReader(str(ARTWORK)), 0, 0, size, size, mask="auto")
    canvas.showPage()
    canvas.save()
    print(OUTPUT)


if __name__ == "__main__":
    create_pdf()
