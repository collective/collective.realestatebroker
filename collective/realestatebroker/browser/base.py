from Acquisition import aq_inner
from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface.image import IATImage
from plone.memoize.instance import memoize

from ZTUtils import Batch, make_query
from Products.CMFDefault.utils import Message as _

# from CMFDefault.utils import ViewBase

from interfaces import IRealEstateListing
from interfaces import IRealEstateView
from collective.realestatebroker.browser.interfaces import IFloorInfo
from collective.realestatebroker import REBMessageFactory as _

from collective.realestatebroker import utils

# Image sizes for which we want tags.
SIZES = ['large', 'mini', 'tile', 'icon', 'thumb']


class BatchedEstateMixin(object):
    """Provide helper methods for batching a folder listing.
       To be used with a BrowserView """

    _BATCH_SIZE = 2

    @memoize
    def _getBatchStart(self):
        return self.request.form.get('b_start', 0)

    @memoize
    def _getBatchObj(self):
        b_start = self._getBatchStart()
        items = self._getItems()
        return Batch(items, self._BATCH_SIZE, b_start, orphan=0)


    @memoize
    def _getNavigationURL(self, b_start):
        target = self.request['ACTUAL_URL']
        kw = {}

        kw['b_start'] = b_start

        query = kw and ('?%s' % make_query(kw)) or ''
        return u'%s%s' % (target, query)

    def navigation_previous(self):
        batch_obj = self._getBatchObj().previous
        if batch_obj is None:
            return None

        length = len(batch_obj)
        url = self._getNavigationURL(batch_obj.first)
        if length == 1:
            title = _(u'Previous item')
        else:
            title = _(u'Previous ${count} items', mapping={'count': length})
        return {'title': title, 'url': url}

    @memoize
    def navigation_next(self):
        batch_obj = self._getBatchObj().next
        if batch_obj is None:
            return None

        length = len(batch_obj)
        url = self._getNavigationURL(batch_obj.first)
        if length == 1:
            title = _(u'Next item')
        else:
            title = _(u'Next ${count} items', mapping={'count': length})
        return {'title': title, 'url': url}

    @memoize
    def summary_length(self):
        length = self._getBatchObj().sequence_length
        return length and thousands_commas(length) or ''

class RealEstateListing(BrowserView, BatchedEstateMixin):
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

    def get_folder_contents(self):
        """Return a list of dictionaries with the residential objects
           in the folder
        """
        result = []
        contentFilter = {'portal_type':['Residential','Commercial']}
        for obj in self.context.listFolderContents(contentFilter=contentFilter):
            #if obj.portal_type != 'Residential':
            #    continue
            realestate_view = obj.restrictedTraverse('@@realestate')
            image_tag = realestate_view.image_tag()
            result.append( {
                'id' : obj.getId(),
                'url': obj.absolute_url(),
                'title':  obj.Title(),
                'zipcode': obj.zipcode,
                'city': obj.city,
                'description': obj.Description(),
                'image_tag': image_tag,
                })
        return result

    def _getItems(self):
        """ Return a list of (filtered) objects in a folder 
            Used by BathedEstateMixin and get_batched_folder_contents 
            to create a batched sequence and by helper methods to provide
            values to the template for the next and previous items """

        folderfilter = {'portal_type':['Residential','Commercial']}
        return self.context.listFolderContents(contentFilter=folderfilter)

    def get_batched_folder_contents(self):
        """Return a list of dictionaries with the realestate objects
           in the folder
        """

        result = []
        
        for obj in self._getBatchObj():
            #if obj.portal_type != 'Residential':
            #    continue
            realestate_view = obj.restrictedTraverse('@@realestate')
            image_tag = realestate_view.image_tag()
            result.append( {
                'id' : obj.getId(),
                'url': obj.absolute_url(),
                'title':  obj.Title(),
                'zipcode': obj.zipcode,
                'city': obj.city,
                'description': obj.Description(),
                'image_tag': image_tag,
                })
        return result    
    

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
        for index, image_brain in enumerate(self.image_brains()):
            image = self.decorate_image(image_brain)
            image['id'] = image_brain['id']
            image['choices'] = self.floor_names()
            image_object = image_brain.getObject()
            annotation = IFloorInfo(image_object)
            image['current'] = annotation.floor
            image['index'] = index
            configuration.append(image)
        return configuration

    @memoize
    def configuration_action(self):
        """Return form action for submitting configuration matrix."""
        base = self.context.absolute_url()
        return base + '/@@handle-configuration'

    @memoize
    def flash_upload_action(self):
        """Return form action for uploading flash files."""
        base = self.context.absolute_url()
        return base + '/photo-management'


class HandleConfiguration(BrowserView):

    def __call__(self):
        form = self.request.form
        messages = []
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(object_provides=IATImage.__identifier__,
                         sort_on='sortable_title',
                         path='/'.join(self.context.getPhysicalPath()))
        for image_brain in brains:
            image_id = image_brain['id']
            floor = form.get(image_id)
            image_object = image_brain.getObject()
            annotation = IFloorInfo(image_object)
            existing_floor = annotation.floor
            if floor != existing_floor:
                annotation.floor = floor
                messages.append(_(u"${image} is now attached to ${floor}.",
                                  mapping={'image': image_id, 'floor': floor}))
        default = int(form.get('default'))
        if default > 0:
            # Move image with that index to the top.
            new_default_brain = brains[default]
            new_default_image = new_default_brain.getObject()
            self.context.moveObjectsByDelta(new_default_brain['id'], -default)
            self.context.plone_utils.reindexOnReorder(self.context)
            messages.append(_(u"${image} is now the default.",
                              mapping={'image': new_default_brain['id']}))

        for message in messages:
            self.context.plone_utils.addPortalMessage(message)
        response = self.request.response
        here_url = self.context.absolute_url()
        response.redirect(here_url)
