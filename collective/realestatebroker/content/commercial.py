"""Schema and content type for commercial real estate."""
from Products.Archetypes import atapi
from collective.realestatebroker.config import PROJECTNAME
from collective.realestatebroker.content import schemata
from collective.realestatebroker.interfaces import ICommercial
from zope.interface import implements
from Products.PloneFlashUpload.interfaces import IUploadingCapable
from archetypes.schemaextender.interfaces import IExtensible
from Products.CMFCore.utils import getToolByName

from collective.realestatebroker import REBMessageFactory as _

CommercialSchema = (atapi.OrderedBaseFolderSchema.copy() +
                     schemata.GeneralSchema +
                     schemata.CommercialSpecificSchema
                     )
CommercialSchema['title'].storage = atapi.AnnotationStorage()
CommercialSchema['title'].widget.label = _(u'Address')
CommercialSchema['title'].widget.description = _(u'Fill in the address of this object')
CommercialSchema['description'].storage = atapi.AnnotationStorage()
CommercialSchema['description'].schemata = 'default'

# Move text and descriptionfield to put them at the bottom of the default tab
CommercialSchema.moveField('text',pos='bottom')
CommercialSchema.moveField('description',before='text')

# Move related kk_von and rent_buy field after the price field
CommercialSchema.moveField('rent_buy',after='price')


class Commercial(atapi.OrderedBaseFolder):
    """Folderish content type for commercial real estate."""
    portal_type = "Commercial"
    _at_rename_after_creation = True
    schema = CommercialSchema
    implements(ICommercial, IUploadingCapable, IExtensible)

    address = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    zipcode = atapi.ATFieldProperty('zipCode')
    city = atapi.ATFieldProperty('city')
    price = atapi.ATFieldProperty('price')
    commercial_type = atapi.ATFieldProperty('commercial_type')
    vat = atapi.ATFieldProperty('vat')
    rent_buy = atapi.ATFieldProperty('rent_buy')
    text = atapi.ATFieldProperty('text')
    acceptance = atapi.ATFieldProperty('acceptance')
    area = atapi.ATFieldProperty('area')
    floor_area = atapi.ATFieldProperty('floor_area')
    volume = atapi.ATFieldProperty('volume')
    construct_year = atapi.ATFieldProperty('constructYear')
    location = atapi.ATFieldProperty('location')
    kind_of_building = atapi.ATFieldProperty('kindOfBuilding')
    heating = atapi.ATFieldProperty('heating')
    insulation = atapi.ATFieldProperty('insulation')
    parking = atapi.ATFieldProperty('parking')
    facilities = atapi.ATFieldProperty('facilities')

    def exclude_from_nav(self):
        """We don't want real estate to show up in the nav tree.
        """
        return True

    def default_rent_buy(self):
        pprops = getToolByName(self, 'portal_properties')
        props = pprops.realestatebroker_properties
        rent_buy_props = props.getProperty('commercial_rent_buy')
        return rent_buy_props[0]

    def default_fixedprice_negotiable(self):
        pprops = getToolByName(self, 'portal_properties')
        props = pprops.realestatebroker_properties
        fp_neg_props = props.getProperty('fixedprice_negotiable')
        return fp_neg_props[0]

atapi.registerType(Commercial, PROJECTNAME)
