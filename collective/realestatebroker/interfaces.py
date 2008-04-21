from zope.interface import Interface
from zope import schema
from collective.realestatebroker import REBMessageFactory as _


class IRealEstateContent(Interface):
    """Generic real estate fields for both residential and commercial."""

    # Generic data (common)
    # ---------------------
    title = schema.TextLine(title=_(u'Title'), required=True)
    description = schema.Text(title=_(u'Description'), description=_(u''))
    address = schema.Text(title = _(u'Address'))
    zipCode = schema.TextLine(title = _(u'Zip code'))

    # Extend this locally with state/province/land/kanton/whatever.
    city = schema.TextLine(title = _(u'City'))
    text = schema.Text(title = _(u'Body text'),
        description = _(u'Enter the main description for this object.'))
    kindOfBuilding = schema.TextLine(title = _(u'Kind of building'))
    constructYear = schema.TextLine(title = _(u'Construction year'))

    # Measurements (common)
    # ---------------------
    volume = schema.TextLine(title = _(u'Volume'))
    area = schema.TextLine(title = _(u'Ground area'))
    floor_area = schema.TextLine(title = _(u'Floor area'))

    # Object details (common)
    # -----------------------
    heating = schema.TextLine(title = _(u'Heating'),
        description = _(u'You can choose more than one option.'))
    insulation = schema.TextLine(title = _(u'Insulation'),
        description = _(u'You can choose more than one option.'))

    # Environment/garden (common)
    # ---------------------------
    location = schema.TextLine(title = _(u'Location'), # NL: "ligging"
        description = _(u'You can choose more than one option.'))

    # Financial data (common)
    # -----------------------
    price = schema.Int(title = _(u'Price'),
        description = _(u'Fill in the price without dots or commas.'))
    acceptance = schema.TextLine(title = _(u'Acceptance'),
        description = _(u'Enter a brief description for the acceptance.'))
    rent_buy = schema.Bool(title = _(u'Rent or buy'))
    fixedprice_negotiable = schema.TextLine(title = _(u'Negotiable or fixed price'))

    # Location (= google maps)
    #  Stores two int fields, really.
    # -------------------------------
    geolocation = schema.TextLine(title = _(u'Location'))


class IResidential(IRealEstateContent):
    """Interface with the residential-specific fields."""
    # Generic data (residential)
    # --------------------------
    house_type = schema.TextLine(title = _(u'House type'))
    garage = schema.Bool(title = _(u'Garage'))
    kindOfGarage = schema.TextLine(title = _(u'Kind of garage'),
        description = _(u'You can choose more than one option.'))
    storage = schema.Bool(title = _(u'Storage'))
    kindOfStorage = schema.TextLine(title = _(u'Kind of storage'),
        description = _(u'You can choose more than one option.'))

    # Measurements (residential)
    # --------------------------
    rooms = schema.TextLine(title = _(u'Number of rooms'))

    # Outside/garden (residential)
    # ----------------------------
    garden = schema.Bool(title = _(u'Garden'))
    kindOfGarden = schema.TextLine(title = _(u'Kind of garden'),
        description = _(u'You can choose more than one option.'))


class ICommercial(IRealEstateContent):
    """Interface with the commercial-specific fields."""
    # Object details (commercial)
    # ---------------------------
    commercial_type = schema.TextLine(title = _(u'Building type'))
    facilities = schema.TextLine(title = _(u'Facilities'),
        description = _(u'You can choose more than one option.'))

    # Financial data (commercial)
    # ---------------------------
    vat = schema.TextLine(title = _(u'VAT'))

    # Outside/garden (commercial)
    # ---------------------------
    parking = schema.Bool(title = _(u'Parking'))
