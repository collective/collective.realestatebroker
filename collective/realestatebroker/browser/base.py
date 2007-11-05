from Acquisition import aq_inner
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.ATContentTypes.interface.image import IATImage
from plone.memoize.view import memoize
from collective.realestatebroker import REBMessageFactory as _
from collective.realestatebroker.interfaces import IResidential, ICommercial
from collective.realestatebroker.adapters.interfaces import IFloorInfo
from interfaces import IRealEstateListing
from interfaces import IRealEstateView

SCHEMATA_I18N = {'measurements': _(u'measurements'),
                 'details': _(u'details'),
                 'environment': _(u'environment'),
                 'financial': _(u'financial'),
                 }

class RealEstateBaseView(BrowserView):
    """Base view with some tools attached"""
    
    def __init__(self, context, request):
        BrowserView.__init__(self, context,request)
        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.wftool = getToolByName(self.context, 'portal_workflow')
        pprops = getToolByName(self.context, 'portal_properties')
        self.properties = pprops.realestatebroker_properties
        self.plone_utils = getToolByName(self.context,'plone_utils')


class RealEstateListing(RealEstateBaseView):
    """Base view for all objects with IRealEstateContent.
    """

    implements(IRealEstateListing)

    def dotted_price(self, pr=0):
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
        currency = str(self.properties.getProperty('currency'))

        return currency + " " + '.'.join(elements)        
            
    @memoize
    def items(self):
        """ Return a list of (filtered) objects in a folder
            Used by batch
            to create a batched sequence and by helper methods to provide
            values to the template for the next and previous items """

        query = dict(object_provides = [ICommercial.__identifier__,
                                        IResidential.__identifier__],
                     sort_on = 'getObjPositionInParent',
                     path = '/'.join(self.context.getPhysicalPath()))
        form = self.request.form
        search_action = form.get('form.button.submit', False)
        reset_action = form.get('form.button.reset', False)
        if search_action:
            if 'search_city' in form and form['search_city'] != 'Any city':
                query['getCity'] = [form['search_city'],]
            if 'min_price' in form and 'max_price' in form:
                min_price=int(form['min_price'])
                max_price=int(form['max_price'])
                if min_price < max_price:
                    # range search
                    query['getPrice']={"query": [min_price,max_price], "range": "minmax"} 
                elif min_price == 0 and max_price == 0:
                    # do nothing, empty select
                    pass
                elif min_price > 0 and max_price == 0:
                    # only minimum price selected, no maximum price
                    query['getPrice']={"query": min_price, "range": "min"} 
                elif min_price >= max_price:
                    self.plone_utils.addPortalMessage(_(u'Please select a valid price range.'), 'warning')
        if reset_action:
            response = self.request.response
            here_url = self.context.absolute_url()
            response.redirect(here_url)
        
        return self.catalog.queryCatalog(query)

    @memoize
    def batch(self):
        """Return a list of dictionaries with the realestate objects
           in the folder. Not doing batching at this moment.
        """
        items = self.items()
        batch = items # Here we have to slice the items into a batch

        result = []
        for brain in batch:
            obj = brain.getObject()
            album = obj.restrictedTraverse('@@realestate_album')
            realestate = obj.restrictedTraverse('@@realestate')
            result.append(dict(id = brain.id,
                url = obj.absolute_url(),
                title = obj.address,
                zipcode = obj.zipcode,
                city = obj.city,
                description = obj.description,
                image = album.first_image(scale='tile'),
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


class RealEstateView(RealEstateBaseView):
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
        'selfrendered' property on the field."""

        schema = self.context.Schema()
        fields = schema.filterFields(schemata=schemata_name, *predicates)
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
        """Return list of characteristic schemata/fields."""
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

        currency = str(self.properties.getProperty('currency'))

        return currency + " " + '.'.join(elements)


class FloorplansView(RealEstateBaseView):
    """docstring for FloorplansView"""

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
        names = list(self.properties.getProperty('floor_names'))
        if not names:
            return
        floors = []
        selected = self.request.form.get('selected', None)
        if not selected:
            selected = names[0]
        base_url = self.context.absolute_url() + '/plans?selected='
        # Grab floorplans.
        brains = self.catalog(object_provides=IATImage.__identifier__,
                         is_floorplan=True,
                         sort_on='getObjPositionInParent',
                         path='/'.join(self.context.getPhysicalPath()))
        used_floors = []
        floorplans = []
        album = self.context.restrictedTraverse('@@realestate_album')
        for brain in brains:
            obj = brain.getObject()
            floor = IFloorInfo(obj).floor
            used_floors.append(floor)
            if floor == selected:
                floorplans.append(album.image_tag(obj, scale="large"))
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
