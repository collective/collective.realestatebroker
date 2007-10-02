"""Schema and content type for residential real estate."""
from Products.Archetypes import atapi
from collective.realestatebroker import PROJECTNAME


class Residential(atapi.BaseFolder):
    """Folderish content type for residential real estate."""


atapi.registerType(Residential, PROJECTNAME)
