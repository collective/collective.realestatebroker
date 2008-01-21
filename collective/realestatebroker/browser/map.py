from Products.Maps.browser.map import BaseMapView
from Products.Maps.interfaces import IMapView
from zope.interface import implements


class RealEstateMapView(BaseMapView):
    """Configuration adapter for plonemaps."""
    implements(IMapView)

    @property
    def enabled(self):
        req_url = self.request.getURL()
        if req_url.endswith('map'):
            return True # Yes, we want the maps javascript.
        return False
