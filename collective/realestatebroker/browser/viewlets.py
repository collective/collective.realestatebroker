from Acquisition import aq_inner
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import ViewletBase


class DescriptionTab(ViewletBase):
    """ Viewlet that renders the the description tab with the ITabManager viewlet manager
    """

    render = ViewPageTemplateFile('templates/description_tab.pt')

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
        url = self.context_state.current_page_url()
        self.is_selected = True
        if url.endswith('chars') or \
           url.endswith('photos') or \
           url.endswith('map'):
           self.is_selected = False

        # Both Residential and Commercial with have a description alias that point
        # to their own <type>_description.pt
        self.description_view = self.context_state.object_url() + '/view'


class CharsTab(ViewletBase):
    """ Viewlet that renders the personal data within the employee viewlet manager
    """

    render = ViewPageTemplateFile('templates/chars_tab.pt')

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
        self.is_selected = self.context_state.current_page_url().endswith('chars')

        # Both Residential and Commercial with have a chars alias that point
        # to their own <type>_chars.pt
        self.chars_view = self.context_state.object_url() + '/chars'


class PhotosTab(ViewletBase):
    """ Viewlet that renders the personal data within the employee viewlet manager
    """

    render = ViewPageTemplateFile('templates/photos_tab.pt')

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
        self.is_selected = self.context_state.current_page_url().endswith('photos')

        self.photos_view = self.context_state.object_url() + '/photos'


class MapTab(ViewletBase):
    """ Viewlet that renders the personal data within the employee viewlet manager
    """

    render = ViewPageTemplateFile('templates/map_tab.pt')

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
        self.is_selected = self.context_state.current_page_url().endswith('map')

        self.map_view = self.context_state.object_url() + '/map'


class RealEstateTitle(ViewletBase):
    """ Viewlet that renders the title of a real estate object, both
    residential and commercial.
    """

    render = ViewPageTemplateFile('templates/realestate_title.pt')

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
    def title(self):
        return self.context.title

    def zipcode(self):
        return self.context.zipcode

    def city(self):
        return self.context.city

    def price(self):
        realestate_view = self.context.restrictedTraverse('@@realestate')
        return realestate_view.CookedPrice()

    def after_price(self):
        if hasattr(self.context, 'kk_von'):
            return self.context.kk_von
        return ''

    def image_tag(self):
        realestate_view = self.context.restrictedTraverse('@@realestate')
        return realestate_view.image_tag()
        
        
        
class RealEstateSimpleSearchForm(ViewletBase):
    """ Viewlet that renders the search form above a realestate listing
        (Commercial and Residential)
    """

    render = ViewPageTemplateFile('templates/simple_search_form.pt')
