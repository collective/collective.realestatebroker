from tempfile import TemporaryFile
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Image
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
    first_image = album.image_brains()[0].getObject() # TODO: no images
    first_image_url = first_image.absolute_url()
    doc_structure = [
        # Front page
        Paragraph(_('For sale'), style['title']),
        Image(first_image_url),
        Paragraph(title, style['title']),
        PageBreak(),
#         Paragraph(_(u"Name of the dish:"), style['h3']),
#         Paragraph(context.name.encode('utf-8'), style['Normal']),
#         Paragraph(_(u"Ingredients:"), style['h3']),
#         Paragraph(', '.join(ingr), style['Normal']),
#         Paragraph(_(u"Needed kitchen tools:"), style['h3']),
#         Paragraph(', '.join(tools), style['Normal']),
#         Paragraph(_(u"Time needed for preparation:"), style['h3']),
#         Paragraph(time_to_cook, style['Normal']),
#         Paragraph(description,  style['Normal']),
        ]

    #tempfile = TemporaryFile()
    stream = StringIO()
    writeDocument(stream, doc_structure)
    return stream.getvalue()
