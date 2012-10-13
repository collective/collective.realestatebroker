import logging

from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from kss.core import kssaction
from plone.app.kss.plonekssview import PloneKSSView
from plone.app.layout.viewlets import ViewletBase
from plone.memoize.view import memoize
from Products.ATContentTypes.interface.image import IATImage

from collective.realestatebroker import REBMessageFactory as _
from collective.realestatebroker import utils
from collective.realestatebroker.adapters.interfaces import IFloorInfo


logger = logging.getLogger('album')


class AlbumView(BrowserView):
    """View class to show the photo album"""

    @memoize
    def image_brains(self, all=False):
        """Grab the brains of all images inside the object.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        if all:
            # Just show all images
            brains = catalog(object_provides=IATImage.__identifier__,
                             sort_on='getObjPositionInParent',
                             path='/'.join(self.context.getPhysicalPath()))
        else:
            # Filter out floorplans
            brains = catalog(object_provides=IATImage.__identifier__,
                             sort_on='getObjPositionInParent',
                             is_floorplan=False,
                             path='/'.join(self.context.getPhysicalPath()))
        return brains

    @memoize
    def image_tag(self, obj, **kwargs):
        """ Return the image tag for a given object
        """
        return obj.getField('image').tag(obj, **kwargs)

    @memoize
    def image_brain_tag(self, brain, scale=None):
        """ Return the image tag for a given object
        """
        assert scale != None
        url = u'%s/image_%s' % (brain.getURL(), scale)
        title = brain.Title
        tag = u'<img src="%s" alt="%s" />' % (url, title)
        return tag

    @memoize
    def image_info(self, image, **kwargs):
        """ This method expects an ATImage object as the first argument.
            It returns a dict with the followin information:
              - title
              - tag
            scale can be passed in as a kwarg to use image sizes from
            ATCT Image.
        """
        return dict(title = image.Title(),
                    tag = self.image_tag(image, **kwargs))

    @memoize
    def image_brain_info(self, brain, scale=None):
        """ This method expects an ATImage brain as the first argument.
            It returns a dict with the followin information:
              - title
              - tag
            scale can be passed in as a kwarg to use image sizes from
            ATCT Image.
        """
        assert scale != None
        return dict(title = brain.Title,
                    tag = self.image_brain_tag(brain, scale))

    @memoize
    def first_image(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        if not 'scale' in kwargs:
            raise RuntimeError('No scale for first image specified')
        brains = self.image_brains()
        if brains:
            return self.image_brain_info(brains[0], kwargs['scale'])

    @memoize
    def photo_batch(self):
        """Return batched photos."""
        brains = self.image_brains()
        selected = int(self.context.request.get('selected', 0))
        batch = utils.batch(brains, selected=selected)
        if not batch:
            return
        batch['selected_tag'] = self.image_brain_tag(batch['selected'],
                                                     scale='large')
        base_url = self.context.absolute_url() + '/album?selected='
        for item in batch['items']:
            image_brain = item['item']
            image_info = self.image_brain_info(image_brain, scale='tile')
            item.update(image_info)
            item['url'] = base_url + str(item['index'])
            item['class'] = 'kssPhotoChange kssattr-item-' + str(item['index'])
        for direction in ['forward', 'reverse', 'fastforward', 'fastreverse']:
            if batch[direction] == None:
                continue
            nxt = batch[direction]
            batch[direction] = base_url + str(nxt)
            batch_class = 'kssPhotoChange kssattr-item-' + str(nxt)
            if direction == 'fastreverse':
                batch['fr_class'] = batch_class + ' reb-nav-reverse'
            if direction == 'fastforward':
                batch['ff_class'] = batch_class + ' reb-nav-forward'
        return batch

    @memoize
    def photos_for_pdf(self):
        """Return list for displaying photos

        Return a list like this:

        [{'floorname': '1st floor', 'photos': ['obj1', 'obj2']}]

        Make sure to filter out floors that don't have any photos.

        """
        floors = {}
        pprops = getToolByName(self.context, 'portal_properties')
        properties = pprops.realestatebroker_properties
        names = list(properties.getProperty('floor_names'))
        if not names:
            return
        for name in names:
            floors[name] = []
        # Grab photos.
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(object_provides=IATImage.__identifier__,
                         is_floorplan=False,
                         sort_on='getObjPositionInParent',
                         path='/'.join(self.context.getPhysicalPath()))
        used_floors = []
        for brain in brains:
            obj = brain.getObject()
            floor = IFloorInfo(obj).floor
            used_floors.append(floor)
            if not floor in floors:
                # List of floors changed, we still have an old one.
                # Or we have a None here: unassigned photos.
                floors[floor] = []
            floors[floor].append(obj)
        # Filter out unused floors
        unused = [name for name in names
                  if name not in used_floors]
        for name in unused:
            del floors[name]
        # Now pack 'em up in a list: in the right order.
        result = []
        for name in names:
            if name in floors:
                result.append({'floorname': name,
                               'photos': floors[name]})
        # If there are no assigned photos, show 'em all.
        if result == []:
            if None in floors:
                if len(floors[None]):
                    name = _(u'All photos')
                    result.append({'floorname': name,
                                   'photos': floors[None]})
        return result


class AlbumViewlet(ViewletBase):
    """ Simple viewlet to render the photo ablum"""

    render = ViewPageTemplateFile("templates/photos.pt")

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
        album = self.context.restrictedTraverse('@@realestate_album')
        self.batch = album.photo_batch()


class AlbumKSSView(PloneKSSView):
    """ KSS Server action to update the album"""

    @kssaction
    def refreshAlbum(self, selected=0):
        self.request.form['selected'] = selected
        ksscore = self.getCommandSet('core')
        ksszope = self.getCommandSet('zope')
        selector = ksscore.getHtmlIdSelector('reb-photo-show')
        ksszope.refreshProvider(selector, 'realestatebroker.photomanager')


class AlbumManagementView(BrowserView):
    """ View for managing photos in an album"""

    @memoize
    def floor_names(self):
        pprops = getToolByName(self.context, 'portal_properties')
        props = pprops.realestatebroker_properties
        names = list(props.getProperty('floor_names'))
        return names

    @memoize
    def photo_configuration(self):
        configuration = []
        album = self.context.restrictedTraverse('realestate_album')
        for index, image_brain in enumerate(album.image_brains(all=True)):
            obj = image_brain.getObject()
            floor_info = IFloorInfo(obj)
            image = album.image_brain_info(image_brain, scale='tile')
            image['id'] = image_brain['id']
            image['choices'] = self.floor_names()
            image['floor'] = floor_info.floor
            image['is_floorplan'] = floor_info.is_floorplan
            image['index'] = index
            configuration.append(image)
        return configuration


class HandleAlbumManagement(BrowserView):

    def __call__(self):
        form = self.request.form
        messages = []
        pprops = getToolByName(self.context, 'portal_properties')
        properties = pprops.realestatebroker_properties
        names = list(properties.getProperty('floor_names'))
        first_available_floor = names[0]
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(object_provides=IATImage.__identifier__,
                         sort_on='sortable_title',
                         path='/'.join(self.context.getPhysicalPath()))
        for image_brain in brains:
            image_id = image_brain['id']
            floor = form.get(image_id)
            obj = image_brain.getObject()
            annotation = IFloorInfo(obj)
            existing_floor = annotation.floor
            is_floorplan = bool(image_id in form.get('floorplan', []))
            if is_floorplan and not floor:
                # A floorplan must be attached to a floor.
                floor = first_available_floor
            if floor != existing_floor:
                annotation.floor = floor
                messages.append(_(u"${image} is now attached to ${floor}.",
                                  mapping={'image':
                                           image_id, 'floor': floor}))
            if is_floorplan != annotation.is_floorplan:
                annotation.is_floorplan = is_floorplan
                if is_floorplan:
                    messages.append(_(u"${image} is now marked as floor "
                                      "plan.", mapping={'image': image_id}))
                else:
                    messages.append(_(u"${image} is no longer marked as "
                                      "floorplan.", mapping={'image':
                                                              image_id}))
            obj.reindexObject()
        current_default = brains[0]['id']
        default = form.get('default')
        if default != current_default:
            self.context.moveObjectsToTop(default)
            self.context.plone_utils.reindexOnReorder(self.context)
            messages.append(_(u"${image} is now the default.",
                              mapping={'image': default}))
        for message in messages:
            self.context.plone_utils.addPortalMessage(message)
        response = self.request.response
        here_url = self.context.absolute_url()
        response.redirect(here_url)
