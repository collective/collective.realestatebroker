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


class AlbumView(BrowserView):
    """View class to show the photo album"""

    @memoize
    def image_brains(self):
        """Grab the brains of all images inside the object.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(object_provides=IATImage.__identifier__,
                         sort_on='getObjPositionInParent',
                         path='/'.join(self.context.getPhysicalPath()))
        return brains

    @memoize
    def image_tag(self, obj, **kwargs):
        """ Return the image tag for a given object
        """
        return obj.getField('image').tag(obj, **kwargs)

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
    def first_image(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        brains = self.image_brains()
        if brains:
            return self.image_info(brains[0].getObject(), **kwargs)

    @memoize
    def photo_batch(self):
        """Return batched photos."""
        brains = self.image_brains()
        selected = int(self.context.request.get('selected', 0))
        batch = utils.batch(brains, selected=selected)
        if not batch:
            return
        selected_image = batch['selected'].getObject()
        batch['selected_tag'] = self.image_tag(selected_image, scale='large')
        base_url = self.context.absolute_url() + '/photos?selected='
        for item in batch['items']:
            obj = item['item'].getObject()
            image_info = self.image_info(obj, scale='tile')
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
        for index, image_brain in enumerate(album.image_brains()):
            obj = image_brain.getObject()
            floor_info = IFloorInfo(obj)
            image = album.image_info(obj, scale='tile')
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
            if floor != existing_floor:
                annotation.floor = floor
                messages.append(_(u"${image} is now attached to ${floor}.",
                                  mapping={'image':
                                           image_id, 'floor': floor}))
            is_floorplan = bool(image_id in form.get('floorplan', []))
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
