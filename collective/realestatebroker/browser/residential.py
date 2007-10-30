""" Browser view classes to render residential real estate content"""
from Acquisition import aq_inner
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize
from base import RealEstateListing
from base import RealEstateView
from interfaces import IResidentialListing
from interfaces import IResidentialView
from collective.realestatebroker import REBMessageFactory as _


class ResidentialListing(RealEstateListing):
    """Default view for a folder which contains residential real estate. This
    view displays a search form and a listing of the search results.
    """

    implements(IResidentialListing)

    @memoize
    def sorted_listing(self, count=10):
        """Returns a list of dicts representing an overview of the residential
        real estate.
        """
        context = aq_inner(self.context)
        brains = self.catalog(object_provides='IResidential',
                              sort_on='sortable_title')[:count]
        results = []
        for brain in brains:
            obj = brain.getObject()
            item = dict(
                title=obj.Title(),
                description=obj.Description(),
                thumb_tag=obj.tag(size='thumb'),
                url=obj.absolute_url(),
            )
            results.append(item)

        return results


class ResidentialView(RealEstateView):
    """ Methods which should be available to both types of real estate are
    inherited from RealEstateView.
    """
    implements(IResidentialView)

    pass
