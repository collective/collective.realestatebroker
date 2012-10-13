from StringIO import StringIO

from Acquisition import aq_inner
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode, getSiteEncoding
from Products.Five.browser import BrowserView
from collective.realestatebroker import REBMessageFactory as _
from collective.realestatebroker.interfaces import IResidential, ICommercial
from plone.app.content.batching import Batch
from plone.memoize.view import memoize
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.component import getUtility
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.cachedescriptors.property import Lazy

from interfaces import IRealEstateListing
from interfaces import IRealEstateView
from interfaces import IUpdateWorkflowStatesView


SCHEMATA_I18N = {'measurements': _(u'measurements'),
                 'details': _(u'details'),
                 'environment': _(u'environment'),
                 'financial': _(u'financial'),
                 }

ESTATE_LISTING_BATCHSIZE=10


class RealEstateBaseView(BrowserView):
    """Base view with some tools attached"""

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.wftool = getToolByName(self.context, 'portal_workflow')
        pprops = getToolByName(self.context, 'portal_properties')
        self.properties = pprops.realestatebroker_properties
        self.plone_utils = getToolByName(self.context, 'plone_utils')


class RealEstateListing(RealEstateBaseView):
    """Base view for all objects with IRealEstateContent.
    """

    implements(IRealEstateListing)

    _batching_file = 'templates/batching.pt'
    batching = ViewPageTemplateFile(_batching_file)

    def __init__(self, context, request):
        RealEstateBaseView.__init__(self, context, request)

        self.query = dict(object_provides = [ICommercial.__identifier__,
                                             IResidential.__identifier__],
                          sort_on = 'review_state',
                          path = '/'.join(self.context.getPhysicalPath()))

        self.formerror=u""
        form = self.request.form
        reset_action = form.get('form.button.reset', False)

        if not reset_action:
            if 'search_city' in form and form['search_city'] != 'Any city':
                self.query['getCity'] = form['search_city']
            if 'min_price' in form and 'max_price' in form:
                min_price=int(form['min_price'])
                max_price=int(form['max_price'])
                if min_price < max_price:
                    # range search
                    self.query['getPrice'] = {"query": [min_price, max_price],
                                              "range": "minmax"}
                elif min_price == 0 and max_price == 0:
                    # do nothing, empty select
                    pass
                elif min_price > 0 and max_price == 0:
                    # only minimum price selected, no maximum price
                    self.query['getPrice']={"query": min_price, "range": "min"}
                elif min_price >= max_price:
                    # Wrong price range
                    self.formerror=_(u'Please select a valid price range.')
        if reset_action:
            response = self.request.response
            here_url = self.context.absolute_url()
            response.redirect(here_url)

    def dotted_price(self, pr=0):
        # create a price with 10^3 dotted separators and the currency from the
        # properties
        elements = []
        if len(pr) > 9:
            elements.append(pr[-12:-9])
        if len(pr) > 6:
            elements.append(pr[-9:-6])
        if len(pr) > 3:
            elements.append(pr[-6:-3])
        elements.append(pr[-3:])

        #get default currency from the properties
        currency = self.properties.getProperty('currency')

        return currency + " " + '.'.join(elements)

    @Lazy
    def search_filter(self):
        """Construct search filter.

        Only add valid search terms from the request.
        """

        form = self.request.form
        search_filter = {}
        for key in ['search_city', 'min_price', 'max_price']:
            value = form.get(key)
            if value is not None and not value == u'':
                search_filter[key] = value
        # When viewing a Brand, add its path to the filter.
        return search_filter

    @Lazy
    def url(self):
        """Base url, needed by the batching template."""
        url = self.context.absolute_url()
        terms = ["%s=%s" % (key, value) for key, value in
                 self.search_filter.items()]
        extra = '&'.join(terms)
        return url + '?' + extra

    @Lazy
    def pagenumber(self):
        """Page number for batching.
        """
        return int(self.request.get('pagenumber', 1))

    @Lazy
    def batch(self):
        """ Batch of Realestate (brains)"""

        # get all possible workflow states minus the 'new' state
        wfstates = list(self.catalog.uniqueValuesFor('review_state'))
        if 'new' in wfstates:
            wfstates.remove('new')

        # prepare searchResults queries for 'new' objects and all other
        # objects

        query_new = self.query.copy()
        query_others = self.query.copy()
        query_new['review_state'] = 'new'
        query_new['sort_on'] = 'created'
        query_new['sort_order'] = 'reverse'
        query_others['review_state'] = wfstates

        # concatenate new and other objectbrains in one search result
        results = (self.catalog.searchResults(query_new) +
                   self.catalog.searchResults(query_others))

        return Batch(items=results, pagesize=ESTATE_LISTING_BATCHSIZE,
                     pagenumber=self.pagenumber,
                     navlistsize=5)

    @memoize
    def items(self):
        """Return a list of dictionaries with the realestate objects
           in the folder. Not doing batching at this moment.
        """
        result = []

        if self.formerror != u"":
            return result

        batch = self.batch

        for brain in batch:
            obj = brain.getObject()
            album = obj.restrictedTraverse('@@realestate_album')
            realestate = obj.restrictedTraverse('@@realestate')

            rent_buy = obj.getRent_buy()
            result.append(dict(
                id = brain.id,
                url = obj.absolute_url(),
                title = obj.address,
                zipcode = obj.zipcode,
                city = obj.city,
                description = obj.description,
                image = album.first_image(scale='tile96'),
                cooked_price = realestate.cooked_price,
                review_state = brain.review_state,
                rent_buy = rent_buy,
                ))
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
    if field.getName() in ['id', 'title', 'description']:
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

        show_all = self.properties.getProperty(
            'show_all_fields_without_filtering_empty_ones')

        schema = self.context.Schema()
        fields = schema.filterFields(schemata=schemata_name, *predicates)

        filtered = []
        for field in fields:
            value = field.get(self.context)
            if value in ['', ['']]:
                pass
            if value:
                filtered.append(field)
            elif value == False:
                filtered.append(field)
            elif show_all:
                # Despite filtering, show all.
                filtered.append(field)
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
            result['fields'] = self.filtered_fields(schemata_id,
                *self.chars_table_field_predicates())
            if len(result['fields']) > 0:
                result['title'] = SCHEMATA_I18N.get(schemata_id, schemata_id)
            else:
                result['title'] = False
            results.append(result)
        return results

    @memoize
    def cooked_price(self):
        """Return formatted price"""
        pr = unicode(aq_inner(self.context.price))
        elements = []

        if len(pr) > 9:
            elements.append(pr[-12:-9])
        if len(pr) > 6:
            elements.append(pr[-9:-6])
        if len(pr) > 3:
            elements.append(pr[-6:-3])
        elements.append(pr[-3:])

        currency = safe_unicode(self.properties.getProperty('currency'),
                                getSiteEncoding(self.context))

        return currency + u' ' + u'.'.join(elements)


class REBConfigView(RealEstateBaseView):
    """ This view is used to render reb-config.js.pt
    """

    def country(self):
        """ Return the country property"""
        pprops = getToolByName(self.context, 'portal_properties')
        reb_props = pprops.realestatebroker_properties
        return reb_props.getProperty('country', None)


class UpdateWorkflowStatesView(RealEstateBaseView):
    """ The view needs to get called on a daily basis.
    It checks for Real estate in the states new and sold. In case the state
    change is done more than 2 weeks ago we do a transition:

    new -> available
    sold -> offline
    """
    implements(IUpdateWorkflowStatesView)

    def __call__(self, days=14):
        """ perform updates
        """
        wf_tool = getToolByName(self.context, 'portal_workflow')
        new_items = self.catalog(portal_type=['Residential', 'Commercial'],
                                 review_state='new')
        sold_items = self.catalog(portal_type=['Residential', 'Commercial'],
                              review_state='sold')
        out = StringIO()
        for item in new_items:
            obj = item.getObject()
            history = wf_tool.getHistoryOf('realestate_workflow', obj)
            if history[-1]['time'] < (DateTime() - days):
                wf_tool.doActionFor(obj, 'available',
                                    wf_id='realestate_workflow')
                print >> out, "updated transition for %r" % item.id

        for item in sold_items:
            obj = item.getObject()
            history = wf_tool.getHistoryOf('realestate_workflow', obj)
            if history[-1]['time'] < (DateTime() - days):
                wf_tool.doActionFor(obj, 'retract',
                                    wf_id='realestate_workflow')
                print >> out, "updated transition for %r" % item.id
        return out.getvalue()
