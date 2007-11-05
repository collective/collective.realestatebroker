from zope.component import getMultiAdapter

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import ViewletBase
#from collective.realestatebroker import REBMessageFactory as _


class DescriptionTab(ViewletBase):
    """Description tab viewlet for ITabManager viewlet manager."""

    render = ViewPageTemplateFile('templates/description_tab.pt')

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
        url = self.context_state.current_page_url()
        self.is_selected = True
        if (url.endswith('chars') or
            url.endswith('photos') or
            'photos?selected' in url or
            url.endswith('plans') or
            'plans?selected' in url or
            url.endswith('map')):
            self.is_selected = False

        # Both Residential and Commercial with have a description alias that
        # point to their own <type>_description.pt
        self.description_view = self.context_state.object_url() + '/view'


class CharsTab(ViewletBase):
    """Characteristics tab viewlet for ITabManager viewlet manager."""

    render = ViewPageTemplateFile('templates/chars_tab.pt')

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
        self.is_selected = self.context_state.current_page_url().endswith(
            'chars')

        # Both Residential and Commercial with have a chars alias that point
        # to their own <type>_chars.pt
        self.chars_view = self.context_state.object_url() + '/chars'


class PhotosTab(ViewletBase):
    """Photos tab viewlet for ITabManager viewlet manager."""

    render = ViewPageTemplateFile('templates/photos_tab.pt')

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
        url = self.context_state.current_page_url()
        self.is_selected = (url.endswith('photos') or 'photos?selected' in url)
        self.photos_view = self.context_state.object_url() + '/photos'


class FloorplansTab(ViewletBase):
    """Floorplans tab viewlet for ITabManager viewlet manager."""

    render = ViewPageTemplateFile('templates/floorplans_tab.pt')

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
        url = self.context_state.current_page_url()
        self.is_selected = (url.endswith('plans') or
                            'plans?selected' in url)
        self.floorplans_view = self.context_state.object_url() + '/plans'


class MapTab(ViewletBase):
    """Map tab viewlet for ITabManager viewlet manager."""

    render = ViewPageTemplateFile('templates/map_tab.pt')

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
        self.is_selected = self.context_state.current_page_url().endswith(
            'map')

        self.map_view = self.context_state.object_url() + '/map'


class RealEstateTitle(ViewletBase):
    """ Viewlet that renders the title of a real estate object, both
    residential and commercial."""

    render = ViewPageTemplateFile('templates/realestate_title.pt')

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')

    def title(self):
        return self.context.title

#     def zipcode(self):
#         return self.context.zipcode

#     def city(self):
#         return self.context.city

#     def price(self):
#         realestate_view = self.context.restrictedTraverse('@@realestate')
#         return realestate_view.cooked_price()

#     def after_price(self):
#         if hasattr(self.context, 'kk_von'):
#             return self.context.kk_von
#         return ''

    def image(self):
        realestate_view = self.context.restrictedTraverse('@@realestate')
        return realestate_view.first_image(scale='thumb')

class Photos(ViewletBase):
    """ Simple viewlet to render the photo ablum
    """
    render = ViewPageTemplateFile("templates/photos.pt")

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
        realestate = self.context.restrictedTraverse('@@realestate')
        self.batch = realestate.photo_batch()
