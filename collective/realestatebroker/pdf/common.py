import os.path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, SimpleDocTemplate
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
    return stylesheet

def writeDocument(stream, structure):
    logofile = os.path.join(os.path.dirname(__file__), 'worldcookery.png')
    logo = Image(logofile, 2060.0*units.inch/600, 651*units.inch/600)
    doc = SimpleDocTemplate(stream, pagesize=pagesizes.A4)
    doc.build([logo] + list(structure))