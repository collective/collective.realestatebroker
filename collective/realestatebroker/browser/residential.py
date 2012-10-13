""" Browser view classes to render residential real estate content"""
from zope.interface import implements
from base import RealEstateListing
from base import RealEstateView
from interfaces import IResidentialListing
from interfaces import IResidentialView


class ResidentialListing(RealEstateListing):
    """Default view for a folder which contains residential real estate. This
    view displays a search form and a listing of the search results.
    """

    implements(IResidentialListing)

    pass


class ResidentialView(RealEstateView):
    """ Methods which should be available to both types of real estate are
    inherited from RealEstateView.
    """
    implements(IResidentialView)

    pass
