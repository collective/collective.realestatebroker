"""Schema and content type for residential real estate."""
from Products.Archetypes import atapi
from collective.realestatebroker.config import PROJECTNAME
from collective.realestatebroker.content.schemata import GeneralInfoSchema


class Residential(atapi.OrderedBaseFolder):
    """Folderish content type for residential real estate."""
    portal_type = "Residential"
    _at_rename_after_creation = True
    schema = atapi.OrderedBaseFolderSchema.copy() + GeneralInfoSchema

    # temporary vocabulary for selectionwidgets in Schemas
    def _get_dummy_vocab(self):
        return ("choice 1", "choice 2", "choice 3")


atapi.registerType(Residential, PROJECTNAME)
