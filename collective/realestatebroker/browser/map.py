from Products.Maps.browser.map import BaseMapView
from Products.Maps.interfaces import IMapView
from zope.interface import implements


class RealEstateMapView(BaseMapView):
    """Configuration adapter for plonemaps."""
    implements(IMapView)
    enabled = True # Yes, we want the maps javascript.
