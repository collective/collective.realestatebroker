from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

from Products.CMFCore.utils import getToolByName

def DummyResidentialVocabularyFactory(context):
    """ Dummy Vocabulary Factory for Residential Schema
    """
    return SimpleVocabulary.fromValues(("choice 1","choice 2","choice 3"))
    
def CityVocabularyFactory(context):
    """ Vocabulary Factory for Cities in schemata
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    city_props = props.getProperty('city')
    return SimpleVocabulary.fromValues(city_props)
    

    
    