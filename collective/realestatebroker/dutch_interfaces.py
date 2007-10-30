"""Example extension to the basic realestatebroker content type interface

This isn't a license to wreak this file beyond recognition, as Zest software
uses this for an actual client. It is provided by way of documentation. Note
that it is hooked up in the unit tests, too, to test the extension mechanism.

For quite a number of fields that are specific to the Netherlands, we didn't
bother to add an English translation, btw.

"""
from zope.interface import Interface
from collective.realestatebroker.interfaces import IResidential
from collective.realestatebroker.interfaces import ICommercial
from collective.realestatebroker import REBMessageFactory as _


class IDutchExtraRealEstateContent(Interface):
    """Extra fields for Dutch real estate."""
    # Generic data
    # ------------

    # Measurements
    # ------------
    # Missing: remarks

    # Object details
    # --------------
    # Missing: remarks

    # Outside/garden
    # --------------
    # Missing: remarks

    # Financial data
    # -----------------
    kk_von = schema.TextLine(
        title = _(u'k.k./v.o.n.'),
        )
    # Missing: remarks



class IDutchResidential(IResidential, IDutchExtraRealEstateContent):
    # Generic data (only residential)
    # -------------------------------

    # Measurements
    # ------------
    livingroom_area = schema.TextLine(
        title = _(u'Living room area'),
        )
    # Added: m^2 of living room.

    # Object details (only residential)
    # ---------------------------------
    merk_cv_ketel = schema.TextLine(
        title = u'Merk en bouwjaar C.V.-ketel',
        )
    warm_water = schema.TextLine(
        title = u'Warm water',
        )
    cable = schema.Bool(
        title = _(u'Cable television'),
        )
    maintenance_inside = schema.TextLine(
        title = _(u'Maintenance level inside'),
        )
    maintenance_outside = schema.TextLine(
        title = _(u'Maintenance level outside'),
        )
    # Added: merk en bouwjaar cv-ketel.
    # Added: warmwater ('c.v.').
    # Added cable.
    # Added "onderhoud binnen".
    # Added "onderhoud buiten".

    # Outside/garden (only residential)
    # ---------------------------------
    garden_depth = schema.TextLine(
        title = _(u'Garden depth'),
        )
    garden_width = schema.TextLine(
        title = _(u'Garden width'),
        )
    garden_area = schema.TextLine(
        title = _(u'Garden area'),
        )
    # Added diepte
    # Added breedte
    # Added oppervlakte

    # Financial data (only residential)
    # ---------------------------------
    ozb_zakelijk = schema.TextLine(
        title = u'OZB zakelijk deel',
        )
    erfpachtsom = schema.TextLine(
        title = u'Erfpachtsom',
        )
    waterschapslasten = schema.TextLine(
        title = u'Waterschapslasten',
        )
    rioolrechten = schema.TextLine(
        title = u'Rioolrechten',
        )
    stookkosten = schema.TextLine(
        title = u'Stookkosten',
        )
    vve_bijdrage = schema.TextLine(
        title = u'VvE bijdrage',
        )
    # Added OZB zakelijk deel
    # Added erfpachtsom
    # Added waterschapslasten
    # Added rioolrechten
    # Added stookkosten
    # Added VvE bijdrage


class IDutchCommercial(ICommercial, IDutchExtraRealEstateContent):
    pass
