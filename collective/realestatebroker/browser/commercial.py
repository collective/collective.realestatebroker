from zope.interface import implements
from Acquisition import aq_inner
from plone.memoize.instance import memoize
from interfaces import ICommercialListing
from interfaces import ICommercialView
from base import RealEstateListing
from base import RealEstateView


class CommercialListing(RealEstateListing):
    """Default view for a folder which contains Commercial real estate. This 
    view displays a search form and a listing of the search results.
    """
    
    implements(ICommercialListing)
    
    @memoize
    def sorted_listing(self, count=10):
        """Returns a list of dicts representing an overview of the Commercial
        real estate. 
        """
        context = aq_inner(self.context)
        brains = self.catalog(object_provides='ICommercial',
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

class CommercialView(RealEstateView):
    
    implements(ICommercialView)
    

    @memoize
    def characteristics(self):
        """Return a dict of characteristics which is stored in a DataGridField
        """
        context = aq_inner(self.context)
        grid = context.getCharacteristics()
        results = {}
        for k, v in grid:
            results[k] = v
        return results

    @memoize
    def details(self):
        """Return a dict of characteristics
        """

        context = aq_inner(self.context)
        results = dict(address = context.address,
                       description = context.description,
                       zipcode = context.zipcode ,
                       city = context.city,
                       price = self.cooked_price,
                       commercial_type = context.commercial_type,
                       vat = context.vat,
                       rent_buy = context.rent_buy, 
                       text = context.text,
                       acceptance = context.acceptance,
                       area = context.area,
                       volume = context.volume,
                       constructYear = context.construct_year,
                       location = context.location,
                       kind_of_building = context.kind_of_building,
                       heating = context.heating,
                       insulation = getattr(context,'insulation',''),
                       parking = context.parking,
                       facilities = context.facilities,
                       )
        return results

    @memoize
    def CookedAcceptance(self):
        """Dummy attribute to allow drop-in replacement of Document"""
        return self.getAcceptance()

