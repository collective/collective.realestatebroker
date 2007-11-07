from  reportlab.lib import units
from reportlab.platypus import Paragraph, PageBreak, Image, Table, Spacer
from reportlab.lib.styles import ParagraphStyle
from StringIO import StringIO

from zope.interface import implementer
from zope.component import adapter
from zope.publisher.interfaces import IRequest
from zope.i18n import translate

from collective.realestatebroker.interfaces import IRealEstateContent
from collective.realestatebroker.pdf.common import getStyleSheet
from collective.realestatebroker.pdf.common import writeDocument
from collective.realestatebroker.pdf.common import insert_image
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
    album_view = context.restrictedTraverse('@@realestate_album')
    realestate_view = context.restrictedTraverse('@@realestate')
    floorplan_view = context.restrictedTraverse('@@realestate_floorplans')
    structure = []

    # Custom styles
    huge_style = ParagraphStyle('huge')
    huge_style.fontSize = 48
    huge_style.spaceAfter = 10

    # Front page
    first_image = album_view.image_brains()[0].getObject() # TODO: no images
    price = ' '.join([_(u'Price:'),
                      str(context.getPrice())])
    structure.append(Paragraph(_(u'For sale'), huge_style))
    structure.append(Spacer(1, 2 * units.cm)) # Somehow the image overlaps...
    structure += insert_image(first_image, full_width=True)
    structure.append(Paragraph(title, style['title']))
    structure.append(Paragraph(context.getCity().encode('utf-8'),
                               style['title']))
    structure.append(Paragraph(price, style['title']))
    structure.append(PageBreak())

    # Second page: desc, main text, plus photos
    description = context.Description().encode('utf-8')
    structure.append(Paragraph(description, style['Normal']))
    text = context.getText() #.encode('utf-8')
    structure.append(Paragraph(text, style['Normal']))
    photo_floors = album_view.photos_for_pdf()
    for floor in photo_floors:
        structure.append(Paragraph(floor['floorname'], style['h1']))
        for photo in floor['photos']:
            structure += insert_image(photo)
        structure.append(PageBreak())
    #structure.append(PageBreak())

    # Floorplans
    floorplan_floors = floorplan_view.floorplans_for_pdf()
    for floor in floorplan_floors:
        name = _(u'Floor plan for ${floorname}',
                 mapping={'floorname': floor['floorname']})
        structure.append(Paragraph(name, style['h1']))
        for photo in floor['photos']:
            structure += insert_image(photo, full_width=True)
        structure.append(PageBreak())

    # Characteristics
    data = []
    data.append([Paragraph(_(u'Object data'), style['title']), ''])
    for field in realestate_view.base_fields():
        label = field.widget.Label(context)
        value = unicode(field.getAccessor(context)())
        data.append([Paragraph(label, style['Normal']),
                     Paragraph(value, style['Normal'])])
    for section in realestate_view.characteristic_fields():
        if not section['title']:
            continue
        data.append([Paragraph(section['title'], style['title']), ''])
        for field in section['fields']:
            label = field.widget.Label(context)
            value = unicode(field.getAccessor(context)())
            data.append([Paragraph(label, style['Normal']),
                         Paragraph(value, style['Normal'])])
    table = Table(data=data)
    structure.append(table)
    # TODO: even/odd, headings.
    structure.append(PageBreak())

    # Location + map
    structure.append(Paragraph(_(u'Address data'), style['h1']))
    data = []
    data.append([Paragraph(_(u'Address'), style['title']),
                 Paragraph(context.Title(), style['title'])])
    data.append([Paragraph(_(u'Zip code'), style['title']),
                 Paragraph(context.getZipCode(), style['title'])])
    data.append([Paragraph(_(u'City'), style['title']),
                 Paragraph(context.getCity(), style['title'])])
    table = Table(data=data)
    structure.append(table)
    # TODO: map
    structure.append(PageBreak())

    # Back matter

    # Write it out. (Originally this code used a tempfile, but I guess that
    # that's something that's not handled right in this zope version.
    stream = StringIO()
    writeDocument(stream, structure)
    return stream.getvalue()
