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
        description = _(u'Fill in the address of this object'),
        )
    zipCode = schema.TextLine(
        title = _(u'Zip code'),
        description = _(u'Fill in the zip code of this object'),
        )
    city = schema.TextLine(
        title = _(u'City'),
        description = _(u'Fill in the city in which this object is located.'),
        )
    price = schema.Int(
        title = _(u'Price'),
        description = _(u'Fill in the price without dots or commas.'),
        )
    house_type = schema.TextLine(
        title = _(u'Type'),
        description = _(u'Select the type object'),
        )
    rooms = schema.TextLine(
        title = _(u'Rooms'),
        description = _(u'Select the number of rooms for this object'),
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
        title = _(u'Area'),
        description = _(u'Fill in the area of the object.'),
        )
    volume = schema.TextLine(
        title = _(u'Volume'),
        description = _(u'Fill in the volume of this object.'),
        )
    constructYear = schema.TextLine(
        title = _(u'Construction year'),
        description = _(u'Fill in the year of construction of this object.'),
        )
    location = schema.TextLine(
        title = _(u'location'),
        description = _(u'Select the location. You can choose more than 1 option.'),
        )
    kindOfBuilding = schema.TextLine(
        title = _(u'Kind of building'),
        description = _(u'Select what kind of building this is.'),
        )
    heating = schema.TextLine(
        title = _(u'heating'),
        description = _(u'Select the heating system for this object. You can choose more than 1 option'),
        )
    isolation = schema.TextLine(
        title = _(u'isolation'),
        description = _(u'Select the kinds of isolation used for this object. You can choose more than 1 option'),
        )


class IResidential(IRealEstateContent):
    """Interface with the residential-specific fields."""

    kk_von = schema.TextLine(
        title = _(u'k.k./v.o.n.'),
        description = _(u'Select the option.'),
        )
    balcony = schema.Bool(
        title = _(u'Balcony'),
        description = _(u'Select whether this object has a balcony or not.'),
        )
    garden = schema.Bool(
        title = _(u'garden'),
        description = _(u'Select whether this object has a garden or not.'),
        )
    kindOfGarden = schema.TextLine(
        title = _(u'Kind of garden'),
        description = _(u'Select the kind of garden. You can choose more than one option'),
        )
    storage = schema.Bool(
        title = _(u'Storage'),
        description = _(u'Select whether this object has a storage.'),
        )
    garage = schema.Bool(
        title = _(u'Garage'),
        description = _(u'Select whether this object has a garage or not.'),
        )
    kindOfGarage = schema.TextLine(
        title = _(u'kindOfGarage'),
        description = _(u'Select the type garage for this object. You can choose more than 1 option'),
        )
    airco = schema.Bool(
        title = _(u'airco'),
        description = _(u'Select whether this object has an airconditioning or not.'),
        )


class ICommercial(IRealEstateContent):
    """Interface with the commercial-specific fields."""

    vat = schema.TextLine(
        title = _(u'VAT'),
        description = _(u'Select the VAT for this object.'),
        )
    rent_buy = schema.Bool(
        title = _(u'Rent or buy'),
        description = _(u'Select Rent/buy for this object.'),
        )
    parking = schema.Bool(
        title = _(u'Parking'),
        description = _(u'Select here if this object has a private car park.'),
        )
    facilities = schema.TextLine(
        title = _(u'Facilities'),
        description = _(u'Select the facilities. You can choose more than 1 option'),
        )
