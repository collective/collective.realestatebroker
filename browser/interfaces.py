from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager


class IRealEstateListing(Interface):
    """docstring for IRealEstateContent"""

    def item():
        """Returns a list of brain representing real estate based on search
        results."""

    def batch():
        """Return a batched list of dictionaries with the realestate objects
           in the folder"""


class IResidentialListing(IRealEstateListing):
    """View class: returns a Residential listing of 'RealEstate' items"""


class ICommercialListing(IRealEstateListing):
    """View class: returns a Commercial listing of 'Realestate' items"""


class IRealEstateView(Interface):
    """A base view for methods that are common for both Commercial and
    Residential items"""

    def base_fields():
        """Return list of base fields (those on the first page)."""

    def characteristic_fields():
        """Return list of characteristic schemata/fields."""

    def cooked_price():
        """Return formatted price"""

    def image_tag():
        """Returns an HTML image tag for the first image found inside
        RealEstateContent, both commercial and residential  """


class IResidentialView(IRealEstateView):
    """This is a view class for presenting the details of a given
       'Residential' object."""


class ICommercialView(IRealEstateView):
    """This is a view class which returns all details for a 'Commercial'
    object."""


class IRealEstateActionsManager(IViewletManager):
    """ A Viewlet manager that renders a set of tabs for RealEstateContent
    objects."""


class IRealEstateTitleManager(IViewletManager):
    """ A Viewlet manager that renders the title and address information of
    RealEstateContent objects."""


class IAlbumManager(IViewletManager):
    """ A Viewlet manager that renders the selected photo and navigation"""


class IPdfGenerator(Interface):
    """PDF generator for real estate content."""
    def rml():
        """Render RML for debug purposes."""


class IREBConfigView(Interface):
    """ View to render reb-config.js.pt"""
    def country():
        """Return the country property"""


class IUpdateWorkflowStatesView(Interface):
    """ Marker interface for workflow updater"""
