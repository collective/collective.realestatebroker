from Products.Archetypes import atapi

from collective.realestatebroker import REBMessageFactory as _
from Products.Maps.field import LocationWidget
from Products.Maps.field import LocationField


GeneralInfoSchema =  atapi.Schema((
    atapi.StringField('zipCode',
        storage=atapi.AnnotationStorage(),
        schemata=u'default',
        widget = atapi.StringWidget(label = _(u'Zip code'),
                 )
        ),
    atapi.StringField('city',
        storage=atapi.AnnotationStorage(),
        schemata=u'default',
        vocabulary_factory="collective.realestatebroker.city_list",
        widget = atapi.SelectionWidget(label = _(u'City'),
                 )
        ),
    atapi.IntegerField('price',
        storage=atapi.AnnotationStorage(),
        schemata=u'default',
        widget = atapi.IntegerWidget(label = _(u'Price'),
                 description = _(u'Fill in the price without dots or commas.'),
                 size=10,
                 )
        ),
    atapi.StringField('kk_von',
        storage=atapi.AnnotationStorage(),
        schemata=u'default',
        vocabulary_factory="collective.realestatebroker.kk_von_list",
        widget = atapi.SelectionWidget(label = _(u'k.k./v.o.n.'),
                )
        ),
    atapi.TextField('text',
        storage=atapi.AnnotationStorage(),
        schemata=u"default",
        validators = ('isTidyHtmlWithCleanup',),
        default_output_type = 'text/x-html-safe',
        widget = atapi.RichWidget(label = _(u'Body text'),
                 description = _(u'Enter the main description for this object.'),
                 rows = 25,
                 allow_file_upload = False,
                 )
        ),
    atapi.StringField('acceptance',
        storage=atapi.AnnotationStorage(),
        schemata=u"default",
        widget = atapi.StringWidget(label = _(u'Acceptance'),
                 description = _(u'Enter a brief description for the acceptance.'),
                 )
        ),


    ))

ResidentialGeneralInfoSchema =  atapi.Schema((
    atapi.StringField('house_type',
        storage=atapi.AnnotationStorage(),
        schemata=u'default',
        vocabulary_factory="collective.realestatebroker.house_type_list",
        widget = atapi.SelectionWidget(label = _(u'House type'),
                 format = 'radio',
                 )
        ),
    atapi.StringField('rooms',
        storage=atapi.AnnotationStorage(),
        schemata=u'default',
        vocabulary_factory="collective.realestatebroker.rooms_list",
        widget = atapi.SelectionWidget(label = _(u'Number of rooms'),
                 format = 'select',
                 )
        ),
    ))

CommercialGeneralInfoSchema =  atapi.Schema((
    atapi.StringField('commercial_type',
        storage=atapi.AnnotationStorage(),
        schemata=u'default',
        vocabulary_factory="collective.realestatebroker.commercial_type_list",
        widget = atapi.SelectionWidget(label = _(u'Building type'),
                 format = 'radio',
                 )
        ),
    atapi.StringField('vat',
        storage=atapi.AnnotationStorage(),
        schemata=u'default',
        vocabulary_factory="collective.realestatebroker.vat_list",
        widget = atapi.SelectionWidget(label = _(u'VAT'),
                 )
        ),
    atapi.StringField('rent_buy',
        storage=atapi.AnnotationStorage(),
        schemata=u'default',
        vocabulary_factory="collective.realestatebroker.rent_buy_list",
        widget = atapi.SelectionWidget(label = _(u'Rent or buy'),
                 )
        ),
    ))


GeneralCharacteristicsSchema =  atapi.Schema((
    atapi.StringField('area',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        widget = atapi.StringWidget(label = _(u'Ground area'),
                 )
        ),
    atapi.StringField('volume',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        widget = atapi.StringWidget(label = _(u'Volume'),
                 )
        ),
    atapi.StringField('constructYear',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        widget = atapi.StringWidget(label = _(u'Construction year'),
                 maxlength=4,
                 size=4,)
        ),
    atapi.StringField('kindOfBuilding',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        vocabulary_factory="collective.realestatebroker.kind_of_building_list",
        widget = atapi.SelectionWidget(label = _(u'Kind of building'),
                 )
        ),
    atapi.StringField('heating',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        vocabulary_factory="collective.realestatebroker.heating_list",
        widget = atapi.SelectionWidget(label = _(u'heating'),
                 description = _(u'You can choose more than one option'),
                 )
        ),
    atapi.StringField('insulation',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        vocabulary_factory="collective.realestatebroker.insulation_list",
        widget = atapi.MultiSelectionWidget(label = _(u'insulation'),
                 description = _(u'You can choose more than one option'),
                 format='checkbox'),
        ),
    ))

ResidentialCharacteristicsSchema =  atapi.Schema((
    atapi.StringField('location',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        vocabulary_factory='collective.realestatebroker.location_list',
        widget = atapi.InAndOutWidget(label = _(u'location'),
                 description = _(u'Select the available facilities by moving them to the right column.'),
                 )
        ),
    atapi.BooleanField('balcony',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        widget = atapi.BooleanWidget(label = _(u'Balcony'),
                 )
        ),
    atapi.BooleanField('garden',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        widget = atapi.BooleanWidget(label = _(u'Garden'),
                 )
        ),
    atapi.StringField('kindOfGarden',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        vocabulary_factory='collective.realestatebroker.kind_of_garden_list',
        widget = atapi.MultiSelectionWidget(label = _(u'Kind of garden'),
                 description = _(u'You can choose more than one option.'),
                 )
        ),
    atapi.BooleanField('storage',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        widget = atapi.BooleanWidget(label = _(u'Storage'),
                 )
        ),
    atapi.BooleanField('garage',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        widget = atapi.BooleanWidget(label = _(u'Garage'),
                 )
        ),
    atapi.StringField('kindOfGarage',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        vocabulary_factory='collective.realestatebroker.kind_of_garage_list',
        widget = atapi.MultiSelectionWidget(label = _(u'kindOfGarage'),
                 description = _(u'You can choose more than one option.'),
                 )
        ),
    atapi.BooleanField('airco',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        widget = atapi.BooleanWidget(label = _(u'airco'),
                 )
        ),
    ))

CommercialCharacteristicsSchema =  atapi.Schema((
    atapi.BooleanField('parking',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        vocabulary_factory='collective.realestatebroker.parking_list',
        widget = atapi.SelectionWidget(label = _(u'Private car park'),
                 )
        ),
    atapi.StringField('facilities',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        vocabulary_factory='collective.realestatebroker.facilities_list',
        widget = atapi.InAndOutWidget(label = _(u'Facilities'),
                 description = _(u'Select the available facilities by moving them to the right column.'),
                 )
        ),
    ))

MapsSchema =  atapi.Schema((
        LocationField(
            'geolocation',
            languageIndependent = 1,
            schemata=u"Location",
            required=True,
            validators=('isGeoLocation',),
            widget=LocationWidget(
                label='Location',
                label_msgid='label_geolocation',
                description_msgid='help_geolocation',
                i18n_domain='collective.realestatebroker',
            ),
            ),
        ))
