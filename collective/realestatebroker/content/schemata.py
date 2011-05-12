from Products.Archetypes import atapi

from collective.realestatebroker import REBMessageFactory as _
from Products.Maps.field import LocationWidget
from Products.Maps.field import LocationField

# Schemata:
# - default
# - financial
# - measurements
# - details
# - environment
# - location


GeneralSchema =  atapi.Schema((
    # Generic data (common)
    # ---------------------
    atapi.StringField('zipCode',
        storage=atapi.AnnotationStorage(),
        schemata=u'default',
        selfrendered=True, # For REB-specific template rendering.
        widget = atapi.StringWidget(label = _(u'Zip code'),
                 )
        ),
    atapi.StringField('city',
        storage=atapi.AnnotationStorage(),
        schemata=u'default',
        selfrendered=True, # For REB-specific template rendering.
        vocabulary_factory="collective.realestatebroker.city_list",
        widget = atapi.SelectionWidget(label = _(u'City'),
                 )
        ),
    atapi.TextField('text',
        storage=atapi.AnnotationStorage(),
        schemata=u"default",
        validators = ('isTidyHtmlWithCleanup',),
        selfrendered=True, # For REB-specific template rendering.
        default_output_type = 'text/x-html-safe',
        widget = atapi.RichWidget(label = _(u'Body text'),
                 description = _(u'Enter the main description for this object.'),
                 rows = 25,
                 allow_file_upload = False,
                 )
        ),
    atapi.StringField('kindOfBuilding', # 'New' or 'old'.
        storage=atapi.AnnotationStorage(),
        schemata=u"default",
        vocabulary_factory="collective.realestatebroker.kind_of_building_list",
        widget = atapi.SelectionWidget(label = _(u'Kind of building'),
                 )
        ),
    atapi.StringField('constructYear',
        storage=atapi.AnnotationStorage(),
        schemata=u"default",
        widget = atapi.StringWidget(label = _(u'Construction year'),
                 size=9,)
        ),
    # Measurements (common)
    # ---------------------
    atapi.StringField('volume',
        storage=atapi.AnnotationStorage(),
        schemata=u"measurements",
        widget = atapi.StringWidget(label = _(u'Volume'),
                 )
        ),
    atapi.StringField('area',
        storage=atapi.AnnotationStorage(),
        schemata=u"measurements",
        widget = atapi.StringWidget(label = _(u'Ground area'),
                 )
        ),
    atapi.StringField('floorArea',
        storage=atapi.AnnotationStorage(),
        schemata=u"measurements",
        widget = atapi.StringWidget(label = _(u'Floor area'),
                 )
        ),
    # Object details (common)
    # -----------------------
    atapi.StringField('heating',
        storage=atapi.AnnotationStorage(),
        schemata=u"details",
        vocabulary_factory="collective.realestatebroker.heating_list",
        widget = atapi.MultiSelectionWidget(label = _(u'heating'),
                 description = _(u'You can choose more than one option.'),
                 format='checkbox',
                 )
        ),
    atapi.StringField('insulation',
        storage=atapi.AnnotationStorage(),
        schemata=u"details",
        vocabulary_factory="collective.realestatebroker.insulation_list",
        widget = atapi.MultiSelectionWidget(label = _(u'insulation'),
                 description = _(u'You can choose more than one option.'),
                 format='checkbox',
                 )
        ),
    # Environment/garden (common)
    # ---------------------------
    atapi.StringField('location', # NL: ligging
        storage=atapi.AnnotationStorage(),
        schemata=u"environment",
        #vocabulary_factory='collective.realestatebroker.location_list',
        # ^^^ vocabulary removed as a sting is much more expressive.
        widget = atapi.StringWidget(label = _(u'location'),
                 )
        ),
    # Financial data (common)
    # -----------------------
    atapi.IntegerField('price',
        storage=atapi.AnnotationStorage(),
        schemata=u'financial',
        selfrendered=True, # For REB-specific template rendering.
        widget = atapi.IntegerWidget(label = _(u'Price'),
                 description = _(u'Fill in the price without dots or commas.'),
                 size=10,
                 )
        ),
    atapi.StringField('acceptance',
        storage=atapi.AnnotationStorage(),
        schemata=u'financial',
        widget = atapi.StringWidget(label = _(u'Acceptance'),
                 description = _(u'Enter a brief description for the acceptance.'),
                 )
        ),
    atapi.StringField('rent_buy',
        storage=atapi.AnnotationStorage(),
        schemata=u'financial',
        selfrendered=True, # For REB-specific template rendering.
        default_method='default_rent_buy',
        vocabulary_factory="collective.realestatebroker.rent_buy_list",
        widget = atapi.SelectionWidget(label = _(u'Rent or buy'),
                 )
        ),

    atapi.StringField('fixedprice_negotiable',
        storage=atapi.AnnotationStorage(),
        schemata=u'financial',
        default_method='default_fixedprice_negotiable',
        vocabulary_factory="collective.realestatebroker.fixedprice_negotiable_list",
        widget = atapi.SelectionWidget(label = _(u'Negotiable or fixed price'),
                 )
        ),
    # Location (= google maps)
    # -----------------------
    LocationField('geolocation',
                  languageIndependent = 1,
                  schemata=u"location",
                  required=True,
                  validators=('isGeoLocation',),
                  widget=LocationWidget(label='Location',
                                        label_msgid='label_geolocation',
                                        description_msgid='help_geolocation',
                                        i18n_domain='collective.realestatebroker',
                                        ),
                  ),
    ))


ResidentialSpecificSchema =  atapi.Schema((
    # Generic data (residential)
    # --------------------------
    atapi.StringField('house_type',
        storage=atapi.AnnotationStorage(),
        schemata=u'default',
        vocabulary_factory="collective.realestatebroker.house_type_list",
        widget = atapi.SelectionWidget(label = _(u'House type'),
                 format = 'radio',
                 )
        ),
    atapi.BooleanField('garage',
        storage=atapi.AnnotationStorage(),
        schemata=u"default",
        widget = atapi.BooleanWidget(label = _(u'Garage'),
                 )
        ),
    atapi.StringField('kindOfGarage',
        storage=atapi.AnnotationStorage(),
        schemata=u"default",
        #vocabulary_factory='collective.realestatebroker.kind_of_garage_list',
        widget = atapi.StringWidget(label = _(u'kindOfGarage'),
                 )
        ),
    atapi.BooleanField('storage',
        storage=atapi.AnnotationStorage(),
        schemata=u"default",
        widget = atapi.BooleanWidget(label = _(u'Storage'),
                 )
        ),
    atapi.StringField('kindOfStorage',
        storage=atapi.AnnotationStorage(),
        schemata=u"default",
        #vocabulary_factory='collective.realestatebroker.kind_of_storage_list',
        widget = atapi.StringWidget(label = _(u'kindOfStorage'),
                 )
        ),
    # Measurements (residential)
    # --------------------------
    atapi.StringField('rooms',
        storage=atapi.AnnotationStorage(),
        schemata=u'measurements',
        #vocabulary_factory="collective.realestatebroker.rooms_list",
        widget = atapi.StringWidget(label = _(u'Number of rooms'),
                 )
        ),
    # Outside/garden (residential)
    # ----------------------------
    atapi.BooleanField('garden',
        storage=atapi.AnnotationStorage(),
        schemata=u"environment",
        widget = atapi.BooleanWidget(label = _(u'Garden'),
                 )
        ),
    atapi.StringField('kindOfGarden',
        storage=atapi.AnnotationStorage(),
        schemata=u"environment",
        vocabulary_factory='collective.realestatebroker.kind_of_garden_list',
        widget = atapi.MultiSelectionWidget(label = _(u'Kind of garden'),
                 description = _(u'You can choose more than one option.'),
                 format='checkbox',
                 ),
        ),
    ))


CommercialSpecificSchema =  atapi.Schema((
    # Object details (commercial)
    # ---------------------------
    atapi.StringField('commercial_type',
        storage=atapi.AnnotationStorage(),
        schemata=u'details',
        vocabulary_factory="collective.realestatebroker.commercial_type_list",
        widget = atapi.SelectionWidget(label = _(u'Building type'),
                 format = 'radio',
                 )
        ),
    atapi.StringField('facilities',
        storage=atapi.AnnotationStorage(),
        schemata=u"details",
        vocabulary_factory='collective.realestatebroker.facilities_list',
        widget = atapi.InAndOutWidget(label = _(u'Facilities'),
                 description = _(u'Select the available facilities by moving them to the right column.'),
                 )
        ),
    # Financial data (commercial)
    # ---------------------------
    atapi.StringField('vat',
        storage=atapi.AnnotationStorage(),
        schemata=u'default',
        vocabulary_factory="collective.realestatebroker.vat_list",
        widget = atapi.SelectionWidget(label = _(u'VAT'),
                 )
        ),
    # Outside/garden (commercial)
    # ---------------------------
    atapi.BooleanField('parking',
        storage=atapi.AnnotationStorage(),
        schemata=u"environment",
        vocabulary_factory='collective.realestatebroker.parking_list',
        widget = atapi.SelectionWidget(label = _(u'Private car park'),
                 )
        ),
    ))
