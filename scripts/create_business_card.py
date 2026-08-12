from pathlib import Path

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.pagesizes import landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader


MM = 72 / 25.4
TRIM_W = 85 * MM
TRIM_H = 55 * MM
BLEED = 3 * MM
PAGE_W = TRIM_W + 2 * BLEED
PAGE_H = TRIM_H + 2 * BLEED

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output" / "pdf"
PDF_PATH = OUT_DIR / "cartao-visita-moniquinha-shine.pdf"
STAR_PATH = OUT_DIR / "moniquinha-star-print.png"


def register_fonts():
    pdfmetrics.registerFont(TTFont("SegoeUI", r"C:\Windows\Fonts\segoeui.ttf"))
    pdfmetrics.registerFont(TTFont("SegoeUI-Bold", r"C:\Windows\Fonts\segoeuib.ttf"))


def background(c: Canvas):
    # Full-bleed gradient, derived from the site's hero.
    steps = 180
    left = (43 / 255, 65 / 255, 120 / 255)
    middle = (83 / 255, 115 / 255, 181 / 255)
    right = (190 / 255, 169 / 255, 210 / 255)
    # Extend the artwork beyond the MediaBox. This prevents a one-pixel white
    # antialiasing seam when print PDFs are rasterized at certain resolutions.
    overscan = 2
    c.setFillColor(Color(*left))
    c.rect(-overscan, -overscan, PAGE_W + 2 * overscan, PAGE_H + 2 * overscan, stroke=0, fill=1)
    strip = PAGE_W / steps + 0.4
    for i in range(steps):
        t = i / (steps - 1)
        if t < 0.62:
            u = t / 0.62
            rgb = tuple(left[k] * (1 - u) + middle[k] * u for k in range(3))
        else:
            u = (t - 0.62) / 0.38
            rgb = tuple(middle[k] * (1 - u) + right[k] * u for k in range(3))
        c.setFillColor(Color(*rgb))
        c.rect(i * PAGE_W / steps, -overscan, strip, PAGE_H + 2 * overscan, stroke=0, fill=1)

    # Soft decorative circles from the reference, kept outside the safe text area.
    c.saveState()
    c.setFillColor(HexColor("#F8D89A"))
    c.setFillAlpha(0.065)
    c.circle(BLEED + 6 * MM, PAGE_H - BLEED - 6 * MM, 9.5 * MM, stroke=0, fill=1)
    c.setFillColor(HexColor("#EBC0D3"))
    c.setFillAlpha(0.075)
    c.circle(PAGE_W - BLEED - 4 * MM, BLEED + 3 * MM, 8 * MM, stroke=0, fill=1)
    c.setFillColor(HexColor("#FFF0C7"))
    c.setFillAlpha(0.045)
    c.circle(PAGE_W * 0.54, BLEED + 1 * MM, 7 * MM, stroke=0, fill=1)
    c.restoreState()


def centered_brand(c: Canvas):
    font = "SegoeUI-Bold"
    size = 15.6
    lead = "Moniquinha"
    accent = " Shine"
    lead_w = pdfmetrics.stringWidth(lead, font, size)
    accent_w = pdfmetrics.stringWidth(accent, font, size)
    x = (PAGE_W - lead_w - accent_w) / 2
    baseline = PAGE_H * 0.58

    c.setFont(font, size)
    c.setFillColor(HexColor("#FFFFFF"))
    c.drawString(x, baseline, lead)
    c.setFillColor(HexColor("#F3A83D"))
    c.drawString(x + lead_w, baseline, accent)

    star_w = 15 * MM
    star_h = 15 * MM
    c.drawImage(
        ImageReader(str(STAR_PATH)),
        (PAGE_W - star_w) / 2,
        baseline - 18.5 * MM,
        width=star_w,
        height=star_h,
        preserveAspectRatio=True,
        mask="auto",
    )


def centered_website(c: Canvas):
    text = "www.moniquinhashine.pt"
    font = "SegoeUI-Bold"
    size = 12.8
    width = pdfmetrics.stringWidth(text, font, size)
    c.setFont(font, size)
    c.setFillColor(HexColor("#FFFFFF"))
    c.drawString((PAGE_W - width) / 2, (PAGE_H - size) / 2 + 2, text)

    # A fine golden underline gives the back the same brand accent without adding text.
    line_w = 31 * MM
    c.setStrokeColor(HexColor("#F3A83D"))
    c.setLineWidth(1.1)
    c.setLineCap(1)
    c.line((PAGE_W - line_w) / 2, PAGE_H * 0.39, (PAGE_W + line_w) / 2, PAGE_H * 0.39)


def create_pdf():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    register_fonts()
    c = Canvas(str(PDF_PATH), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    c.setTitle("Cartão de visita - Moniquinha Shine")
    c.setAuthor("Moniquinha Shine")
    c.setSubject("Frente e verso, 85 x 55 mm, com 3 mm de sangria")

    background(c)
    centered_brand(c)
    c.showPage()

    background(c)
    centered_website(c)
    c.showPage()

    c.save()
    print(PDF_PATH)


if __name__ == "__main__":
    create_pdf()
