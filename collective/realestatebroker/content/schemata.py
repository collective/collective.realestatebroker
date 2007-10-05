from Products.Archetypes import atapi

from collective.realestatebroker import RealEstateBrokerMessageFactory as _


GeneralInfoSchema = atapi.Schema((

    atapi.TextField('address',
                    index='FieldIndex',
                    schemata='General info',
                    widget=atapi.StringWidget(label = _(u"label_address", default=u"Address"),
                                              size = 30,
                                              )
                    ),

    atapi.TextField('zipCode',
                    index='TextIndex',
                    schemata='General info',
                    widget=atapi.StringWidget(label = _(u"label_zipCode", default=u"Zip code"),
                                              size = 30,
                                              )
                    ),
    atapi.TextField('city',
                    index='TextIndex',
                    schemata='General info',
                    vocabulary_factory=u"collective.realestatebroker.DummyResidentialList", # uit residential.py
                    widget=atapi.SelectionWidget(label = _(u"label_city", default=u"City"),
                                                 size = 30,
                                                 )
                    ),

    atapi.TextField('price',
                    index='FieldIndex',
                    schemata='General info',
                    widget=atapi.IntegerWidget(label = _(u"label_price", default=u"Price"),
                                               size = 30,
                                               )
                    ),

    atapi.TextField('kk_von',
                    index='TextIndex',
                    schemata='General info',
                    vocabulary_factory=u"collective.realestatebroker.DummyResidentialList", # uit residential.py
                    widget=atapi.SelectionWidget(label = _(u"label_kk_van",default=u"K.k./V.o.n."),
                                                 )
                    ),


    atapi.TextField('housetype',
                    index='FieldIndex',
                    schemata='General info',
                    vocabulary_factory=u"collective.realestatebroker.DummyResidentialList", # uit residential.py
                    widget=atapi.SelectionWidget(label = _(u"label_type",default=u"Type"),
                                                 description = _(u"desc_type", default=u"Select the type object"),
                                                 )
                    ),

    atapi.TextField('rooms',
                    index='FieldIndex',
                    schemata='General info',
                    vocabulary_factory=u"collective.realestatebroker.DummyResidentialList", # uit residential.py
                    widget=atapi.SelectionWidget(label = _(u"label_rooms", default=u"Rooms"),
                                                 )
                    ),
    ))
