from Products.Archetypes import atapi

from collective.realestatebroker import RealEstateBrokerMessageFactory as _



GeneralInfoSchema = atapi.Schema((

    atapi.TextField('address',
                index='FieldIndex',
                schemata='General info',
                widget=atapi.StringWidget(label = _(u"label_address", default=u"Address"),
                                description = _(u'desc_address', default=u"Fill in the address of this object"),
                                size = 30,
                                )
                ),

    atapi.TextField('zipCode',
                index='TextIndex',
                schemata='General info',            
                widget=atapi.StringWidget(label = _(u"label_zipCode", default=u"Zip code"),
                                description = _(u"desc_zipCode", default=u"Fill in the zip code of this object"),
                                size = 30,
                                )
                ),
    atapi.TextField('city',
                index='TextIndex',
                schemata='General info',
                vocabulary='_get_dummy_vocab',            
                widget=atapi.SelectionWidget(label = _(u"label_city", default=u"City"),
                            description = _(u"desc_city", default=u"Fill in the city in which this object is located."),
                            size = 30,
                            )
                ),            

    atapi.TextField('price',
                index='FieldIndex',
                schemata='General info',            
                widget=atapi.IntegerWidget(label = _(u"label_price", default=u"Price"),
                            description = _(u"desc_price", default=u"Fill in the price without dots or comma's."),
                            size = 30,
                            )
                ),

    atapi.TextField('kk_von',
                index='TextIndex',
                schemata='General info',
                vocabulary='_get_dummy_vocab',
                widget=atapi.SelectionWidget(label = _(u"label_kk_van",default=u"K.k./V.o.n."),
                            description = _(u"desc_kk_van", default=u"Select the one option."),
                            )
                ),


    atapi.TextField('housetype',
               index='FieldIndex',
               schemata='General info',
               vocabulary='_get_dummy_vocab',
               widget=atapi.SelectionWidget(label = _(u"label_type",default=u"Type"),
                            description = _(u"desc_type", default=u"Select the type object"),
                            )
               ),

    atapi.TextField('rooms',
               index='FieldIndex',
               schemata='General info',
               vocabulary='_get_dummy_vocab',
               widget=atapi.SelectionWidget(label = _(u"label_rooms", default=u"Rooms"),
                            description= _(u"desc_rooms", default=u"Select the number of rooms for this object"),
                            )
               ),
))