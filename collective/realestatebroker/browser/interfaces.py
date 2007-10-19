from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager


class IRealEstateListing(Interface):
    """docstring for IRealEstateContent"""
    def sorted_listing():
        """Returns a list of dicts representing an overview of the Residential
        real estate.
        """
            

class IResidentialListing(IRealEstateListing):
    """ This is a view class which returns a listing of 'Residential' objects.
    """
    pass


class ICommercialListing(IRealEstateListing):
    """ This is a view class which returns a listing of 'Commercial' objects.
    """
    pass


class IRealEstateView(Interface):
    """docstring for IRealEstateView"""
    
    def image_tag():
        """Returns an HTML image tag for the first image found inside
        RealEstateContent, both commercial and residential  
        """


class IResidentialView(IRealEstateView):
    """This is a view class for presenting the details of a given
       'Residential' object.
    """
    
    def details():
        """ Return a dict with all information about a residential real
        estate object.
        """

        
class ICommercialView(IRealEstateView):
    """This is a view class which returns all details for a 'Commercial'
    object.
    """
    pass


class ITabsManager(IViewletManager):
    """ A Viewlet manager that renders a set of tabs for RealEstateContent
    objects.
    """
