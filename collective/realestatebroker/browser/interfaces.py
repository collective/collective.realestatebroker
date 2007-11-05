from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager


class IRealEstateListing(Interface):
    """docstring for IRealEstateContent"""

    def sorted_listing():
        """Returns a list of dicts representing an overview of the Residential
        real estate."""

    def get_batched_folder_contents():
        """Return a batched list of dictionaries with the realestate objects
           in the folder"""


class IResidentialListing(IRealEstateListing):
    """View class: returns a Residential listing of 'RealEstate' items"""
    pass


class ICommercialListing(IRealEstateListing):
    """View class: returns a Commercial listing of 'Realestate' items"""
    pass


class IRealEstateView(Interface):
    """A base view for methods that are common for both Commercial and
    Residential items"""

    def cooked_price():
        """Return formatted price"""

    def image_tag():
        """Returns an HTML image tag for the first image found inside
        RealEstateContent, both commercial and residential  """


class IResidentialView(IRealEstateView):
    """This is a view class for presenting the details of a given
       'Residential' object."""

    def details():
        """ Return a dict with all information about a residential real
        estate object."""


class ICommercialView(IRealEstateView):
    """This is a view class which returns all details for a 'Commercial'
    object."""
    pass


class ITabsManager(IViewletManager):
    """ A Viewlet manager that renders a set of tabs for RealEstateContent
    objects."""
    pass


class IRealEstateTitleManager(IViewletManager):
    """ A Viewlet manager that renders the title and address information of
    RealEstateContent objects."""

    def title():
        """Return the title of the RealEstateContent"""

    def zipcode():
        """Return the zipcode of the RealEstateContent"""

    def city():
        """Return the city where the real estate is located"""

    def price():
        """Return a formatted price"""

    def after_price():
        """Extra info regarding the price e.g. tax/sales costs"""


class IPhotoAlbumManager(IViewletManager):
    """ A Viewlet manager that renders the selected photo and navigation"""
    
