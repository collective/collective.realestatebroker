from Products.Maps.interfaces import IMap
from Products.Maps.interfaces import IRichMarker
from Products.Maps.interfaces import IMarker
from Products.Maps.content.Location import GeoLocation
from zope.interface import implements
from collective.realestatebroker import REBMessageFactory as _


class RealEstateMarker(GeoLocation):
    implements(IRichMarker)

    @property
    def title(self):
        return self.context.Title()

    @property
    def description(self):
        return self.context.Description()

    @property
    def layers(self):
        #return self.context.Subject()
        return None

    @property
    def icon(self):
        return self.context.portal_type.lower()

    @property
    def url(self):
        return self.context.absolute_url()

    @property
    def related_items(self):
        return []

    @property
    def contents(self):
        text = self.context.getText(mimetype="text/plain").strip()
        if text:
            return ({'title': _("Info"),
                     'text': self.context.getText()},)


class RealEstateMap(object):
    implements(IMap)

    def __init__(self, context):
        self.context = context

    def getMarkers(self):
        return [IMarker(self.context)]
