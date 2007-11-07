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
        title=_('label_cities',
                default=u'Cities where Real Estate can be added'),
        description=_('help_cities',
                      default=u"Real Estate objects can only be in these cities."),
        value_type=schema.TextLine(),
        required=True,
    )   
    currency = schema.TextLine(
        title=_('label_default_currency',
                default=u'Default currency.'),
        description=_('help_default_currency',
                default=u"Specify the default currency to be used for prices."),
                        default=u'EUR',
                        required=True,
     )
        
class IREBSearchFormSchema(Interface):
    min_price = schema.List(
        title=_('label_min_price',
                default=u'selectable minimum price'),
        description=_('help_min_price',
                default=u"Specify the values to list as minimum prices in the"
                "price range of the search form."),
                        value_type=schema.TextLine(),
                        required=True,
                       )
    max_price = schema.List(
        title=_('label_max_price',
                default=u'selectable minimum price'),
        description=_('help_max_price',
                default=u"Specify the values to list as minimum prices in the"
                "price range of the search form."),
                        value_type=schema.TextLine(),
                        required=True,
                       )

class IRealEstateBrokerSchema(IREBGeneralSchema, IREBSearchFormSchema):
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

searchformset = FormFieldsets(IREBSearchFormSchema)
searchformset.id = 'searchform'
searchformset.label = _(u'Search form')



class RealEstateBrokerControlPanel(ControlPanelForm):
    form_fields = FormFieldsets(generalset,searchformset)
    label = _("RealEstateBroker settings")
    description = None
    form_name = _("RealEstateBroker settings")
