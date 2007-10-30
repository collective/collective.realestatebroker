"""Example extension to the basic realestatebroker content type schemas.

This isn't a license to wreak this file beyond recognition, as Zest software
uses this for an actual client. It is provided by way of documentation. Note
that it is hooked up in the unit tests, too, to test the extension mechanism.

For quite a number of fields that are specific to the Netherlands, we didn't
bother to add an English translation, btw.

"""
from Products.Archetypes import atapi
from collective.realestatebroker import REBMessageFactory as _
from zope import component
from zope import interface
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from collective.realestatebroker.interfaces import IResidential
from collective.realestatebroker.interfaces import ICommercial
from archetypes.schemaextender.field import ExtensionField

class ExtendedStringField(ExtensionField, atapi.StringField):
    pass


class ExtendedBooleanField(ExtensionField, atapi.BooleanField):
    pass


dutch_extra_fields = [
    # Generic data
    # ------------
    ExtendedStringField(
    'generic_remarks',
    storage=atapi.AnnotationStorage(),
    schemata=u'default',
    widget = atapi.StringWidget(label = _(u'Generic remarks'))
    ),
    # Added: remarks

    # Measurements
    # ------------
    ExtendedStringField(
    'measurement_remarks',
    storage=atapi.AnnotationStorage(),
    schemata=u'measurements',
    widget = atapi.StringWidget(label = _(u'Measurement remarks'))
    ),
    # Added: remarks

    # Object details
    # --------------
    ExtendedStringField(
    'detail_remarks',
    storage=atapi.AnnotationStorage(),
    schemata=u'details',
    widget = atapi.StringWidget(label = _(u'Object detail remarks'))
    ),
    # Added: remarks

    # Outside/garden
    # --------------
    ExtendedStringField(
    'environment_remarks',
    storage=atapi.AnnotationStorage(),
    schemata=u'environment',
    widget = atapi.StringWidget(label = _(u'Environment remarks'))
    ),
    # Added: remarks

    # Financial data
    # -----------------
    ExtendedStringField(
    'kk_von',
    storage=atapi.AnnotationStorage(),
    schemata=u'financial',
    vocabulary_factory="collective.realestatebroker.kk_von_list",
    widget = atapi.SelectionWidget(label = u'k.k./v.o.n.')
    ),
    ExtendedStringField(
    'financial_remarks',
    storage=atapi.AnnotationStorage(),
    schemata=u'financial',
    widget = atapi.StringWidget(label = _(u'Financial remarks'))
    ),
     # Added: remarks
    ]


dutch_extra_residential_fields = [
    # Generic data (only residential)
    # -------------------------------

    # Financial data (only residential)
    # ---------------------------------
    ExtendedStringField(
    'ozb_zakelijk',
    storage=atapi.AnnotationStorage(),
    schemata=u'financial',
    widget = atapi.StringWidget(label = u'OZB zakelijk deel',)
    ),

    ExtendedStringField(
    'erfpachtsom',
    storage=atapi.AnnotationStorage(),
    schemata=u'financial',
    widget = atapi.StringWidget(
        label = u'Erfpachtsom',
        )
    ),
    ExtendedStringField(
    'waterschapslasten',
    storage=atapi.AnnotationStorage(),
    schemata=u'financial',
    widget = atapi.StringWidget(
        label = u'Waterschapslasten',
        )
    ),
    ExtendedStringField(
    'rioolrechten',
    storage=atapi.AnnotationStorage(),
    schemata=u'financial',
    widget = atapi.StringWidget(
        label = u'Rioolrechten',
        )
    ),
    ExtendedStringField(
    'stookkosten',
    storage=atapi.AnnotationStorage(),
    schemata=u'financial',
    widget = atapi.StringWidget(
        label = u'Stookkosten',
        )
    ),
    ExtendedStringField(
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
    ExtendedStringField(
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
    ExtendedStringField(
    'merk_cv_ketel',
    storage=atapi.AnnotationStorage(),
    schemata=u'details',
    widget = atapi.StringWidget(
        label = u'Merk en bouwjaar C.V.-ketel',
        )
    ),
    ExtendedStringField(
    'warm_water',
    storage=atapi.AnnotationStorage(),
    schemata=u'details',
    widget = atapi.StringWidget(
        label = u'Warm water',
        )
    ),
    ExtendedBooleanField(
    'cable',
    storage=atapi.AnnotationStorage(),
    schemata=u'details',
    widget = atapi.StringWidget(
        label = _(u'Cable television'),
        )
    ),
    ExtendedStringField(
    'maintenance_inside',
    storage=atapi.AnnotationStorage(),
    schemata=u'details',
    widget = atapi.StringWidget(
        label = _(u'Maintenance level inside'),
        )
    ),
    ExtendedStringField(
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
    ExtendedStringField(
    'garden_depth',
    storage=atapi.AnnotationStorage(),
    schemata=u'environment',
    widget = atapi.StringWidget(
        label = _(u'Garden depth'),
        )
    ),
    ExtendedStringField(
    'garden_width',
    storage=atapi.AnnotationStorage(),
    schemata=u'environment',
    widget = atapi.StringWidget(
        label = _(u'Garden width'),
        )
    ),
    ExtendedStringField(
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
    ]

dutch_extra_commercial_fields = [
    # Nothing yet
    ]

class BaseSchemaExtender(object):
    interface.implements(IOrderableSchemaExtender)

    _fields = []

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self._fields

    def getOrder(self, original):
        # Possibility to move fields.
        return original


class ResidentialSchemaExtender(BaseSchemaExtender):
    component.adapts(IResidential)

    _fields = dutch_extra_fields + dutch_extra_residential_fields


class CommercialSchemaExtender(BaseSchemaExtender):
    component.adapts(ICommercial)

    _fields = dutch_extra_fields + dutch_extra_commercial_fields
