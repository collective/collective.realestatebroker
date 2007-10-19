"""Schema and content type for residential real estate."""
from zope.interface import directlyProvides
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from Products.Archetypes import atapi
from collective.realestatebroker import REBMessageFactory as _
from collective.realestatebroker.config import PROJECTNAME
from collective.realestatebroker.content import schemata
from collective.realestatebroker.interfaces import IResidential
from collective.realestatebroker.content.base import DummyResidentialVocabularyFactory,CityVocabularyFactory

ResidentialSchema = (atapi.OrderedBaseFolderSchema.copy() +
                     schemata.GeneralInfoSchema +
                     schemata.ResidentialGeneralInfoSchema +
                     schemata.DescriptionSchema +
                     schemata.GeneralCharacteristicsSchema +
                     schemata.ResidentialCharacteristicsSchema
                     )
ResidentialSchema['title'].storage = atapi.AnnotationStorage()
ResidentialSchema['title'].widget.label = _(u'Address')
ResidentialSchema['title'].widget.description = _(u'Fill in the address of this object')
ResidentialSchema['description'].storage = atapi.AnnotationStorage()
ResidentialSchema['description'].schemata = 'Description'


directlyProvides(DummyResidentialVocabularyFactory, IVocabularyFactory)
directlyProvides(CityVocabularyFactory, IVocabularyFactory)


class Residential(atapi.OrderedBaseFolder):
    """Folderish content type for residential real estate."""
    implements(IResidential)

    portal_type = "Residential"
    _at_rename_after_creation = True
    schema = ResidentialSchema

    address = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    zipcode = atapi.ATFieldProperty('zipCode')
    city = atapi.ATFieldProperty('city')
    price = atapi.ATFieldProperty('price')
    house_type = atapi.ATFieldProperty('house_type')
    rooms = atapi.ATFieldProperty('rooms')
    kk_von = atapi.ATFieldProperty('kk_von')
    text = atapi.ATFieldProperty('text')
    acceptance = atapi.ATFieldProperty('acceptance')
    area = atapi.ATFieldProperty('area')
    volume = atapi.ATFieldProperty('volume')
    construct_year = atapi.ATFieldProperty('constructYear')
    location = atapi.ATFieldProperty('location')
    kind_of_building = atapi.ATFieldProperty('kindOfBuilding')
    heating = atapi.ATFieldProperty('heating')
    isolation = atapi.ATFieldProperty('isolation')
    balcony = atapi.ATFieldProperty('balcony')
    garden = atapi.ATFieldProperty('garden')
    kind_of_garden = atapi.ATFieldProperty('kindOfGarden')
    storage = atapi.ATFieldProperty('storage')
    garage = atapi.ATFieldProperty('garage')
    kind_of_garage = atapi.ATFieldProperty('kindOfGarage')
    airco = atapi.ATFieldProperty('airco')

    # temporary vocabulary for selectionwidgets in Schemas

    def _get_dummy_vocab(self):
        return ("choice 1", "choice 2", "choice 3")

atapi.registerType(Residential, PROJECTNAME)
