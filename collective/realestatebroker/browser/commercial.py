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
    def sorted_listing(self):
        """Returns a list of dicts representing an overview of the Commercial
        real estate. 
        """
        context = aq_inner(self.context)
        brains = self.catalog(object_provides='ICommercial',
                              sort_on='sortable_title')
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

    @memoize
    def tag(self, **kwargs):
        """Returns a html IMG tag of the firstimage in the folderish
           RealEstate object. Needs to be implemented in subclasses. 
        """
        return self.getField('image').tag(self, **kwargs)
                

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

