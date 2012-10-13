from zope.interface import implements

from interfaces import ICommercialListing
from interfaces import ICommercialView
from base import RealEstateListing
from base import RealEstateView


class CommercialListing(RealEstateListing):
    """Default view for a folder which contains Commercial real estate. This
    view displays a search form and a listing of the search results.
    """

    implements(ICommercialListing)

    pass


class CommercialView(RealEstateView):

    implements(ICommercialView)

    pass
