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
        self.is_selected = self.context_state.view_template_id().endswith('_view')
       
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
        self.is_selected = self.context_state.view_template_id().endswith('_chars')
       
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
        self.is_selected = self.context_state.view_template_id().endswith('_photos')
       
        # Both Residential and Commercial with have a chars alias that point
        # to their own <type>_photos.pt 
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
        self.is_selected = self.context_state.view_template_id().endswith('_map')
       
        # Both Residential and Commercial with have a chars alias that point
        # to their own <type>_map.pt 
        self.map_view = self.context_state.object_url() + '/map'
