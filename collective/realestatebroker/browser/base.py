import logging
from pprint import pprint
from Acquisition import aq_inner
from ZTUtils import Batch, make_query
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.ATContentTypes.interface.image import IATImage
from Products.CMFCore.utils import getToolByName
from plone.memoize.view import memoize
from collective.realestatebroker import REBMessageFactory as _
from collective.realestatebroker import utils
from collective.realestatebroker.interfaces import IResidential, ICommercial
from collective.realestatebroker.interfaces import IFloorInfo
from interfaces import IRealEstateListing
from interfaces import IRealEstateView
from viewlets import Photos

SCHEMATA_I18N = {'measurements': _(u'measurements'),
                 'details': _(u'details'),
                 'environment': _(u'environment'),
                 'financial': _(u'financial'),
                 }


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
        if 'form' in self.request:
            form=self.request.form
            if 'city' in form:
                kw['city'] = form['city']
            if 'min_price' in form and 'max_price' in form:
                kw['min_price'] = form['min_price']
                kw['max_price'] = form['max_price']

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
        raise("TODO! thousands_commas not defined!")
        #return length and thousands_commas(length) or ''


class RealEstateListing(BrowserView):
    """Base view for all objects with IRealEstateContent.
    """

    implements(IRealEstateListing)

    def __init__(self, context, request):
        BrowserView.__init__(self, context,request)

        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.wftool = getToolByName(self.context, 'portal_workflow')

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
        for obj in self.context.listFolderContents(
            contentFilter=contentFilter):
            #if obj.portal_type != 'Residential':
            #    continue
            realestate_view = obj.restrictedTraverse('@@realestate')
            image_tag = realestate_view.image_tag()
            result.append({
                'id': obj.getId(),
                'url': obj.absolute_url(),
                'title':  obj.Title(),
                'zipcode': obj.zipcode,
                'city': obj.city,
                'description': obj.Description(),
                'image_tag': image_tag,
                'review_state': self.wftool.getInfoFor(obj,'review_state'),
                })
        return result

    def DottedPrice(self, pr=0):
        # create a price with 10^3 dotted separators and the currency from the properties
        elements = []
        if len(pr) > 9:
            elements.append(pr[-12:-9])
        if len(pr) > 6:
            elements.append(pr[-9:-6])
        if len(pr) > 3:
            elements.append(pr[-6:-3])
        elements.append(pr[-3:])
        
        #get default currency from the properties
        pprops = getToolByName(self.context, 'portal_properties')
        props = pprops.realestatebroker_properties
        currency = str(props.getProperty('currency'))

        return currency + " " + '.'.join(elements)        
            

    def _getItems(self):
        """ Return a list of (filtered) objects in a folder
            Used by get_batched_folder_contents
            to create a batched sequence and by helper methods to provide
            values to the template for the next and previous items """

        query = {'object_provides':
                 [ICommercial.__identifier__,IResidential.__identifier__],
                 'sort_on':'getObjPositionInParent',
                 'path': '/'.join(self.context.getPhysicalPath()),
                 }
                 
        catalog = getToolByName(self.context, 'portal_catalog')

        plone_utils = getToolByName(self.context,'plone_utils')

        form = self.request.form
        search_action = form.get('form.button.submit', False)
        reset_action = form.get('form.button.reset', False)
        if search_action:
            if 'search_city' in form:
                if form['search_city'] != 'Any city':
                    query['getCity'] = [form['search_city'],]
            if 'min_price' in form and 'max_price' in form:
                min_price=int(form['min_price'])
                max_price=int(form['max_price'])
                if min_price < max_price:
                    # range search
                    query['getPrice']={"query": [min_price,max_price], "range": "minmax"} 
                elif (min_price == 0) and (max_price == 0):
                    # do nothing, empty select
                    pass
                elif (min_price > 0) and (max_price == 0):
                    # only minimum price selected, no maximum price
                    query['getPrice']={"query": min_price, "range": "min"} 
                elif (min_price >= max_price):
                    # invalid value
                    plone_utils.addPortalMessage(_(u'Please select a valid price range.'), 'warning')
                else:
                    # should not happen
                    plone_utils.addPortalMessage(_(u'Please select a valid price range. Should not happen'),'warning')
        if reset_action:
            response = self.request.response
            here_url = self.context.absolute_url()
            response.redirect(here_url)
        
        return catalog.queryCatalog(query)

        
    def get_batched_folder_contents(self):
        """Return a list of dictionaries with the realestate objects
           in the folder. Not doing batching at this moment.
        """
        batch = self._getItems()
        result = []
        for brain in batch:
            obj = brain.getObject()
            realestate = obj.restrictedTraverse('@@realestate')
            result.append(dict(id = brain.id,
                url = obj.absolute_url(),
                title = obj.address,
                zipcode = obj.zipcode,
                city = obj.city,
                description = obj.description,
                image = realestate.first_image(scale='tile'),
                cooked_price = realestate.cooked_price,
                review_state = brain.review_state))
        return result

    def available_cities(self):
        """Return list of cities from the city_list vocabulary
           FIXME: more user friendly would be search over the available cities
           from all the available realestate property in this folder
        """
        cities_vocab = getUtility(IVocabularyFactory,
                                  'collective.realestatebroker.city_list')
        return [city.value for city in cities_vocab(None)]


# Couple of field filter functions. Used by RealEstateView.
def is_main_field(field):
    return field.schemata == 'default'


def is_not_selfrendered_field(field):
    if field.getName() in ['title', 'description']:
        # These are not in "our" schema, so we'll hard-code them here.
        return False
    if not hasattr(field, 'selfrendered'):
        return True
    if field.selfrendered:
        # Fields with a 'selfrendered=True' attribute are excluded.
        return False
    else:
        return True


def is_characteristics_field(field):
    return (field.schemata != 'default' and field.schemata != 'metadata')


class RealEstateView(BrowserView):
    """Generic view for viewing one real estate object."""
    implements(IRealEstateView)

    def base_table_field_predicates(self):
        """Return predicates that filter out undesired fields.

        'Undesired' meaning fields that should not be rendered in a default
        table view on the main 'description' page.

        """
        return [is_main_field,
                is_not_selfrendered_field,
                ]

    def chars_table_field_predicates(self):
        """Return predicates that filter out undesired fields.

        'Undesired' meaning fields that should not be rendered in a default
        table view on the characteristics page.

        """
        return [is_characteristics_field,
                is_not_selfrendered_field,
                ]

    @memoize
    def filtered_fields(self, schemata_name, *predicates):
        """Return schemata's fields, filtered for emptyness and selfrendered.

        Empty fields should not be rendered, neither fields that are rendered
        explicitly elsewhere in the template (as indicated by the
        'selfrendered' property on the field.

        """
        schema = self.context.Schema()
        fields = schema.filterFields(schemata=schemata_name,
                                     *predicates)
        filtered = [field for field in fields
                    if field.get(self.context) == False
                    or field.get(self.context)]
        return filtered

    @memoize
    def base_fields(self):
        """Return list of base fields (those on the first page)."""
        return self.filtered_fields('default',
                                    *self.base_table_field_predicates())

    @memoize
    def characteristic_fields(self):
        """Return list of characteristic schemata/fields.
        """
        schemata_ids = ['measurements', 'details', 'environment', 'financial']
        results = []
        for schemata_id in schemata_ids:
            result = {}
            result['title'] = SCHEMATA_I18N.get(schemata_id, schemata_id)
            result['fields'] = self.filtered_fields(
                schemata_id,
                *self.chars_table_field_predicates())
            results.append(result)
        return results
    
    @memoize
    def cooked_price(self):
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

        #get default currency from the properties
        pprops = getToolByName(self.context, 'portal_properties')
        props = pprops.realestatebroker_properties
        currency = str(props.getProperty('currency'))

        return currency + " " + '.'.join(elements)

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
    def image_info(self, image, **kwargs):
        """ This method expects an ATImage object as the first argument.
            It returns a dict with the followin information:
              - title
              - tag
            scale can be passed in as a kwarg to use image sizes from
            ATCT Image.
        """
        annotation = IFloorInfo(image)
        return dict(title = image.Title(),
                    tag = self.image_tag(image, **kwargs))

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

    @memoize
    def floor_names(self):
        pprops = getToolByName(self.context, 'portal_properties')
        props = pprops.realestatebroker_properties
        names = list(props.getProperty('floor_names'))
        return names

    @memoize
    def floorplans(self):
        """Return dict for displaying floors

        Return a dict like this:

        {'floors': [{'name': 'BG', 'selected': False, 'url': 'aaa'},
                    {'name': '1e', 'selected': True, 'url': 'bbb'}],
         'floorplans': ['&lt;img src=&quot;favicon.ico /&gt;']}

        Make sure to filter out floors that don't have any floorplan.

        """
        result = {}
        names = self.floor_names()
        if not names:
            return
        floors = []
        selected = self.request.form.get('selected', None)
        if not selected:
            selected = names[0]
        base_url = self.context.absolute_url() + '/plans?selected='
        # Grab floorplans.
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(object_provides=IATImage.__identifier__,
                         is_floorplan=True,
                         sort_on='getObjPositionInParent',
                         path='/'.join(self.context.getPhysicalPath()))
        used_floors = []
        floorplans = []
        for brain in brains:
            obj = brain.getObject()
            floor = IFloorInfo(obj).floor
            used_floors.append(floor)
            if floor == selected:
                floorplans.append(self.image_tag(obj, scale="large"))
        result['floorplans'] = floorplans
        for name in names:
            floor = {}
            if not name in used_floors:
                continue
            floor['name'] = name
            floor['selected'] = (name == selected)
            floor['url'] = base_url + name
            floors.append(floor)
        result['floors'] = floors
        return result

    @memoize
    def photo_configuration(self):
        configuration = []
        for index, image_brain in enumerate(self.image_brains()):
            obj = image_brain.getObject()
            image = self.image_info(obj, scale='tile')
            image['id'] = image_brain['id']
            image['choices'] = self.floor_names()
            # image['floor'] and image['is_floorplan'] are handled by
            # image_info.
            image['index'] = index
            configuration.append(image)
        return configuration


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
