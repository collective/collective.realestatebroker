"""Schema and content type for commercial real estate."""
from Products.Archetypes import atapi
from collective.realestatebroker.config import PROJECTNAME
from collective.realestatebroker.content.schemata import GeneralInfoSchema


class Commercial(atapi.BaseFolder):
    """Folderish content type for commercial real estate."""
    portal_type = "Commercial"
    _at_rename_after_creation = True
    schema = atapi.BaseFolderSchema.copy() + GeneralInfoSchema

    # temporary vocabulary for selectionwidgets in Schemas
    def _get_dummy_vocab(self):
        return ("choice 1", "choice 2", "choice 3")


atapi.registerType(Commercial, PROJECTNAME)
