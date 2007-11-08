from StringIO import StringIO

from reportlab.lib import units
from reportlab.platypus import PageBreak
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from zope.component import adapter
from zope.i18n import translate
from zope.interface import implementer
from zope.publisher.interfaces import IRequest

from collective.realestatebroker.interfaces import IRealEstateContent
from collective.realestatebroker.pdf.common import insert_image
from collective.realestatebroker.pdf.common import rebColors
from collective.realestatebroker.pdf.common import rebStyleSeet
from collective.realestatebroker.pdf.common import writeDocument
from collective.realestatebroker.pdf.interfaces import IPDFPresentation


@adapter(IRealEstateContent, IRequest)
@implementer(IPDFPresentation)
def realestateToPDF(context, request):
    # this translates AND encodes to utf-8
    def _(msg, mapping=None):
        return translate(msg, domain='collective.realestatebroker',
                         mapping=mapping,
                         context=request).encode('utf-8')

    # create the document structure
    style = rebStyleSeet()
    colors = rebColors()
    album_view = context.restrictedTraverse('@@realestate_album')
    realestate_view = context.restrictedTraverse('@@realestate')
    floorplan_view = context.restrictedTraverse('@@realestate_floorplans')
    structure = []

    # Front page
    first_image = album_view.image_brains()[0].getObject() # TODO: no images
    price = ' '.join([_(u'Price:'),
                      str(context.getPrice())])
    structure.append(Paragraph(_(u'For sale'), style['huge']))
    structure.append(Spacer(1, 2 * units.cm)) # Somehow the image overlaps...
    structure += insert_image(first_image, full_width=True)
    structure.append(Paragraph(context.Title(), style['big']))
    structure.append(Paragraph(context.getCity(), style['big']))
    structure.append(Paragraph(price, style['big']))
    structure.append(PageBreak())

    # Second page: desc, main text.
    description = context.Description()
    structure.append(Paragraph(description, style['description']))
    text = context.getText()
    structure.append(Paragraph(text, style['normal']))
    structure.append(PageBreak())

    # Photos, sorted by page.
    photo_floors = album_view.photos_for_pdf()
    for floor in photo_floors:
        structure.append(Paragraph(floor['floorname'], style['heading1']))
        for photo in floor['photos']:
            structure += insert_image(photo)
        structure.append(PageBreak())
    #structure.append(PageBreak())

    # Floorplans
    floorplan_floors = floorplan_view.floorplans_for_pdf()
    for floor in floorplan_floors:
        name = _(u'Floor plan for ${floorname}',
                 mapping={'floorname': floor['floorname']})
        structure.append(Paragraph(name, style['heading1']))
        for photo in floor['photos']:
            structure += insert_image(photo, full_width=True)
        structure.append(PageBreak())

    # Characteristics
    data = []
    index = 0
    heading_rows = []
    even_rows = []
    data.append([Paragraph(_(u'Object data'), style['table_header']), ''])
    heading_rows.append(index)
    index += 1
    for local_index, field in enumerate(realestate_view.base_fields()):
        label = field.widget.Label(context)
        value = unicode(field.getAccessor(context)())
        data.append([Paragraph(label, style['table_text']),
                     Paragraph(value, style['table_text'])])
        if (local_index // 2.0 == local_index / 2.0):
            even_rows.append(index)
        index += 1
    for section in realestate_view.characteristic_fields():
        if not section['title']:
            continue
        data.append([Paragraph(section['title'], style['table_header']), ''])
        heading_rows.append(index)
        index += 1
        for local_index, field in enumerate(section['fields']):
            label = field.widget.Label(context)
            value = unicode(field.getAccessor(context)())
            data.append([Paragraph(label, style['table_text']),
                         Paragraph(value, style['table_text'])])
            if (local_index // 2.0 == local_index / 2.0):
                even_rows.append(index)
            index += 1
    table = Table(data=data)
    #TODOxxxxxxxxxxxxxx
    table_style = TableStyle([])
    for row in heading_rows:
        table_style.add('BACKGROUND', (0, row), (1, row),
                        colors['table_heading_background'])
        table_style.add('BOTTOMPADDING', (0, row), (1, row), 7)
    for row in even_rows:
        table_style.add('BACKGROUND', (0, row), (1, row),
                        colors['table_even_background'])
    table_style.add('GRID', (0, 0), (1, -1), 1,
                    colors['table_grid_color'])
    table.setStyle(table_style)
    structure.append(table)
    # TODO: even/odd, headings.
    structure.append(PageBreak())

    # Location + map
    structure.append(Paragraph(_(u'Address data'), style['heading1']))
    table_style = TableStyle([])
    data = []
    data.append([Paragraph(_(u'Address'), style['big']),
                 Paragraph(context.Title(), style['big'])])
    data.append([Paragraph(_(u'Zip code'), style['big']),
                 Paragraph(context.getZipCode(), style['big'])])
    data.append([Paragraph(_(u'City'), style['big']),
                 Paragraph(context.getCity(), style['big'])])
    table = Table(data=data)
    table_style.add('BOTTOMPADDING', (0, 0), (1, -1), 12)
    table.setStyle(table_style)
    structure.append(table)
    # TODO: map
    structure.append(PageBreak())

    # Back matter

    # Write it out. (Originally this code used a tempfile, but I guess that
    # that's something that's not handled right in this zope version.
    stream = StringIO()
    writeDocument(stream, structure)
    return stream.getvalue()
