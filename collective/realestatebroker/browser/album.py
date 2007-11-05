from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from kss.core import kssaction
from plone.app.kss.plonekssview import PloneKSSView
from plone.app.layout.viewlets import ViewletBase
from plone.memoize.view import memoize
from Products.ATContentTypes.interface.image import IATImage
from collective.realestatebroker import utils


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
