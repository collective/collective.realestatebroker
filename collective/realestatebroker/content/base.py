from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

from Products.CMFCore.utils import getToolByName

def DummyResidentialVocabularyFactory(context):
    """ Dummy Vocabulary Factory for Residential Schema
    """
    return SimpleVocabulary.fromValues(("choice 1","choice 2","choice 3"))
    
def CityVocabularyFactory(context):
    """ Vocabulary Factory for cities in schemata
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    city_props = props.getProperty('city')
    return SimpleVocabulary.fromValues(city_props)
    
def HouseTypeVocabularyFactory(context):
    """ Vocabulary Factory for house type in schemata
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    house_type_props = props.getProperty('house_type')
    return SimpleVocabulary.fromValues(house_type_props)

def RoomsVocabularyFactory(context):
    """ Vocabulary Factory for number of rooms in schemata
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    rooms_props = props.getProperty('rooms')
    return SimpleVocabulary.fromValues(rooms_props)
    
def ResidentialKKVONVocabularyFactory(context):
    """ Vocabulary Factory for KK/VON for the objec in schemata
        KK = Kosten Koper (Dutch) VON = Vrij Op Naam (Dutch)
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    kk_von_props = props.getProperty('residential_kk_von')
    return SimpleVocabulary.fromValues(kk_von_props)
            