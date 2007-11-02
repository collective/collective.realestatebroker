from Acquisition import aq_inner
from Products.ATContentTypes.interface.image import IATImage
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from ZTUtils import Batch, make_query
from collective.realestatebroker import utils
from collective.realestatebroker.interfaces import IResidential, ICommercial
from interfaces import IFloorInfo
from interfaces import IRealEstateListing, IRealEstateView
from plone.memoize.view import memoize
from zope.component import getUtility
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from collective.realestatebroker import REBMessageFactory as _

import logging
from pprint import pprint

logger = logging.getLogger('fredtest')

# Image sizes for which we want tags.
SIZES = ['large', 'mini', 'tile', 'icon', 'thumb']
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


class RealEstateListing(BrowserView, BatchedEstateMixin):
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

    def _getItems(self):
        """ Return a list of (filtered) objects in a folder
            Used by BathedEstateMixin and get_batched_folder_contents
            to create a batched sequence and by helper methods to provide
            values to the template for the next and previous items """

        query = {'object_provides':
                 [ICommercial.__identifier__,IResidential.__identifier__],
                 'sort_on':'getObjPositionInParent',
                 'path': '/'.join(self.context.getPhysicalPath()),
                 }

        catalog = getToolByName(self.context, 'portal_catalog')

        form = self.request.form
        search_action = form.get('form.button.submit', False)
        if search_action:
            if 'search_city' in form:
                query['getCity'] = [form['search_city'],]
            if 'min_price' in form and 'max_price' in form:
                # TODO: why no searches with only a min or a max price?
                minprice = int(form['min_price'])
                maxprice = int(form['min_price'])
                # TODO:              ^^^ max?
            logger.info("%s\n" % pprint(query))

        return catalog.queryCatalog(query)

        #return self.context.listFolderContents(contentFilter=folderfilter)

    def get_batched_folder_contents(self):
        """Return a list of dictionaries with the realestate objects
           in the folder
        """


        batch_list = self._getBatchObj()
        result = []
        for brain in batch_list:
            obj = brain.getObject()
            realestate_view = obj.restrictedTraverse('@@realestate')

            image_tag = realestate_view.image_tile()
            cooked_price = realestate_view.CookedPrice()
            result.append({
                'id': brain.id,
                'url': obj.absolute_url(),
                'title':  brain.Title,
                'zipcode': obj.zipcode,
                'city': brain.getCity,
                'description': brain.Description,
                'image_tag': image_tag,
                'cooked_price': cooked_price,
                'review_state': brain.review_state,
                })

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
    def image_tile(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        if self.image_brains():
            first_image = self.image_brains()[0]
            info = self.decorate_image(first_image)
            return info['tag_tile']

    @memoize
    def CookedBody(self):
        """Dummy attribute to allow drop-in replacement of Document"""
        return self.getMainText()

    @memoize
    def photo_batch(self):
        """Return batched photos."""
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
    def floorplans(self):
        """Return dict for displaying floors

        Return a dict like this:

        {'floors': [{'name': 'BG', 'selected': False, 'url': 'aaa'},
                    {'name': '1e', 'selected': True, 'url': 'bbb'}],
         'floorplans': ['&lt;img src=&quot;favicon.ico /&gt;']}

        """
        result = {}
        pprops = getToolByName(self.context, 'portal_properties')
        props = pprops.realestatebroker_properties
        names = list(props.getProperty('floor_names'))
        if not names:
            return
        floors = []
        selected = self.request.form.get('selected', None)
        if not selected:
            selected = names[0]
        base_url = self.context.absolute_url() + '/plans?selected='
        for name in names:
            floor = {}
            floor['name'] = name
            floor['selected'] = (name == selected)
            floor['url'] = base_url + name
            floors.append(floor)
        # Grab floorplans, not fully implemented yet.
        floorplan_brains = [brain for brain in self.image_brains()
                            # if brain.isPlattegrond == True
                            ]
        decorated = [self.decorate_image(brain) for brain in floorplan_brains]
        floorplans = [item['tag_large'] for item in decorated]
        result['floors'] = floors
        result['floorplans'] = floorplans
        return result

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
                                  mapping={'image':
                                           image_id, 'floor': floor}))
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
