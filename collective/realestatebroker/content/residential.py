"""Schema and content type for residential real estate."""
from Products.Archetypes import atapi
from collective.realestatebroker.config import PROJECTNAME
from collective.realestatebroker.content import schemata
from collective.realestatebroker.interfaces import IResidential

from zope.interface import directlyProvides
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

ResidentialSchema = (atapi.OrderedBaseFolderSchema.copy() +
                     schemata.GeneralInfoSchema +
                     schemata.ResidentialGeneralInfoSchema +
                     schemata.DescriptionSchema +
                     schemata.GeneralCharacteristicsSchema +
                     schemata.ResidentialCharacteristicsSchema
                     )
ResidentialSchema['title'].storage = atapi.AnnotationStorage()
ResidentialSchema['description'].storage = atapi.AnnotationStorage()


class Residential(atapi.OrderedBaseFolder):
    """Folderish content type for residential real estate."""
    portal_type = "Residential"
    _at_rename_after_creation = True
    schema = ResidentialSchema
    implements(IResidential)

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    address = atapi.ATFieldProperty('address')
    zipCode = atapi.ATFieldProperty('zipCode')
    city = atapi.ATFieldProperty('city')
    price = atapi.ATFieldProperty('price')
    house_type = atapi.ATFieldProperty('house_type')
    rooms = atapi.ATFieldProperty('rooms')
    kk_von = atapi.ATFieldProperty('kk_von')
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
    balcony = atapi.ATFieldProperty('balcony')
    garden = atapi.ATFieldProperty('garden')
    kindOfGarden = atapi.ATFieldProperty('kindOfGarden')
    storage = atapi.ATFieldProperty('storage')
    garage = atapi.ATFieldProperty('garage')
    kindOfGarage = atapi.ATFieldProperty('kindOfGarage')
    airco = atapi.ATFieldProperty('airco')

    # temporary vocabulary for selectionwidgets in Schemas

    def _get_dummy_vocab(self):
        return ("choice 1", "choice 2", "choice 3")

    def CookedPrice(self):
        """Return formatted price"""
        pr = str(self.price)
        elements = []

        if len(pr) > 9:
            elements.append(pr[-12:-9])
        if len(pr) > 6:
            elements.append(pr[-9:-6])
        if len(pr) > 3:
            elements.append(pr[-6:-3])
        elements.append(pr[-3:])
        return '.'.join(elements)



def DummyResidentialVocabularyFactory(context):
    """ Dummy Vocabulary Factory for Residential Schema
    """
    return SimpleVocabulary.fromValues(("choice 1","choice 2","choice 3"))

directlyProvides(DummyResidentialVocabularyFactory, IVocabularyFactory)

atapi.registerType(Residential, PROJECTNAME)
