"""Schema and content type for residential real estate."""
from Products.Archetypes import atapi
from collective.realestatebroker.config import PROJECTNAME


class Residential(atapi.BaseFolder):
    """Folderish content type for residential real estate."""
    portal_type = "Residential"
    _at_rename_after_creation = True


atapi.registerType(Residential, PROJECTNAME)
