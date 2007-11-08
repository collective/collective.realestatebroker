from reportlab.lib.styles import ParagraphStyle
import os.path
from zope.component import queryUtility
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, SimpleDocTemplate, Spacer
from reportlab.lib import styles
from reportlab.lib import units
from reportlab.lib import pagesizes
from collective.realestatebroker.pdf.interfaces import IStyleModifier
from collective.realestatebroker.pdf.interfaces import IHeaderAndFooter


def getStyleSheet():
    fonts = {'LuxiSans': 'luxisr.ttf',
             'LuxiSansOblique': 'luxisri.ttf',
             'LuxiSansBold': 'luxisb.ttf',
             'LuxiSansBoldOblique': 'luxisbi.ttf'}
    for name, fn in fonts.items():
        filename = os.path.join(os.path.dirname(__file__), fn)
        pdfmetrics.registerFont(TTFont(name, filename))

    stylesheet = styles.getSampleStyleSheet()
    stylesheet['Normal'].fontName = 'LuxiSans'
    stylesheet['title'].fontName = 'LuxiSansBold'
    stylesheet['h1'].fontName = 'LuxiSansBold'
    stylesheet['h2'].fontName = 'LuxiSansBold'
    stylesheet['h3'].fontName = 'LuxiSansBoldOblique'
    stylesheet['title'].alignment = 0
    return stylesheet


def rebColors():
    """Return standard colors, but for the stylesheet and for the pdf."""
    colors = {}
    colors['table_heading_background'] = (1, 0, 0) # Red as example.
    colors['table_heading_textcolor'] = (1, 1, 1) # White.
    colors['table_odd_background'] = (1, 1, 1) # White.
    colors['table_even_background'] = (0.9, 0.9, 0.9) # Light gray.
    colors['table_grid_color'] = (0, 0, 0)
    # TODO: grab adapter and give it a chance to modify the colors.
    return colors


def rebStyleSeet():
    """Return realestatebroker stylesheet."""
    stylesheet = {}
    colors = rebColors()
    fonts = {'LuxiSans': 'luxisr.ttf',
             'LuxiSansOblique': 'luxisri.ttf',
             'LuxiSansBold': 'luxisb.ttf',
             'LuxiSansBoldOblique': 'luxisbi.ttf'}
    for name, fn in fonts.items():
        filename = os.path.join(os.path.dirname(__file__), fn)
        pdfmetrics.registerFont(TTFont(name, filename))
    normal_font = 'LuxiSans'
    bold_font = 'LuxiSansBold'
    # Huge is for the huge "for sale" text on the default frontpage.
    huge = ParagraphStyle('huge')
    huge.fontSize = 48
    huge.leading = 50
    huge.spaceAfter = 0
    huge.fontName = bold_font
    stylesheet['huge'] = huge
    # Big: large text on the front page and for the address at the end.
    big = ParagraphStyle('big')
    big.fontSize = 24
    big.leading = 26
    big.spaceAfter = 10
    big.fontName = bold_font
    stylesheet['big'] = big
    # Footer: small text at the bottom of every page.
    footer = ParagraphStyle('footer')
    footer.fontSize = 10
    footer.spaceAfter = 0
    footer.fontName = normal_font
    stylesheet['footer'] = footer
    # Normal: normal text
    normal = ParagraphStyle('normal')
    normal.fontSize = 12
    normal.leading = 14
    normal.spaceAfter = 12
    normal.fontName = normal_font
    stylesheet['normal'] = normal
    # Description: description text, you might want to have this bold or so.
    description = ParagraphStyle('description')
    description.fontSize = 16
    description.leading = 18
    description.spaceAfter = 16
    description.fontName = bold_font
    stylesheet['description'] = description
    # Heading1: heading1 text
    heading1 = ParagraphStyle('heading1')
    heading1.fontSize = 16
    heading1.leading = 18
    heading1.spaceAfter = 16
    heading1.fontName = bold_font
    stylesheet['heading1'] = heading1
    # Table_header: table header text.
    table_header = ParagraphStyle('table_header')
    table_header.fontSize = 14
    table_header.leading = 16
    table_header.spaceAfter = 0
    table_header.fontName = bold_font
    table_header.textColor = colors['table_heading_textcolor']
    stylesheet['table_header'] = table_header
    # Table_text: table header text. White as the header is dark gray.
    table_text = ParagraphStyle('table_text')
    table_text.fontSize = 12
    table_text.leading = 14
    table_text.spaceAfter = 0
    table_text.fontName = normal_font
    stylesheet['table_text'] = table_text

    # TODO: grab adapter if available and give it a change to modify these
    # settings.
    utility = queryUtility(IStyleModifier)
    if not utility:
        return stylesheet
    else:
        return utility(stylesheet)


def header_and_footer(canvas, doc):
    utility = queryUtility(IHeaderAndFooter)
    if not utility:
        return
    else:
        utility(canvas, doc)


def writeDocument(stream, structure):
    #logofile = os.path.join(os.path.dirname(__file__), 'worldcookery.png')
    doc = SimpleDocTemplate(stream,
                            pagesize=pagesizes.A4,
                            leftMargin = 2.5 * units.cm,
                            rightMargin = 2.5 * units.cm,
                            topMargin = 4 * units.cm,
                            bottomMargin = 3 * units.cm,
                            )
    doc.build(list(structure),
              onFirstPage=header_and_footer,
              onLaterPages=header_and_footer,
              )


def insert_image(image, full_width=False):
    """Return image flowable, scaled to fit.

    For landscape images, 'fit' means page width.

    For portrait images, 'fit' means the height has to be the same as that of
    a landscape image.

    """

    url = image.absolute_url()
    width, height = image.getSize()
    if full_width:
        max_width = (21 - 2.5 - 2.5) * units.cm
    else:
        # Add a bit of padding, as otherwise you won't commonly get two photos
        # on the same page.
        max_width = (21 - 2.5 - 2.5 - 2) * units.cm
    if width >= height or full_width:
        # Landscape (or portrait where we want to use the full width/height).
        img_width = max_width
        img_height = max_width * height / width
        # Compensation for too-high images
        max_height = (29.7 - 4 - 3 - 2) * units.cm
        if img_height > max_height:
            factor = max_height / img_height
            img_width = img_width * factor
            img_height = img_height * factor
    else:
        # Portrait.
        img_height = max_width * width / height
        img_width = img_height * width / height
    return [Spacer(1, 0.2 * units.cm),
            Image(url, width=img_width, height=img_height),
            Spacer(1, 0.2 * units.cm)]
