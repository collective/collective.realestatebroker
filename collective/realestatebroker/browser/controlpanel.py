from zope.interface import Interface
from zope.component import adapts
from zope.interface import implements

from zope.i18nmessageid import MessageFactory
from zope import schema

from plone.fieldsets import FormFieldsets
from plone.app.controlpanel.form import ControlPanelForm

from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import safe_unicode, getSiteEncoding

_ = MessageFactory('collective.realestatebroker')


class IREBGeneralSchema(Interface):
    cities = schema.List(
        title = _(u'Cities'),
        description = _(u'Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )
    currency = schema.TextLine(
        title = _(u'Currency'),
        description = _(u'Select the currency that should be prepended before prices.'),
        default = u'EUR',
        required = True,
    )
    location = schema.List (
        title = _('Location'),
        description = _('Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )
    heating = schema.List (
        title = _('Heating'),
        description = _('Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )
    insulation = schema.List (
        title = _('Insulation'),
        description = _('Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )
    floor_names = schema.List (
        title = _('Floor Names'),
        description = _('Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )
    commercial_rent_buy = schema.List (
        title = _('Rent/Buy'),
        description = _('Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )
    fixedprice_negotiable = schema.List (
        title = _('Negotiable or fixed price'),
        description = _('Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )
class IREBSearchFormSchema(Interface):
    min_price = schema.List(
        title = _(u'Minimum search price'),
        description = _(u'Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )
    max_price = schema.List(
        title = _(u'Maximum search price'),
        description = _(u'Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )

class IREBResidentialSchema(Interface):
    residential_house_type = schema.List (
        title = _('House type'),
        description = _('Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )
    residential_rooms = schema.List (
        title = _('Number of rooms'),
        description = _('Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )
    residential_balcony = schema.List (
        title = _(u'Balcony'),
        description = _(u'Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )
    residential_garden = schema.List (
        title = _(u'Garden'),
        description = _(u'Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )
    residential_kindOfGarden = schema.List (
        title = _(u'Kind of garden'),
        description = _(u'Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )
    residential_garage = schema.List (
        title = _(u'Garage'),
        description = _(u'Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )
    residential_kindOfGarage = schema.List (
        title = _(u'Kind of garage'),
        description = _(u'Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )
    residential_airco = schema.List (
        title = _(u'Airco'),
        description = _(u'Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )
    residential_storage = schema.List (
        title = _(u'Storage'),
        description = _(u'Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )


class IREBCommercialSchema(Interface):
    commercial_vat = schema.List (
        title = _('Tax'),
        description = _('Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )
    commercial_type = schema.List (
        title = _('Commercial Type'),
        description = _('Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )
    commercial_facilities = schema.List (
        title = _('Facilities'),
        description = _('Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )
    commercial_parking = schema.List (
        title = _('Parking'),
        description = _('Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )

class IRealEstateBrokerSchema(IREBGeneralSchema, IREBResidentialSchema, IREBCommercialSchema, IREBSearchFormSchema):
    """Combined schema for the adapter lookup.
    """

class REBControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(IRealEstateBrokerSchema)

    def __init__(self, context):
        super(REBControlPanelAdapter, self).__init__(context)
        properties = getToolByName(context, 'portal_properties')
        self.context = properties.realestatebroker_properties


    # General Fieldset Setters/Getters

    def get_currency(self):
        value = getattr(self.context, 'currency', u'')
        value = safe_unicode(value, getSiteEncoding(self.context))
        return value

    def set_currency(self, value):
        value = safe_unicode(value, getSiteEncoding(self.context))
        self.context._updateProperty('currency', value)

    currency = property(get_currency, set_currency)

    def get_cities(self):
        value = getattr(self.context, 'city', u'')
        value = safe_unicode(value, getSiteEncoding(self.context))
        return value

    def set_cities(self, value):
        value = safe_unicode(value, getSiteEncoding(self.context))
        self.context._updateProperty('city', value)

    cities = property(get_cities, set_cities)

    def get_location(self):
        value = getattr(self.context, 'location', u'')
        value = safe_unicode(value, getSiteEncoding(self.context))
        return value

    def set_location(self, value):
        value = safe_unicode(value, getSiteEncoding(self.context))
        self.context._updateProperty('location', value)

    location = property(get_location, set_location)

    def get_heating(self):
        value = getattr(self.context, 'heating', u'')
        value = safe_unicode(value, getSiteEncoding(self.context))
        return value

    def set_heating(self, value):
        value = safe_unicode(value, getSiteEncoding(self.context))
        self.context._updateProperty('heating', value)

    heating = property(get_heating, set_heating)

    def get_insulation(self):
        value = getattr(self.context, 'insulation', u'')
        value = safe_unicode(value, getSiteEncoding(self.context))
        return value

    def set_insulation(self, value):
        value = safe_unicode(value, getSiteEncoding(self.context))
        self.context._updateProperty('insulation', value)

    insulation = property(get_insulation, set_insulation)

    def get_floor_names(self):
        value = getattr(self.context, 'floor_names', u'')
        value = safe_unicode(value, getSiteEncoding(self.context))
        return value

    def set_floor_names(self, value):
        value = safe_unicode(value, getSiteEncoding(self.context))
        self.context._updateProperty('floor_names', value)

    floor_names = property(get_floor_names, set_floor_names)

    def get_fixedprice_negotiable(self):
        value = getattr(self.context, 'fixedprice_negotiable', u'')
        value = safe_unicode(value, getSiteEncoding(self.context))
        return value

    def set_fixedprice_negotiable(self, value):
        value = safe_unicode(value, getSiteEncoding(self.context))
        self.context._updateProperty('fixedprice_negotiable', value)

    fixedprice_negotiable = property(get_fixedprice_negotiable, set_fixedprice_negotiable)

    # Residential Fieldset Setters/Getters


    def get_residential_house_type(self):
        value = getattr(self.context, 'residential_house_type', u'')
        value = safe_unicode(value, getSiteEncoding(self.context))
        return value

    def set_residential_house_type(self, value):
        value = safe_unicode(value, getSiteEncoding(self.context))
        self.context._updateProperty('residential_house_type', value)

    residential_house_type = property(get_residential_house_type, set_residential_house_type)

    def get_residential_rooms(self):
        value = getattr(self.context, 'residential_rooms', u'')
        value = safe_unicode(value, getSiteEncoding(self.context))
        return value

    def set_residential_rooms(self, value):
        value = safe_unicode(value, getSiteEncoding(self.context))
        self.context._updateProperty('residential_rooms', value)

    residential_rooms = property(get_residential_rooms, set_residential_rooms)

    def get_residential_balcony(self):
        value = getattr(self.context, 'residential_balcony', u'')
        value = safe_unicode(value, getSiteEncoding(self.context))
        return value

    def set_residential_balcony(self, value):
        value = safe_unicode(value, getSiteEncoding(self.context))
        self.context._updateProperty('residential_balcony', value)

    residential_balcony = property(get_residential_balcony, set_residential_balcony)

    def get_residential_garden(self):
        value = getattr(self.context, 'residential_garden', u'')
        value = safe_unicode(value, getSiteEncoding(self.context))
        return value

    def set_residential_garden(self, value):
        value = safe_unicode(value, getSiteEncoding(self.context))
        self.context._updateProperty('residential_garden', value)

    residential_garden = property(get_residential_garden, set_residential_garden)

    def get_residential_kindOfGarden(self):
        value = getattr(self.context, 'residential_kindOfGarden', u'')
        value = safe_unicode(value, getSiteEncoding(self.context))
        return value

    def set_residential_kindOfGarden(self, value):
        value = safe_unicode(value, getSiteEncoding(self.context))
        self.context._updateProperty('residential_kindOfGarden', value)

    residential_kindOfGarden = property(get_residential_kindOfGarden, set_residential_kindOfGarden)

    def get_residential_garage(self):
        value = getattr(self.context, 'residential_garage', u'')
        value = safe_unicode(value, getSiteEncoding(self.context))
        return value

    def set_residential_garage(self, value):
        value = safe_unicode(value, getSiteEncoding(self.context))
        self.context._updateProperty('residential_garage', value)

    residential_garage = property(get_residential_garage, set_residential_garage)

    def get_residential_kindOfGarage(self):
        value = getattr(self.context, 'residential_kindOfGarage', u'')
        value = safe_unicode(value, getSiteEncoding(self.context))
        return value

    def set_residential_kindOfGarage(self, value):
        value = safe_unicode(value, getSiteEncoding(self.context))
        self.context._updateProperty('residential_kindOfGarage', value)

    residential_kindOfGarage = property(get_residential_kindOfGarage, set_residential_kindOfGarage)

    def get_residential_airco(self):
        value = getattr(self.context, 'residential_airco', u'')
        value = safe_unicode(value, getSiteEncoding(self.context))
        return value

    def set_residential_airco(self, value):
        value = safe_unicode(value, getSiteEncoding(self.context))
        self.context._updateProperty('residential_airco', value)

    residential_airco = property(get_residential_airco, set_residential_airco)

    def get_residential_storage(self):
        value = getattr(self.context, 'residential_storage', u'')
        value = safe_unicode(value, getSiteEncoding(self.context))
        return value

    def set_residential_storage(self, value):
        value = safe_unicode(value, getSiteEncoding(self.context))
        self.context._updateProperty('residential_storage', value)

    residential_storage = property(get_residential_storage, set_residential_storage)

    # Commercial Fieldset Setters/Getters

    def get_commercial_vat(self):
        value = getattr(self.context, 'commercial_vat', u'')
        value = safe_unicode(value, getSiteEncoding(self.context))
        return value

    def set_commercial_vat(self, value):
        value = safe_unicode(value, getSiteEncoding(self.context))
        self.context._updateProperty('commercial_vat', value)

    commercial_vat = property(get_commercial_vat, set_commercial_vat)

    def get_commercial_rent_buy(self):
        value = getattr(self.context, 'commercial_rent_buy', u'')
        value = safe_unicode(value, getSiteEncoding(self.context))
        return value

    def set_commercial_rent_buy(self, value):
        value = safe_unicode(value, getSiteEncoding(self.context))
        self.context._updateProperty('commercial_rent_buy', value)

    commercial_rent_buy = property(get_commercial_rent_buy, set_commercial_rent_buy)

    def get_commercial_type(self):
        value = getattr(self.context, 'commercial_type', u'')
        value = safe_unicode(value, getSiteEncoding(self.context))
        return value

    def set_commercial_type(self, value):
        value = safe_unicode(value, getSiteEncoding(self.context))
        self.context._updateProperty('commercial_type', value)

    commercial_type = property(get_commercial_type, set_commercial_type)

    def get_commercial_facilities(self):
        value = getattr(self.context, 'commercial_facilities', u'')
        value = safe_unicode(value, getSiteEncoding(self.context))
        return value

    def set_commercial_facilities(self, value):
        value = safe_unicode(value, getSiteEncoding(self.context))
        self.context._updateProperty('commercial_facilities', value)

    commercial_facilities = property(get_commercial_facilities, set_commercial_facilities)

    def get_commercial_parking(self):
        value = getattr(self.context, 'commercial_parking', u'')
        value = safe_unicode(value, getSiteEncoding(self.context))
        return value

    def set_commercial_parking(self, value):
        value = safe_unicode(value, getSiteEncoding(self.context))
        self.context._updateProperty('commercial_parking', value)

    commercial_parking = property(get_commercial_parking, set_commercial_parking)


    # SearchForm Fieldset Setters/Getters

    def get_min_price(self):
        value = getattr(self.context, 'min_price', u'')
        value = safe_unicode(value, getSiteEncoding(self.context))
        return value

    def set_min_price(self, value):
        value = safe_unicode(value, getSiteEncoding(self.context))
        self.context._updateProperty('min_price', value)

    min_price = property(get_min_price, set_min_price)

    def get_max_price(self):
        value = getattr(self.context, 'max_price', u'')
        value = safe_unicode(value, getSiteEncoding(self.context))
        return value

    def set_max_price(self, value):
        value = safe_unicode(value, getSiteEncoding(self.context))
        self.context._updateProperty('max_price', value)

    max_price = property(get_max_price, set_max_price)

generalset = FormFieldsets(IREBGeneralSchema)
generalset.id = 'general'
generalset.label = _(u'General')

residentialset = FormFieldsets(IREBResidentialSchema)
residentialset.id = 'residentialform'
residentialset.label = _(u'Residential')

commercialset = FormFieldsets(IREBCommercialSchema)
commercialset.id = 'commercialform'
commercialset.label = _(u'Commercial')

searchset = FormFieldsets(IREBSearchFormSchema)
searchset.id = 'searchform'
searchset.label = _(u'Searching')

class RealEstateBrokerControlPanel(ControlPanelForm):
    form_fields = FormFieldsets(generalset,residentialset,commercialset,searchset)
    label = _(u"RealEstateBroker settings")
    description = _(u"Specify the different default values and value lists that "
                     "are used througout Real Estate Broker")
    form_name = _(u"RealEstateBroker settings")
