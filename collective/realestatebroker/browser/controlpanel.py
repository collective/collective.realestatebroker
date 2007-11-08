from zope.interface import Interface
from zope.component import adapts
from zope.interface import implements
from zope.formlib.form import FormFields

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
        title = _('label_cities',
                default = u'Cities where Real Estate can be added'),
        description = _('help_cities',
                      default = u"Real Estate objects can only be in these cities."),
        value_type = schema.TextLine(),
        required = True,
    )   
    currency = schema.TextLine(
        title = _('label_default_currency',
                default = u'Default currency.'),
        description = _('help_default_currency',
                default = u"Specify the default currency to be used for prices."),
        default = u'EUR',
        required = True,
     )
        
class IREBSearchFormSchema(Interface):
    min_price = schema.List(
        title = _('label_min_price',
                default = u'selectable minimum price'),
        description = _('help_min_price',
                default = u"Specify the values to list as minimum prices in the"
                           "price range of the search form."),
        value_type = schema.TextLine(),
        required = True,
    )
    max_price = schema.List(
        title = _('label_max_price',
                default = u'selectable minimum price'),
        description = _('help_max_price',
                default = u"Specify the values to list as minimum prices in the"
                           "price range of the search form."),
        value_type = schema.TextLine(),
        required = True,
    )

class IREBResidentialSchema(Interface):
    residential_balcony = schema.List (
        title = _('Balcony'),
        description = _('Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )
    residential_garden = schema.List (
        title = _('Garden'),
        description = _('Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    ) 
    residential_kindOfGarden = schema.List (
        title = _('Kind of garden'),
        description = _('Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )  
    residential_garage = schema.List (
        title = _('Garage'),
        description = _('Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )
    residential_kindOfGarage = schema.List (
        title = _('Kind of garage'),
        description = _('Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )
    residential_airco = schema.List (
        title = _('Airco'),
        description = _('Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )
    residential_storage = schema.List (
        title = _('Storage'),
        description = _('Enter the options to choose from.'),
        value_type = schema.TextLine(),
        required = True,
    )


class IRealEstateBrokerSchema(IREBGeneralSchema, IREBResidentialSchema, IREBSearchFormSchema):
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


    # Residentia Fieldset Setters/Getters

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
residentialset.label = _(u'Residential form')

searchset = FormFieldsets(IREBSearchFormSchema)
searchset.id = 'searchform'
searchset.label = _(u'Search form')

class RealEstateBrokerControlPanel(ControlPanelForm):
    form_fields = FormFieldsets(generalset,residentialset,searchset)
    label = _("RealEstateBroker settings")
    description = None
    form_name = _("RealEstateBroker settings")
