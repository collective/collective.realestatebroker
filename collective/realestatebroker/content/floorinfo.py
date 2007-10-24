"""Simple schema and content type for floor info."""
from zope.interface import implements
from Products.Archetypes import atapi
#from collective.realestatebroker import REBMessageFactory as _
from collective.realestatebroker.config import PROJECTNAME
from collective.realestatebroker.interfaces import IFloorInfo

FloorInfoSchema = atapi.BaseSchema.copy()
FloorInfoSchema['title'].storage = atapi.AnnotationStorage()
FloorInfoSchema['description'].storage = atapi.AnnotationStorage()
FloorInfoSchema['description'].schemata = 'default'


class FloorInfo(atapi.BaseContent):
    """Content type for floor info (just title and description).

    It is a separate contenttype so that it ends up in the folder listing.
    Which means we can drag and drop it along with the images.  Which means
    that we can treat the images behind a FloorInfo object as images that
    belong to that floor.  Simple and effective way to handle this.

    """
    implements(IFloorInfo)

    portal_type = "FloorInfo"
    _at_rename_after_creation = True
    schema = FloorInfoSchema


atapi.registerType(FloorInfo, PROJECTNAME)
