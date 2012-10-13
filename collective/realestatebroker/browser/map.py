from Products.Maps.browser.map import BaseMapView
from Products.Maps.interfaces import IMapView
from zope.interface import implements

from collective.realestatebroker.interfaces import IRealEstateContent


class RealEstateMapView(BaseMapView):
    """Configuration adapter for plonemaps."""
    implements(IMapView)

    @property
    def enabled(self):
        req_url = self.request.getURL()
        if not IRealEstateContent.providedBy(self.context):
            return False
        if req_url.endswith('map') or req_url.endswith('edit'):
            return True  # Yes, we want the maps javascript.
        return False
