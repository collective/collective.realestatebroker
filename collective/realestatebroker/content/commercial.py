"""Schema and content type for commercial real estate."""
from Products.Archetypes import atapi
from collective.realestatebroker.config import PROJECTNAME
from collective.realestatebroker.content import schemata
from collective.realestatebroker.interfaces import ICommercial
from zope.interface import implements

from collective.realestatebroker import REBMessageFactory as _

CommercialSchema = (atapi.OrderedBaseFolderSchema.copy() +
                     schemata.GeneralInfoSchema +
                     schemata.CommercialGeneralInfoSchema +
                     schemata.DescriptionSchema +
                     schemata.GeneralCharacteristicsSchema +
                     schemata.CommercialCharacteristicsSchema
                     )
CommercialSchema['title'].storage = atapi.AnnotationStorage()
CommercialSchema['title'].widget.label = _(u'Address')
CommercialSchema['title'].widget.description = _(u'Fill in the address of this object')
CommercialSchema['description'].storage = atapi.AnnotationStorage()
CommercialSchema['description'].schemata = 'Description'


class Commercial(atapi.OrderedBaseFolder):
    """Folderish content type for commercial real estate."""
    portal_type = "Commercial"
    _at_rename_after_creation = True
    schema = CommercialSchema
    implements(ICommercial)

    address = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    zipCode = atapi.ATFieldProperty('zipCode')
    city = atapi.ATFieldProperty('city')
    price = atapi.ATFieldProperty('price')
    house_type = atapi.ATFieldProperty('house_type')
    rooms = atapi.ATFieldProperty('rooms')
    vat = atapi.ATFieldProperty('vat')
    rent_buy = atapi.ATFieldProperty('rent_buy')
    text = atapi.ATFieldProperty('text')
    acceptance = atapi.ATFieldProperty('acceptance')
    area = atapi.ATFieldProperty('area')
    volume = atapi.ATFieldProperty('volume')
    constructYear = atapi.ATFieldProperty('constructYear')
    location = atapi.ATFieldProperty('location')
    kindOfBuilding = atapi.ATFieldProperty('kindOfBuilding')
    heating = atapi.ATFieldProperty('heating')
    isolation = atapi.ATFieldProperty('isolation')
    parking = atapi.ATFieldProperty('parking')
    facilities = atapi.ATFieldProperty('facilities')


atapi.registerType(Commercial, PROJECTNAME)
