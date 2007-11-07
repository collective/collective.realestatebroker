import os.path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, SimpleDocTemplate, Spacer
from reportlab.lib import styles, units, pagesizes


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


def writeDocument(stream, structure):
    #logofile = os.path.join(os.path.dirname(__file__), 'worldcookery.png')
    doc = SimpleDocTemplate(stream,
                            pagesize=pagesizes.A4,
                            leftMargin = 2.5 * units.cm,
                            rightMargin = 2.5 * units.cm,
                            topMargin = 4 * units.cm,
                            bottomMargin = 3 * units.cm,
                            )
    doc.build(list(structure))


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
