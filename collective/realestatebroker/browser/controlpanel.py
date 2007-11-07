from zope.interface import Interface
from zope.component import adapts
from zope.interface import implements
from zope.formlib.form import FormFields

from zope.i18nmessageid import MessageFactory
from zope.schema import TextLine

from plone.app.controlpanel.form import ControlPanelForm

from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import safe_unicode, getSiteEncoding

_ = MessageFactory('collective.realestatebroker')


class IRealEstateBrokerSchema(Interface):
        currency = TextLine(
                        title=_('label_default_currency',
                                default=u'Default currency.'),
                        description=_('help_default_coordinated',
                                      default=u"Specify the default "
                                               "currency to be used "
                                               "for prices."),
                        default=u'EUR',
                        required=True,
                       )


class REBControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(IRealEstateBrokerSchema)

    def __init__(self, context):
        super(REBControlPanelAdapter, self).__init__(context)
        properties = getToolByName(context, 'portal_properties')
        self.context = properties.realestatebroker_properties

    def get_currency(self):
        value = getattr(self.context, 'currency', u'')
        value = safe_unicode(value, getSiteEncoding(self.context))
        return value

    def set_currency(self, value):
        value = safe_unicode(value, getSiteEncoding(self.context))
        self.context._updateProperty('currency', value)

    currency = property(get_currency, set_currency)

 

class RealEstateBrokerControlPanel(ControlPanelForm):

    form_fields = FormFields(IRealEstateBrokerSchema)
    label = _("RealEstateBroker settings")
    description = None
    form_name = _("RealEstateBroker settings")
