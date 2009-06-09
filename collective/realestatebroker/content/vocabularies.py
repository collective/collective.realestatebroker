from zope.schema.vocabulary import SimpleVocabulary

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
#from collective.realestatebroker import REBMessageFactory as _


def unicode_vocabulary(proplist):
    #return a Vocabulary with valid ascii Token and unicode Title and Value
    return [SimpleVocabulary.createTerm(
         safe_unicode(i),
         safe_unicode(i).encode('ascii', 'replace'),
         safe_unicode(i)) for i in proplist]


def CityVocabularyFactory(context):
    """ Vocabulary Factory for cities in schemata
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    city_props = props.getProperty('city')
    return unicode_vocabulary(city_props)


def HouseTypeVocabularyFactory(context):
    """ Vocabulary Factory for house type in schemata
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    house_type_props = props.getProperty('residential_house_type')
    return unicode_vocabulary(house_type_props)


def CommercialTypeVocabularyFactory(context):
    """ Vocabulary Factory for house type in schemata
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    commercial_type_props = props.getProperty('commercial_type')
    return unicode_vocabulary(commercial_type_props)


def RoomsVocabularyFactory(context):
    """ Vocabulary Factory for number of rooms in schemata
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    rooms_props = props.getProperty('residential_rooms')
    return unicode_vocabulary(rooms_props)


def KKVONVocabularyFactory(context):
    """ Vocabulary Factory for KK/VON for the objec in schemata
        KK = Kosten Koper (Dutch) VON = Vrij Op Naam (Dutch)
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    kk_von_props = props.getProperty('kk_von')
    return unicode_vocabulary(kk_von_props)


def LocationVocabularyFactory(context):
    """ Location of property
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    location_props = props.getProperty('location')
    return unicode_vocabulary(location_props)


def KindOfBuildingVocabularyFactory(context):
    """ Type of Building property
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    kind_of_building_props = props.getProperty('kindOfBuilding')
    return unicode_vocabulary(kind_of_building_props)


def HeatingVocabularyFactory(context):
    """ Heating system installed property
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    heating_props = props.getProperty('heating')
    return unicode_vocabulary(heating_props)


def InsulationVocabularyFactory(context):
    """ Insulation system of property
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    insulation_props = props.getProperty('insulation')
    return unicode_vocabulary(insulation_props)


def KindOfGardenVocabularyFactory(context):
    """ Kind of garden property
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    kind_of_garden_props = props.getProperty('residential_kindOfGarden')
    return unicode_vocabulary(kind_of_garden_props)


def KindOfGarageVocabularyFactory(context):
    """ Type of garage property
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    kind_of_garage_props = props.getProperty('residential_kindOfGarage')
    return unicode_vocabulary(kind_of_garage_props)


def VATVocabularyFactory(context):
    """ VAT taxation property
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    vat_props = props.getProperty('commercial_vat')
    return unicode_vocabulary(vat_props)


def RentBuyVocabularyFactory(context):
    """ To rent, buy or both property
    """
    # Unneeded.
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    rent_buy_props = props.getProperty('commercial_rent_buy')
    return unicode_vocabulary(rent_buy_props)


def ParkingVocabularyFactory(context):
    """ Parking property
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    parking_props = props.getProperty('commercial_parking')
    return unicode_vocabulary(parking_props)


def FacilitiesVocabularyFactory(context):
    """ Available facilities property
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    facilities_props = props.getProperty('commercial_facilities')
    return unicode_vocabulary(facilities_props)


def MinPriceVocabularyFactory(context):
    """ Minimum price for search forms
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    min_price_props = props.getProperty('min_price')
    return unicode_vocabulary(min_price_props)


def MaxPriceVocabularyFactory(context):
    """ Maximum price for search forms
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    max_price_props = props.getProperty('max_price')
    return unicode_vocabulary(max_price_props)


def FixedPriceNegotiableVocabularyFactory(context):
    """ Negotiable price or fixed price for real estate?
    """
    pprops = getToolByName(context, 'portal_properties')
    props = pprops.realestatebroker_properties
    fp_neg_props = props.getProperty('fixedprice_negotiable')
    return unicode_vocabulary(fp_neg_props)
