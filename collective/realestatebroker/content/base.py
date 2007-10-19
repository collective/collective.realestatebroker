from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


def DummyResidentialVocabularyFactory(context):
    """ Dummy Vocabulary Factory for Residential Schema
    """
    return SimpleVocabulary.fromValues(("choice 1","choice 2","choice 3"))
    
def CityVocabularyFactory(context):
    """ Vocabulary Factory for Cities in schemata
    """
    
    props = context.portal_properties.realestatebroker_properties
    city_props = props.getProperty('city')
    return SimpleVocabulary.fromValues(city_props)
    
