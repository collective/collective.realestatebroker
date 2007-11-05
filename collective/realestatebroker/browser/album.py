from plone.app.kss.plonekssview import PloneKSSView
from kss.core import kssaction
from Products.Five.browser import BrowserView
from plone.memoize.view import memoize


class PhotoKSSView(PloneKSSView):

    @kssaction
    def refreshPhotos(self, selected=0):
        self.request.form['selected'] = selected
        ksscore = self.getCommandSet('core')
        ksszope = self.getCommandSet('zope')
        selector = ksscore.getHtmlIdSelector('reb-photo-show')
        ksszope.refreshProvider(selector, 'realestatebroker.photomanager')


class AblumView(BrowserView):
    """docstring for AblumView"""

    @memoize
    def image_tag(self, obj, **kwargs):
        """ Return the image tag for a given object
        """
        return obj.getField('image').tag(obj, **kwargs)

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