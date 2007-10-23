from Acquisition import aq_inner
from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface.image import IATImage
from plone.memoize.instance import memoize

from interfaces import IRealEstateListing
from interfaces import IRealEstateView

from collective.realestatebroker import utils

class RealEstateListing(BrowserView):
    """Base view for all objects with IRealEstateContent.
    """

    implements(IRealEstateListing)

    def __init__(self, context, request):
        self.catalog = getToolByName(self.context, 'portal_catalog')

    def sorted_listing(self, count):
        """Returns a list of dicts representing an overview of the Commercial
           real estate. Needs to be implemented in subclasses.
        """
        raise NotImplementedError

    def tag(self, **kwargs):
        """Returns a html IMG tag of the firstimage in the folderish
           RealEstate object. Needs to be implemented in subclasses.
        """
        raise NotImplementedError


class RealEstateView(BrowserView):
    """docstring for RealEstateView"""

    implements(IRealEstateView)

    @memoize
    def CookedPrice(self):
        """Return formatted price"""
        pr = str(aq_inner(self.context.price))
        elements = []

        if len(pr) > 9:
            elements.append(pr[-12:-9])
        if len(pr) > 6:
            elements.append(pr[-9:-6])
        if len(pr) > 3:
            elements.append(pr[-6:-3])
        elements.append(pr[-3:])
        return '.'.join(elements)

    @memoize
    def image_tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(object_provides=IATImage.__identifier__,
                         sort_on='sortable_title',
                         path='/'.join(self.context.getPhysicalPath()))
        if brains:
            first_image = brains[0].getObject()
            return first_image.getField('image').tag(first_image, scale='thumb', **kwargs)

    @memoize
    def CookedBody(self):
        """Dummy attribute to allow drop-in replacement of Document"""
        return self.getMainText()

    @memoize
    def photo_batch(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(object_provides=IATImage.__identifier__,
                         sort_on='sortable_title',
                         path='/'.join(self.context.getPhysicalPath()))
        selected = int(self.context.request.get('selected', 0))
        batch = utils.batch(brains, selected=selected)
        if not batch:
            return
        base_url = self.context.absolute_url() + '/photos?selected='
        # Now decorate the bare stuff with what we need.
        selected_brain = batch['selected']
        selected_obj = selected_brain.getObject()
        selected_tag = selected_obj.getField('image').tag(selected_obj)
        batch['selected_tag'] = selected_tag
        for item in batch['items']:
            brain = item['item']
            obj = brain.getObject()
            tag = obj.getField('image').tag(obj, scale='thumb')
            item['tag'] = tag
            item['url'] = base_url + str(item['index'])
        for direction in ['forward', 'reverse', 'fastforward', 'fastreverse']:
            if batch[direction] == None:
                continue
            batch[direction] = base_url + str(batch[direction])
        return batch
