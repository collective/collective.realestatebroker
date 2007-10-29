from zope.interface import Interface
from zope import schema

from collective.realestatebroker import REBMessageFactory as _


class IRealEstateContent(Interface):
    """Generic real estate fields for both residential and commercial."""

    title = schema.TextLine(
        title=_(u'Title'),
        required=True)
    description = schema.Text(
        title=_(u'Description'),
        description=_(u''))
    address = schema.Text(
        title = _(u'Address'),
        )
    zipCode = schema.TextLine(
        title = _(u'Zip code'),
        )
    city = schema.TextLine(
        title = _(u'City'),
        )
    price = schema.Int(
        title = _(u'Price'),
        description = _(u'Fill in the price without dots or commas.'),
        )
    kk_von = schema.TextLine(
        title = _(u'k.k./v.o.n.'),
        )
    text = schema.Text(
        title = _(u'Body text'),
        description = _(u'Enter the main description for this object.'),
        )
    acceptance = schema.TextLine(
        title = _(u'Acceptance'),
        description = _(u'Enter a brief description for the acceptance.'),
        )
    area = schema.TextLine(
        title = _(u'Ground area'),
        )
    volume = schema.TextLine(
        title = _(u'Volume'),
        )
    constructYear = schema.TextLine(
        title = _(u'Construction year'),
        )
    kindOfBuilding = schema.TextLine(
        title = _(u'Kind of building'),
        )
    heating = schema.TextLine(
        title = _(u'Heating'),
        description = _(u'You can choose more than one option.'),
        )
    insulation = schema.TextLine(
        title = _(u'Insulation'),
        description = _(u'You can choose more than one option.'),
        )
    location = schema.TextLine(
        title = _(u'Location'),
        description = _(u'You can choose more than one option.'),
        )

class IResidential(IRealEstateContent):
    """Interface with the residential-specific fields."""
    rooms = schema.TextLine(
        title = _(u'Number of rooms'),
        )
    house_type = schema.TextLine(
         title = _(u'House type'),
         )
    balcony = schema.Bool(
        title = _(u'Balcony'),
        )
    garden = schema.Bool(
        title = _(u'Garden'),
        )
    kindOfGarden = schema.TextLine(
        title = _(u'Kind of garden'),
        description = _(u'You can choose more than one option.'),
        )
    storage = schema.Bool(
        title = _(u'Storage'),
        )
    garage = schema.Bool(
        title = _(u'Garage'),
        )
    kindOfGarage = schema.TextLine(
        title = _(u'Kind of garage'),
        description = _(u'You can choose more than one option.'),
        )
    airco = schema.Bool(
        title = _(u'airco'),
        )


class ICommercial(IRealEstateContent):
    """Interface with the commercial-specific fields."""
    commercial_type = schema.TextLine(
         title = _(u'Building type'),
         )
    vat = schema.TextLine(
        title = _(u'VAT'),
        )
    rent_buy = schema.Bool(
        title = _(u'Rent or buy'),
        )
    parking = schema.Bool(
        title = _(u'Parking'),
        )
    facilities = schema.TextLine(
        title = _(u'Facilities'),
        description = _(u'You can choose more than one option.'),
        )
