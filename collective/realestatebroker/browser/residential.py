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
    def sorted_listing(self, count):
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

    @memoize
    def details(self):
        """Return a dict of characteristics
        """
        if self.context.kk_von:
            kk_von = _(u'label_kk', default=u'Excluding costs for buyer')
        else:
            kk_von = _(u'label_von', default=u'All costs included')
        context = aq_inner(self.context)
        results = dict(address = context.address,
                       description = context.description,
                       zipcode = context.zipcode ,
                       city = context.city,
                       price = self.CookedPrice,
                       house_type = context.house_type,
                       rooms = context.rooms,
                       kk_von = kk_von,
                       text = context.text,
                       acceptance = context.acceptance,
                       area = context.area,
                       volume = context.volume,
                       constructYear = context.construct_year,
                       location = context.location,
                       kind_of_building = context.kind_of_building,
                       heating = context.heating,
                       isolation = context.isolation,
                       balcony = context.balcony,
                       garden = context.garden,
                       kind_of_garden = context.kind_of_garden,
                       storage = context.storage,
                       garage = context.garage,
                       kind_of_garage = context.kind_of_garage,
                       airco = context.airco,
                       )
        return results

    @memoize
    def CookedAcceptance(self):
        """Dummy attribute to allow drop-in replacement of Document"""
        return self.getAcceptance()
