from Acquisition import aq_inner
from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface.image import IATImage
from plone.memoize.instance import memoize

from interfaces import IRealEstateListing
from interfaces import IRealEstateView

from collective.realestatebroker import utils
from collective.realestatebroker.config import FLOORPLANS_ID
import logging
logger = logging.getLogger('realestatebroker')


# Image sizes for which we want tags.
SIZES = ['large', 'mini', 'tile', 'icon', 'thumb']


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
    def image_brains(self):
        """Grab the brains of all images inside the object.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(object_provides=IATImage.__identifier__,
                         sort_on='getObjPositionInParent',
                         path='/'.join(self.context.getPhysicalPath()))
        return brains

    def decorate_image(self, brain):
        item = {}
        obj = brain.getObject()
        for size in SIZES:
            tagname = 'tag_' + size
            item[tagname] = obj.getField('image').tag(obj, scale=size)
        item['url'] = brain.getURL
        item['title'] = brain.Title
        return item

    @memoize
    def image_tag(self):
        """Generate image tag using the api of the ImageField
        """
        if self.image_brains():
            first_image = self.image_brains()[0]
            info = self.decorate_image(first_image)
            return info['tag_thumb']

    @memoize
    def CookedBody(self):
        """Dummy attribute to allow drop-in replacement of Document"""
        return self.getMainText()

    @memoize
    def photo_batch(self):
        brains = self.image_brains()
        selected = int(self.context.request.get('selected', 0))
        batch = utils.batch(brains, selected=selected)
        if not batch:
            return
        base_url = self.context.absolute_url() + '/photos?selected='
        # Now decorate the bare stuff with what we need.
        selected_brain = batch['selected']
        decoration = self.decorate_image(selected_brain)
        selected_tag = decoration['tag_large']
        batch['selected_tag'] = selected_tag
        for item in batch['items']:
            brain = item['item']
            decoration = self.decorate_image(brain)
            item.update(decoration)
            item['url'] = base_url + str(item['index'])
        for direction in ['forward', 'reverse', 'fastforward', 'fastreverse']:
            if batch[direction] == None:
                continue
            batch[direction] = base_url + str(batch[direction])
        return batch

    def _check_floorplans(self):
        if not FLOORPLANS_ID in self.context.objectIds():
            self.context.invokeFactory('FloorInfo',
                                       id=FLOORPLANS_ID,
                                       title='Floor plans')

    @memoize
    def all_floor_info(self):
        """Return list of dicts with floor info (title, desc, photos)."""
        self._check_floorplans()
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(sort_on='getObjPositionInParent',
                         path='/'.join(self.context.getPhysicalPath()))
        floors = []
        current_floor = -1
        for brain in brains:
            if brain.portal_type == 'FloorInfo':
                # A new floor
                current_floor += 1
                floor = {}
                floor['id'] = brain.id
                floor['title'] = brain.Title
                floor['description'] = brain.Description
                floor['photos'] = []
                floors.append(floor)
            elif brain.portal_type == 'Image':
                # A photo
                if current_floor == -1:
                    continue
                floor = floors[current_floor]
                photo = self.decorate_image(brain)
                floor['photos'].append(photo)
            else:
                # The residential or commercial item itself...
                pass
        return floors

    @memoize
    def floor_info(self):
        """Return all_floor_info, but filter out the floor plans."""
        all = self.all_floor_info()
        return [floor for floor in all
                if floor['id'] != FLOORPLANS_ID]

    @memoize
    def floor_plans(self):
        """Return all_floor_info, but only floor plans."""
        all = self.all_floor_info()
        return [floor for floor in all
                if floor['id'] == FLOORPLANS_ID]
