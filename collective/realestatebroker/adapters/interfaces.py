from zope.interface import Interface
from zope.interface import Attribute

class IFloorInfo(Interface):
    """Interface for getting/setting a floor annotation on an image."""
    floor = Attribute('Floor the image is attached to.')
    is_floorplan = Attribute('Boolean indicating a floorplan.')
