from Products.Archetypes import atapi

from collective.realestatebroker import RealEstateBrokerMessageFactory as _

GeneralInfoSchema =  atapi.Schema((
    atapi.TextField('address',
        storage=atapi.AnnotationStorage(),
        schemata=u"default",
        widget = atapi.TextAreaWidget(label = _(u'Address'),
                 description = _(u'Fill in the address of this object'),
                 )
        ),
    atapi.StringField('zipCode',
        storage=atapi.AnnotationStorage(),
        schemata=u"default",
        widget = atapi.StringWidget(label = _(u'Zip code'),
                 description = _(u'Fill in the zip code of this object'),
                 )
        ),
    atapi.StringField('city',
        storage=atapi.AnnotationStorage(),
        schemata=u"default",
        widget = atapi.StringWidget(label = _(u'City'),
                 description = _(u'Fill in the city in which this object is located.'),
                 )
        ),
    atapi.IntegerField('price',
        storage=atapi.AnnotationStorage(),
        schemata=u"default",
        widget = atapi.IntegerWidget(label = _(u'Price'),
                 description = _(u'Fill in the price without dots or commas.'),
                 )
        ),
    atapi.StringField('house_type',
        storage=atapi.AnnotationStorage(),
        schemata=u"default",
        widget = atapi.StringWidget(label = _(u'Type'),
                 description = _(u'Select the type object'),
                 )
        ),
    atapi.StringField('rooms',
        storage=atapi.AnnotationStorage(),
        schemata=u"default",
        widget = atapi.StringWidget(label = _(u'Rooms'),
                 description = _(u'Select the number of rooms for this object'),
                 )
        )
    ))

ResidentialGeneralInfoSchema =  atapi.Schema((
    atapi.BooleanField('kk_von',
        storage=atapi.AnnotationStorage(),
        schemata=u"default",
        widget = atapi.BooleanWidget(label = _(u'k.k./v.o.n.'),
                 description = _(u'Select the one option.'),
                 )
        ),
    ))

CommercialGeneralInfoSchema =  atapi.Schema((
    atapi.StringField('vat',
        storage=atapi.AnnotationStorage(),
        schemata=u"default",
        widget = atapi.StringWidget(label = _(u'VAT'),
                 description = _(u'Select the VAT for this object.'),
                 )
        ),
    atapi.BooleanField('rent_buy',
        storage=atapi.AnnotationStorage(),
        schemata=u"default",
        widget = atapi.BooleanWidget(label = _(u'Rent or buy'),
                 description = _(u'Select Rent/buy for this object.'),
                 )
        ),
    ))

DescriptionSchema =  atapi.Schema((
    atapi.TextField('desc',
        storage=atapi.AnnotationStorage(),
        schemata=u"Description",
        widget = atapi.TextAreaWidget(label = _(u'Description'),
                 description = _(u'Enter a short description for this object.'),
                 )
        ),
    atapi.TextField('mainText',
        storage=atapi.AnnotationStorage(),
        schemata=u"Description",
        widget = atapi.TextAreaWidget(label = _(u'Body text'),
                 description = _(u'Enter the main description for this object.'),
                 )
        ),
    atapi.StringField('acceptance',
        storage=atapi.AnnotationStorage(),
        schemata=u"Description",
        widget = atapi.StringWidget(label = _(u'Acceptance'),
                 description = _(u'Enter a brief description for the acceptance.'),
                 )
        ),
    ))

GeneralCharacteristicsSchema =  atapi.Schema((
    atapi.StringField('area',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        widget = atapi.StringWidget(label = _(u'Area'),
                 description = _(u'Fill in the area of the object.'),
                 )
        ),
    atapi.StringField('volume',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        widget = atapi.StringWidget(label = _(u'Volume'),
                 description = _(u'Fill in the volume of this object.'),
                 )
        ),
    atapi.StringField('constructYear',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        widget = atapi.StringWidget(label = _(u'Construction year'),
                 description = _(u'Fill in the year of construction of this object.'),
                 )
        ),
    atapi.StringField('location',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        widget = atapi.StringWidget(label = _(u'location'),
                 description = _(u'Select the location. You can choose more than 1 option.'),
                 )
        ),
    atapi.StringField('kindOfBuilding',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        widget = atapi.StringWidget(label = _(u'Kind of building'),
                 description = _(u'Select what kind of building this is.'),
                 )
        ),
    atapi.StringField('heating',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        widget = atapi.StringWidget(label = _(u'heating'),
                 description = _(u'Select the heating system for this object. You can choose more than 1 option'),
                 )
        ),
    atapi.StringField('isolation',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        widget = atapi.StringWidget(label = _(u'isolation'),
                 description = _(u'Select the kinds of isolation used for this object. You can choose more than 1 option'),
                 )
        ),
    ))

ResidentialCharacteristicsSchema =  atapi.Schema((
    atapi.BooleanField('balcony',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        widget = atapi.BooleanWidget(label = _(u'Balcony'),
                 description = _(u'Select whether this object has a balcony or not.'),
                 )
        ),
    atapi.BooleanField('garden',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        widget = atapi.BooleanWidget(label = _(u'garden'),
                 description = _(u'Select whether this object has a garden or not.'),
                 )
        ),
    atapi.StringField('kindOfGarden',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        widget = atapi.StringWidget(label = _(u'Kind of garden'),
                 description = _(u'Select the kind of garden. You can choose more than one option'),
                 )
        ),
    atapi.BooleanField('storage',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        widget = atapi.BooleanWidget(label = _(u'Storage'),
                 description = _(u'Select whether this object has a storage.'),
                 )
        ),
    atapi.BooleanField('garage',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        widget = atapi.BooleanWidget(label = _(u'Garage'),
                 description = _(u'Select whether this object has a garage or not.'),
                 )
        ),
    atapi.StringField('kindOfGarage',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        widget = atapi.StringWidget(label = _(u'kindOfGarage'),
                 description = _(u'Select the type garage for this object. You can choose more than 1 option'),
                 )
        ),
    atapi.BooleanField('airco',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        widget = atapi.BooleanWidget(label = _(u'airco'),
                 description = _(u'Select whether this object has an airconditioning or not.'),
                 )
        ),
    ))

CommercialCharacteristicsSchema =  atapi.Schema((
    atapi.BooleanField('parking',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        widget = atapi.BooleanWidget(label = _(u'Parking'),
                 description = _(u'Select here if this object has a private car park.'),
                 )
        ),
    atapi.StringField('facilities',
        storage=atapi.AnnotationStorage(),
        schemata=u"Characteristics",
        widget = atapi.StringWidget(label = _(u'Facilities'),
                 description = _(u'Select the facilities. You can choose more than 1 option'),
                 )
        ),
    ))
