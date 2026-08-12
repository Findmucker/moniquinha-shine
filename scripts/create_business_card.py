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
WHATSAPP_PATH = OUT_DIR / "whatsapp-logo-gradient.png"


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
    baseline = PAGE_H * 0.70

    c.setFont(font, size)
    c.setFillColor(HexColor("#FFFFFF"))
    c.drawString(x, baseline, lead)
    c.setFillColor(HexColor("#F3A83D"))
    c.drawString(x + lead_w, baseline, accent)

    star_w = 13 * MM
    star_h = 13 * MM
    c.drawImage(
        ImageReader(str(STAR_PATH)),
        (PAGE_W - star_w) / 2,
        baseline - 19.5 * MM,
        width=star_w,
        height=star_h,
        preserveAspectRatio=True,
        mask="auto",
    )

    tagline_line_1 = "Limpeza, organização e cuidado do seu lar,"
    tagline_line_2 = "com energia, carinho e um "
    tagline_highlight = "toque pessoal."
    tagline_font = "SegoeUI"
    tagline_size = 7.2
    tagline_leading = 9.4
    first_baseline = BLEED + 10.7 * MM

    c.saveState()
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFillAlpha(0.94)
    c.setFont(tagline_font, tagline_size)
    line_1_width = pdfmetrics.stringWidth(tagline_line_1, tagline_font, tagline_size)
    line_1_x = (PAGE_W - line_1_width) / 2
    c.drawString(line_1_x, first_baseline, tagline_line_1)

    prefix_width = pdfmetrics.stringWidth(tagline_line_2, tagline_font, tagline_size)
    highlight_width = pdfmetrics.stringWidth(tagline_highlight, tagline_font, tagline_size)
    second_x = (PAGE_W - prefix_width - highlight_width) / 2
    c.drawString(second_x, first_baseline - tagline_leading, tagline_line_2)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFillAlpha(0.94)
    c.setFont(tagline_font, tagline_size)
    second_y = first_baseline - tagline_leading
    c.drawString(second_x + prefix_width, second_y, tagline_highlight)
    c.restoreState()

    # Two tiny, asymmetric sparkle clusters give the copy a branded finish
    # without enclosing it or competing with the main mark.
    draw_sparkle(c, line_1_x - 3.8 * MM, first_baseline + 0.8 * MM, 0.48 * MM, "#FFD36A", 0.58)
    draw_sparkle(c, line_1_x - 2.4 * MM, first_baseline + 1.7 * MM, 0.18 * MM, "#7897D2", 0.42)
    right_x = second_x + prefix_width + highlight_width
    draw_sparkle(c, right_x + 3.8 * MM, second_y + 0.9 * MM, 0.44 * MM, "#F3A83D", 0.54)
    draw_sparkle(c, right_x + 2.5 * MM, second_y - 0.6 * MM, 0.17 * MM, "#CDB9E3", 0.42)


def draw_sparkle(c: Canvas, x, y, radius, color, alpha):
    """Draw an organic four-point sparkle as a print-safe vector path."""
    c.saveState()
    c.setFillColor(HexColor(color))
    c.setFillAlpha(alpha)
    p = c.beginPath()
    p.moveTo(x, y + radius)
    p.curveTo(x + radius * 0.08, y + radius * 0.34, x + radius * 0.34, y + radius * 0.08, x + radius, y)
    p.curveTo(x + radius * 0.34, y - radius * 0.08, x + radius * 0.08, y - radius * 0.34, x, y - radius)
    p.curveTo(x - radius * 0.08, y - radius * 0.34, x - radius * 0.34, y - radius * 0.08, x - radius, y)
    p.curveTo(x - radius * 0.34, y + radius * 0.08, x - radius * 0.08, y + radius * 0.34, x, y + radius)
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()


def golden_glitter_line(c: Canvas, center_x, center_y):
    # The larger golden stars follow an intentionally loose, uneven rhythm.
    sparkles = [
        (-30.0, -0.4, 0.30, "#FFF0B7", 0.22),
        (-27.1, 1.3, 0.48, "#FFE49A", 0.30),
        (-23.7, -1.8, 0.64, "#F3A83D", 0.42),
        (-20.8, 1.7, 0.40, "#FFD36A", 0.28),
        (-18.0, -1.2, 0.52, "#FFE49A", 0.30),
        (-15.4, 0.3, 0.72, "#F3A83D", 0.48),
        (-12.2, 2.0, 1.65, "#FFD36A", 0.90),
        (-8.4, -1.5, 0.58, "#FFF0B7", 0.40),
        (-5.1, -1.0, 1.08, "#F7B84C", 0.72),
        (-1.7, 1.2, 0.48, "#FFE49A", 0.34),
        (1.5, -2.0, 0.72, "#FFD36A", 0.54),
        (5.7, 2.3, 1.42, "#F3A83D", 0.82),
        (9.4, -1.4, 0.46, "#FFF0B7", 0.36),
        (13.0, -0.7, 1.02, "#FFD36A", 0.68),
        (16.6, 1.5, 0.58, "#FFE49A", 0.38),
        (20.1, -1.8, 0.46, "#FFF0B7", 0.30),
        (23.4, 1.9, 0.68, "#F3A83D", 0.44),
        (26.9, -0.9, 0.46, "#FFE49A", 0.30),
        (30.0, 0.9, 0.28, "#FFF0B7", 0.22),
    ]
    for dx, dy, radius, color, alpha in sparkles:
        draw_sparkle(c, center_x + dx * MM, center_y + dy * MM, radius * MM, color, alpha)

    # Microstars cling to the edges of the four larger stars. Their colours
    # follow the underlying background: blue on the left, lilac on the right.
    edge_sparkles = [
        (-25.0, -1.5, 0.18, "#6F8FCD", 0.38),
        (-23.4, -3.0, 0.16, "#7896D1", 0.34),
        (-14.2, 2.2, 0.34, "#7897D2", 0.58),
        (-11.7, 4.2, 0.25, "#91A8D8", 0.48),
        (-10.5, 1.0, 0.22, "#7897D2", 0.45),
        (-6.9, -0.8, 0.30, "#849DD3", 0.52),
        (-4.7, -3.0, 0.23, "#91A7D8", 0.44),
        (-3.4, -0.2, 0.20, "#9AA9D6", 0.42),
        (3.8, 2.4, 0.30, "#B2ACDB", 0.52),
        (6.2, 4.1, 0.24, "#C0B3DE", 0.48),
        (7.4, 1.3, 0.22, "#B8AFDC", 0.44),
        (11.3, -0.4, 0.28, "#C8B6E1", 0.52),
        (13.5, -2.6, 0.22, "#D2BDE5", 0.46),
        (14.6, 0.2, 0.20, "#CDB9E3", 0.40),
        (22.1, 2.0, 0.18, "#D6C0E7", 0.38),
        (23.8, 3.2, 0.16, "#DEC8EA", 0.34),
    ]
    for dx, dy, radius, color, alpha in edge_sparkles:
        draw_sparkle(c, center_x + dx * MM, center_y + dy * MM, radius * MM, color, alpha)

    glitter = [
        (-29.1, 1.5, 0.16, "#5F83C5", 0.24), (-25.6, -0.4, 0.18, "#6789C9", 0.28),
        (-22.2, 2.7, 0.16, "#6B8CCC", 0.30), (-19.5, -2.4, 0.18, "#7191CF", 0.30),
        (-17.0, 1.4, 0.20, "#6F90CE", 0.34), (-13.8, -0.5, 0.24, "#7997D1", 0.44),
        (-10.0, 3.2, 0.18, "#88A0D4", 0.38), (-7.2, -2.5, 0.22, "#8FA5D6", 0.42),
        (-3.0, 1.5, 0.20, "#9EABD7", 0.36), (0.0, -0.5, 0.24, "#A9AFD9", 0.44),
        (3.1, 0.8, 0.18, "#B4B1DC", 0.36), (7.7, 3.1, 0.23, "#BDB3DE", 0.42),
        (10.5, -2.2, 0.19, "#C5B6E0", 0.38), (14.8, 2.1, 0.24, "#CEBAE3", 0.44),
        (17.8, -0.7, 0.19, "#D6C0E7", 0.34), (21.8, 0.7, 0.18, "#D7C1E7", 0.32),
        (25.1, -2.2, 0.16, "#DCC6EA", 0.29), (28.2, 2.1, 0.18, "#E0CBEA", 0.26),
    ]
    c.saveState()
    for dx, dy, radius, color, alpha in glitter:
        c.setFillColor(HexColor(color))
        c.setFillAlpha(alpha)
        c.circle(center_x + dx * MM, center_y + dy * MM, radius * MM, stroke=0, fill=1)
    c.restoreState()


def draw_whatsapp_badge(c: Canvas, x, y, radius):
    """Draw the official WhatsApp glyph recolored with the brand gradient."""
    diameter = 2 * radius
    c.drawImage(
        ImageReader(str(WHATSAPP_PATH)),
        x - radius,
        y - radius,
        width=diameter,
        height=diameter,
        preserveAspectRatio=True,
        mask="auto",
    )


def centered_whatsapp_contact(c: Canvas, center_y):
    number = "+351 915 520 147"
    font = "SegoeUI-Bold"
    size = 8.8
    radius = 2.35 * MM
    gap = 2.0 * MM
    number_width = pdfmetrics.stringWidth(number, font, size)
    group_width = 2 * radius + gap + number_width
    badge_x = (PAGE_W - group_width) / 2 + radius
    draw_whatsapp_badge(c, badge_x, center_y + 1.0, radius)

    c.setFont(font, size)
    c.setFillColor(HexColor("#FFF5DD"))
    c.drawString(badge_x + radius + gap, center_y - size * 0.32, number)


def centered_website(c: Canvas):
    text = "www.moniquinhashine.pt"
    font = "SegoeUI-Bold"
    size = 12.8
    width = pdfmetrics.stringWidth(text, font, size)
    c.setFont(font, size)
    c.setFillColor(HexColor("#FFFFFF"))
    c.drawString((PAGE_W - width) / 2, PAGE_H * 0.59, text)

    centered_whatsapp_contact(c, PAGE_H * 0.43)
    golden_glitter_line(c, PAGE_W / 2, PAGE_H * 0.29)


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
