from reportlab.platypus import Paragraph, PageBreak, Image
from StringIO import StringIO

from zope.interface import implementer
from zope.component import adapter
from zope.publisher.interfaces import IRequest
from zope.i18n import translate

from collective.realestatebroker.interfaces import IRealEstateContent
from collective.realestatebroker.pdf.common import getStyleSheet, writeDocument
from collective.realestatebroker.pdf.interfaces import IPDFPresentation

@adapter(IRealEstateContent, IRequest)
@implementer(IPDFPresentation)
def realestateToPDF(context, request):
    # this translates AND encodes to utf-8
    def _(msg, mapping=None):
        return translate(msg, domain='collective.realestatebroker',
                         mapping=mapping,
                         context=request).encode('utf-8')

    title = ('<para spaceBefore="20" spaceAfter="40">%s</para>'
             % context.Title().encode('utf-8'))
#     description = ('<para spaceBefore="15">%s</para>'
#                    % context.description.encode('utf-8'))
#     ingr = [ingr.encode('utf-8') for ingr in context.ingredients]
#     tools = [tool.encode('utf-8') for tool in context.tools]
#     time_to_cook = _(u'${time_to_cook} mins',
#                      mapping={'time_to_cook': context.time_to_cook})

    # create the document structure
    style = getStyleSheet()
    album = context.restrictedTraverse('@@realestate_album')
    realestate = context.restrictedTraverse('@@realestate')
    structure = []

    # Front page
    first_image = album.image_brains()[0].getObject() # TODO: no images
    first_image_url = first_image.absolute_url()
    price = ' '.join([_(u'Price:'),
                      str(context.getPrice())])
    Paragraph(_(u'For sale'), style['title']),
    structure.append(Image(first_image_url))
    structure.append(Paragraph(title, style['title']))
    structure.append(Paragraph(context.getCity().encode('utf-8'),
                               style['title']))
    structure.append(Paragraph(price, style['title']))
    structure.append(PageBreak())
    # Second page plus photos
    description = context.Description().encode('utf-8')
    structure.append(Paragraph(description, style['Normal']))
    text = context.getText() #.encode('utf-8')
    structure.append(Paragraph(text, style['Normal']))

    structure.append(PageBreak())
    # Floorplans
    floorplan_view = context.restrictedTraverse('@@realestate_floorplans')
    floorplans = floorplan_view.floorplans_for_pdf()
    for name in floorplans:
        image_urls = floorplans[name]
        structure.append(Paragraph(name, style['title']))
        for url in image_urls:
            structure.append(Image(url))
        structure.append(PageBreak())


    #tempfile = TemporaryFile()
    stream = StringIO()
    writeDocument(stream, structure)
    return stream.getvalue()
