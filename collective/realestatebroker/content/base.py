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

def CommercialTypeVocabularyFactory(context):
    """ Vocabulary Factory for house type in schemata
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    commercial_type_props = props.getProperty('commercial_type')
    return SimpleVocabulary.fromValues(commercial_type_props)

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

def ResidentialLocationVocabularyFactory(context):
    """ Location of property
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    location_props = props.getProperty('residential_location')
    return SimpleVocabulary.fromValues(location_props)
    
def KindOfBuildingVocabularyFactory(context):
    """ Location of property
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    kind_of_building_props = props.getProperty('kindOfBuilding')
    return SimpleVocabulary.fromValues(kind_of_building_props)  
    
def HeatingVocabularyFactory(context):
    """ Location of property
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    heating_props = props.getProperty('heating')
    return SimpleVocabulary.fromValues(heating_props)      

def InsulationVocabularyFactory(context):
    """ Insulation system of property
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    insulation_props = props.getProperty('insulation')
    return SimpleVocabulary.fromValues(insulation_props)  
    
def ResidentialKindOfGardenVocabularyFactory(context):
    """ Insulation system of property
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    kind_of_garden_props = props.getProperty('residential_kindOfGarden')
    return SimpleVocabulary.fromValues(kind_of_garden_props)
    
    
def ResidentialKindOfGarageVocabularyFactory(context):
    """ Insulation system of property
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    kind_of_garage_props = props.getProperty('residential_kindOfGarage')
    return SimpleVocabulary.fromValues(kind_of_garage_props)               