from urllib import unquote

from Acquisition import aq_inner
from zope.component import getMultiAdapter
from Products.CMFCore.ActionInformation import ActionInfo
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets import ViewletBase
from plone.memoize.view import memoize


class RealEstateActionsViewlet(ViewletBase):

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        #self.portal_url = self.portal_state.portal_url()
        # ^^^ For some reason, this line gives a horridly strange
        # attributeerror after an update to plone 3.1.2. As it doesn't seem to
        # be used, I've commented it out. [reinout]
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
        plone_utils = getToolByName(self.context, 'plone_utils')
        self.getIconFor = plone_utils.getIconFor
        self.actions = self.update_actions()

    @memoize
    def update_actions(self):
        """Prepare the real estate tabs working out which tab is selected.
        Used in realestate_actions.pt
        """
        context = aq_inner(self.context)
        context_url = context.absolute_url()
        context_fti = context.getTypeInfo()
        atool = getToolByName(context, 'portal_actions')
        actions = atool.listActions(categories=['realestate'])
        ec = atool._getExprContext(context)
        action_list = [ActionInfo(action, ec) for action in actions]
        tabs = []
        found_selected = False
        fallback_action = None
        request_url = self.request['ACTUAL_URL']
        request_url_path = request_url[len(context_url):]

        if request_url_path.startswith('/'):
            request_url_path = request_url_path[1:]

        idx = 0
        last = len(action_list)-1
        for action in action_list:
            item = {'title'    : action['title'],
                    'id'       : action['id'],
                    'url'      : '',
                    'class'    : '',
                    'selected' : False}
            klass = 'formTab'
            if idx == 0:
                klass += ' firstFormTab'
            if idx == last:
                klass += ' lastFormTab'
            idx += 1
            action_url = action['url'].strip()
            if action_url.startswith('http') or action_url.startswith('javascript'):
                item['url'] = action_url
            else:
                item['url'] = '%s/%s'%(context_url, action_url)
            action_method = item['url'].split('/')[-1]
            # Action method may be a method alias: Attempt to resolve to a template.
            action_method = context_fti.queryMethodID(action_method, default=action_method)
            if action_method:
                request_action = unquote(request_url_path)
                request_action = context_fti.queryMethodID(request_action, default=request_action)
                if action_method == request_action:
                    item['selected'] = True
                    found_selected = True
                    klass += ' selected'
            item['class'] = klass
            current_id = item['id']
            if current_id == 'view':
                fallback_action = item
            tabs.append(item)
        if not found_selected and fallback_action is not None:
            fallback_action['selected'] = True

        return tabs

    render = ViewPageTemplateFile("templates/realestate_actions.pt")


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

    def image(self):
        album = self.context.restrictedTraverse('@@realestate_album')
        return album.first_image(scale='thumb')
