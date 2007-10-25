from Acquisition import aq_inner
from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface.image import IATImage
from plone.memoize.instance import memoize

from interfaces import IRealEstateListing
from interfaces import IRealEstateView

from collective.realestatebroker import utils

# Image sizes for which we want tags.
SIZES = ['large', 'mini', 'tile', 'icon', 'thumb']


class RealEstateListing(BrowserView):
    """Base view for all objects with IRealEstateContent.
    """

    implements(IRealEstateListing)

    def __init__(self, context, request):
        BrowserView.__init__(self, context,request)
        
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
                         sort_on='sortable_title',
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
    def image_tag(self, **kwargs):
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

    @memoize
    def floor_names(self):
        pprops = getToolByName(self.context, 'portal_properties')
        props = pprops.realestatebroker_properties
        names = list(props.getProperty('floor_names'))
        extra = props.getProperty('floorplans_title')
        names.append(extra)
        return names

    @memoize
    def photo_configuration(self):
        configuration = []
        for image_brain in self.image_brains():
            image = self.decorate_image(image_brain)
            image['id'] = image_brain['id']
            image['choices'] = self.floor_names()
            configuration.append(image)
        return configuration

    @memoize
    def configuration_action(self):
        """Return form action for submitting configuration matrix."""
        base = self.context.absolute_url()
        return base + '/@@handle-configuration'


class HandleConfiguration(BrowserView):

    def __call__(self):
        form = self.request.form
        result = []
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(object_provides=IATImage.__identifier__,
                         sort_on='sortable_title',
                         path='/'.join(self.context.getPhysicalPath()))
        for image_brain in brains:
            image_id = image_brain['id']
            floor = form.get(image_id)
            if floor:
                result.append('%s in %s' % (image_id, floor))
            else:
                result.append('%s not handled yet' % image_id)

        for message in result:
            self.context.plone_utils.addPortalMessage(message)
        response = self.request.response
        here_url = self.context.absolute_url()
        response.redirect(here_url)
