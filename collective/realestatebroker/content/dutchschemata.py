"""Example extension to the basic realestatebroker content type schemas.

This isn't a license to wreak this file beyond recognition, as Zest software
uses this for an actual client. It is provided by way of documentation. Note
that it is hooked up in the unit tests, too, to test the extension mechanism.

For quite a number of fields that are specific to the Netherlands, we didn't
bother to add an English translation, btw.

"""
from Products.Archetypes import atapi
from collective.realestatebroker import REBMessageFactory as _


GeneralDutchExtraSchema = atapi.Schema((
    # Generic data
    # ------------
    atapi.StringField(
    'generic_remarks',
    storage=atapi.AnnotationStorage(),
    schemata=u'default',
    widget = atapi.StringWidget(label = _(u'Generic remarks'))
    ),
    # Added: remarks

    # Measurements
    # ------------
    atapi.StringField(
    'measurement_remarks',
    storage=atapi.AnnotationStorage(),
    schemata=u'measurements',
    widget = atapi.StringWidget(label = _(u'Measurement remarks'))
    ),
    # Added: remarks

    # Object details
    # --------------
    atapi.StringField(
    'detail_remarks',
    storage=atapi.AnnotationStorage(),
    schemata=u'details',
    widget = atapi.StringWidget(label = _(u'Object detail remarks'))
    ),
    # Added: remarks

    # Outside/garden
    # --------------
    atapi.StringField(
    'environment_remarks',
    storage=atapi.AnnotationStorage(),
    schemata=u'environment',
    widget = atapi.StringWidget(label = _(u'Environment remarks'))
    ),
    # Added: remarks

    # Financial data
    # -----------------
    atapi.StringField(
    'kk_von',
    storage=atapi.AnnotationStorage(),
    schemata=u'financial',
    vocabulary_factory="collective.realestatebroker.kk_von_list",
    widget = atapi.SelectionWidget(label = u'k.k./v.o.n.')
    ),
    atapi.StringField(
    'financial_remarks',
    storage=atapi.AnnotationStorage(),
    schemata=u'financial',
    widget = atapi.StringWidget(label = _(u'Financial remarks'))
    ),
     # Added: remarks
     )
    )


ResidentialDutchExtraSchema = atapi.Schema(
    (
    # Generic data (only residential)
    # -------------------------------

    # Financial data (only residential)
    # ---------------------------------
    atapi.StringField(
    'ozb_zakelijk',
    storage=atapi.AnnotationStorage(),
    schemata=u'financial',
    widget = atapi.StringWidget(label = u'OZB zakelijk deel',)
    ),

    atapi.StringField(
    'erfpachtsom',
    storage=atapi.AnnotationStorage(),
    schemata=u'financial',
    widget = atapi.StringWidget(
        label = u'Erfpachtsom',
        )
    ),
    atapi.StringField(
    'waterschapslasten',
    storage=atapi.AnnotationStorage(),
    schemata=u'financial',
    widget = atapi.StringWidget(
        label = u'Waterschapslasten',
        )
    ),
    atapi.StringField(
    'rioolrechten',
    storage=atapi.AnnotationStorage(),
    schemata=u'financial',
    widget = atapi.StringWidget(
        label = u'Rioolrechten',
        )
    ),
    atapi.StringField(
    'stookkosten',
    storage=atapi.AnnotationStorage(),
    schemata=u'financial',
    widget = atapi.StringWidget(
        label = u'Stookkosten',
        )
    ),
    atapi.StringField(
    'vve_bijdrage',
    storage=atapi.AnnotationStorage(),
    schemata=u'financial',
    widget = atapi.StringWidget(
        label = u'VvE bijdrage',
        )
    ),
    # Added OZB zakelijk deel
    # Added erfpachtsom
    # Added waterschapslasten
    # Added rioolrechten
    # Added stookkosten
    # Added VvE bijdrage

    # Measurements
    # ------------
    atapi.StringField(
    'livingroom_area',
    storage=atapi.AnnotationStorage(),
    schemata=u'measurements',
    widget = atapi.StringWidget(
        label = _(u'Living room area'),
        )
    ),
    # Added: m^2 of living room.

    # Object details (only residential)
    # ---------------------------------
    atapi.StringField(
    'merk_cv_ketel',
    storage=atapi.AnnotationStorage(),
    schemata=u'details',
    widget = atapi.StringWidget(
        label = u'Merk en bouwjaar C.V.-ketel',
        )
    ),
    atapi.StringField(
    'warm_water',
    storage=atapi.AnnotationStorage(),
    schemata=u'details',
    widget = atapi.StringWidget(
        label = u'Warm water',
        )
    ),
    atapi.BooleanField(
    'cable',
    storage=atapi.AnnotationStorage(),
    schemata=u'details',
    widget = atapi.StringWidget(
        label = _(u'Cable television'),
        )
    ),
    atapi.StringField(
    'maintenance_inside',
    storage=atapi.AnnotationStorage(),
    schemata=u'details',
    widget = atapi.StringWidget(
        label = _(u'Maintenance level inside'),
        )
    ),
    atapi.StringField(
    'maintenance_outside',
    storage=atapi.AnnotationStorage(),
    schemata=u'details',
    widget = atapi.StringWidget(
        label = _(u'Maintenance level outside'),
        )
    ),
    # Added: merk en bouwjaar cv-ketel.
    # Added: warmwater ('c.v.').
    # Added cable.
    # Added "onderhoud binnen".
    # Added "onderhoud buiten".

    # Outside/garden (only residential)
    # ---------------------------------
    atapi.StringField(
    'garden_depth',
    storage=atapi.AnnotationStorage(),
    schemata=u'environment',
    widget = atapi.StringWidget(
        label = _(u'Garden depth'),
        )
    ),
    atapi.StringField(
    'garden_width',
    storage=atapi.AnnotationStorage(),
    schemata=u'environment',
    widget = atapi.StringWidget(
        label = _(u'Garden width'),
        )
    ),
    atapi.StringField(
    'garden_area',
    storage=atapi.AnnotationStorage(),
    schemata=u'environment',
    widget = atapi.StringWidget(
        label = _(u'Garden area'),
        )
    ),
    # Added diepte
    # Added breedte
    # Added oppervlakte
    )
    )


CommercialDutchExtraSchema = atapi.Schema(
    (# Nothing yet.
    )
    )
