"""Schema and content type for commercial real estate."""
from Products.Archetypes import atapi
from collective.realestatebroker.config import PROJECTNAME
from collective.realestatebroker.content.schemata import GeneralInfoSchema
from collective.realestatebroker.content import schemata
from collective.realestatebroker.interfaces import ICommercial
from zope.interface import implements

CommercialSchema = (atapi.OrderedBaseFolderSchema.copy() +
                     schemata.GeneralInfoSchema +
                     schemata.CommercialGeneralInfoSchema +
                     schemata.DescriptionSchema +
                     schemata.GeneralCharacteristicsSchema +
                     schemata.CommercialCharacteristicsSchema
                     )
CommercialSchema['title'].storage = atapi.AnnotationStorage()
CommercialSchema['description'].storage = atapi.AnnotationStorage()


class Commercial(atapi.OrderedBaseFolder):
    """Folderish content type for commercial real estate."""
    portal_type = "Commercial"
    _at_rename_after_creation = True
    schema = CommercialSchema
    implements(ICommercial)

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    address = atapi.ATFieldProperty('address')
    zipCode = atapi.ATFieldProperty('zipCode')
    city = atapi.ATFieldProperty('city')
    price = atapi.ATFieldProperty('price')
    house_type = atapi.ATFieldProperty('house_type')
    rooms = atapi.ATFieldProperty('rooms')
    vat = atapi.ATFieldProperty('vat')
    rent_buy = atapi.ATFieldProperty('rent_buy')
    desc = atapi.ATFieldProperty('desc')
    mainText = atapi.ATFieldProperty('mainText')
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

    # temporary vocabulary for selectionwidgets in Schemas
    def _get_dummy_vocab(self):
        return ("choice 1", "choice 2", "choice 3")


atapi.registerType(Commercial, PROJECTNAME)
