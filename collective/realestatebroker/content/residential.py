"""Schema and content type for residential real estate."""
from zope.interface import directlyProvides
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from Products.Archetypes import atapi
from collective.realestatebroker import REBMessageFactory as _
from collective.realestatebroker.config import PROJECTNAME
from collective.realestatebroker.content import schemata
from collective.realestatebroker.interfaces import IResidential
from Products.PloneFlashUpload.interfaces import IUploadingCapable
from archetypes.schemaextender.interfaces import IExtensible

ResidentialSchema = (atapi.OrderedBaseFolderSchema.copy() +
                     schemata.GeneralSchema +
                     schemata.ResidentialSpecificSchema
                     )
ResidentialSchema['title'].storage = atapi.AnnotationStorage()
ResidentialSchema['title'].widget.label = _(u'Address')
ResidentialSchema['title'].widget.description = _(u'Fill in the address of this object')
ResidentialSchema['description'].storage = atapi.AnnotationStorage()
ResidentialSchema['description'].schemata = 'default'

# Move text and descriptionfield to put them at the bottom of the default tab
ResidentialSchema.moveField('text',pos='bottom')
ResidentialSchema.moveField('description',before='text')


class Residential(atapi.OrderedBaseFolder):
    """Folderish content type for residential real estate."""
    implements(IResidential, IUploadingCapable, IExtensible)

    portal_type = "Residential"
    _at_rename_after_creation = True
    schema = ResidentialSchema

    address = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    zipcode = atapi.ATFieldProperty('zipCode')
    city = atapi.ATFieldProperty('city')
    price = atapi.ATFieldProperty('price')
    house_type = atapi.ATFieldProperty('house_type')
    rooms = atapi.ATFieldProperty('rooms')
    text = atapi.ATFieldProperty('text')
    acceptance = atapi.ATFieldProperty('acceptance')
    area = atapi.ATFieldProperty('area')
    floor_area = atapi.ATFieldProperty('floor_area')
    volume = atapi.ATFieldProperty('volume')
    construct_year = atapi.ATFieldProperty('constructYear')
    location = atapi.ATFieldProperty('location')
    kind_of_building = atapi.ATFieldProperty('kindOfBuilding')
    heating = atapi.ATFieldProperty('heating')
    insulation = atapi.ATFieldProperty('insulation')
    garden = atapi.ATFieldProperty('garden')
    kind_of_garden = atapi.ATFieldProperty('kindOfGarden')
    storage = atapi.ATFieldProperty('storage')
    kind_of_storage = atapi.ATFieldProperty('kindOfStorage')
    garage = atapi.ATFieldProperty('garage')
    kind_of_garage = atapi.ATFieldProperty('kindOfGarage')

    def exclude_from_nav(self):
        """We don't want real estate to show up in the nav tree.
        """
        return True


atapi.registerType(Residential, PROJECTNAME)
