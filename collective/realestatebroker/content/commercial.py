"""Schema and content type for commercial real estate."""
from Products.Archetypes import atapi
from collective.realestatebroker.config import PROJECTNAME


class Commercial(atapi.BaseFolder):
    """Folderish content type for commercial real estate."""
    portal_type = "Commercial"
    _at_rename_after_creation = True


atapi.registerType(Commercial, PROJECTNAME)
