"""Floor annotation management for images.

Images inside realestate objects should be attached to floors. And be tagged,
if applicable, as floorplan. Both are handled by annotating images: floors
with a textual label, floorplan is yes/no.

Images implement the IATImage interface.  We'll use a mock image that provides
the same interface.

    >>> from Products.ATContentTypes.interface.image import IATImage
    >>> from zope.annotation.interfaces import IAttributeAnnotatable
    >>> from zope.interface import implements
    >>> from persistent import Persistent
    >>> class MockImage(Persistent):
    ...     implements(IATImage, IAttributeAnnotatable)
    >>> IATImage.implementedBy(MockImage)
    True
    >>> IAttributeAnnotatable.implementedBy(MockImage)
    True

Our image can be annotated once we switch on zope's attribute annotatable
mechanism.

    >>> from zope.annotation.attribute import AttributeAnnotations
    >>> from zope import component
    >>> component.provideAdapter(AttributeAnnotations)
    >>> image = MockImage()
    >>> annotation = IAnnotations(image)

We can grab an IFloorInfo adapter that allows us to query and set the floor
info.

    >>> from collective.realestatebroker.adapters.floor import FloorInfo
    >>> from collective.realestatebroker.adapters.interfaces import IFloorInfo

We have to provide the adapter manually, as it is normally handled through
zcml.

    >>> component.provideAdapter(FloorInfo)
    >>> floor_info = IFloorInfo(image)

Our image doesn't have any floor information yet:

    >>> floor_info.floor == None
    True

By default, floorplan is False, also if nothing is set yet.

    >>> floor_info.is_floorplan
    False

We can set it:

    >>> floor_info.floor = '42 floor'
    >>> floor_info.is_floorplan = True

And grab it again:

    >>> floor_info = IFloorInfo(image)
    >>> floor_info.floor
    '42 floor'
    >>> floor_info.is_floorplan
    True

Behind the scenes, the floor info is handled with annotations.

    >>> from zope.annotation.interfaces import IAnnotations
    >>> from collective.realestatebroker.adapters.floor import FLOORKEY
    >>> from collective.realestatebroker.adapters.floor import FLOORPLANKEY
    >>> annotation = IAnnotations(image)
    >>> annotation.get(FLOORKEY)
    '42 floor'
    >>> annotation.get(FLOORPLANKEY)
    True

"""

from zope.annotation.interfaces import IAnnotations
from zope.component import adapts
from zope.interface import implements
from Products.CMFPlone import CatalogTool as catalogtool
from Products.ATContentTypes.interface.image import IATImage
from interfaces import IFloorInfo

FLOORKEY = 'REB_FLOOR'
FLOORPLANKEY = 'REB_FLOORPLAN'


class FloorInfo(object):
    implements(IFloorInfo)
    adapts(IATImage)

    def __init__(self, context):
        self.context = context

    def set_floor(self, floor):
        annotation = IAnnotations(self.context)
        annotation[FLOORKEY] = floor
    def get_floor(self):
        annotation = IAnnotations(self.context)
        return annotation.get(FLOORKEY)
    floor = property(get_floor, set_floor)

    def set_is_floorplan(self, floorplan):
        annotation = IAnnotations(self.context)
        annotation[FLOORPLANKEY] = floorplan
    def get_is_floorplan(self):
        annotation = IAnnotations(self.context)
        return annotation.get(FLOORPLANKEY, False)
    is_floorplan = property(get_is_floorplan, set_is_floorplan)


def is_floorplan(object, portal, **kw):
    adapted = IFloorInfo(object, None)
    if adapted is not None:
        return adapted.is_floorplan
    return False

catalogtool.registerIndexableAttribute('is_floorplan', is_floorplan)
