"""Floor annotation management for images.

Images inside realestate objects should be attached to floors. Or be labeled
as floor plan. Both are handled by annotating images with a textual label.

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

We can grab an IFloorInfo adapter that allows us to query and set the floor info.

    >>> from collective.realestatebroker.browser.floor import FloorInfo
    >>> from collective.realestatebroker.browser.interfaces import IFloorInfo

We have to provide the adapter manually, as it is normally handled through
zcml.

    >>> component.provideAdapter(FloorInfo)
    >>> floor_info = IFloorInfo(image)

Our image doesn't have any floor information yet:

    >>> floor_info.floor == None
    True

We can set it:

    >>> floor_info.floor = '42 floor'

And grab it again:

    >>> floor_info = IFloorInfo(image)
    >>> floor_info.floor
    '42 floor'

Behind the scenes, the floor info is handled with annotations.

    >>> from zope.annotation.interfaces import IAnnotations
    >>> from collective.realestatebroker.browser.floor import ANNOKEY
    >>> annotation = IAnnotations(image)
    >>> annotation.get(ANNOKEY)
    '42 floor'

"""

from zope.component import adapts
from zope.interface import implements
from Products.ATContentTypes.interface.image import IATImage
from collective.realestatebroker.browser.interfaces import IFloorInfo
from zope.annotation.interfaces import IAnnotations

ANNOKEY = 'REB_FLOOR'


class FloorInfo(object):
    implements(IFloorInfo)
    adapts(IATImage)

    def __init__(self, context):
        self.context = context

    def set_floor(self, floor):
        annotation = IAnnotations(self.context)
        annotation[ANNOKEY] = floor
    def get_floor(self):
        annotation = IAnnotations(self.context)
        return annotation.get(ANNOKEY)
    floor = property(get_floor, set_floor)
