"""Migration support for the old 1.0 version to 2.0.

We have to accomplish several tasks:

- Replace old REHome/REBusiness objects with Residential/Commercial objects.

- REHome/REBusiness have CMFPhotoAlbums with CMFPhotos in them, these photos
  must be moved directly into the (folderish) Residential/Commercial object as
  regular Images.

- Migrate old workflow states OR old status field to new workflow states.

- Migrate old property sheets to new ones.

- Clean up leftover junk like skin layers and old portal types and two portal
  actions.

- Remove RealEstateBroker/CMFPhoto(Album) from the quickinstaller.

A unittest that tests out the whole migration mechanism can be found in
`tests/migration-unittest.txt`.

"""
import logging
from StringIO import StringIO
from collective.realestatebroker.config import MIGRATIONPRODUCTAVAILABLE

if MIGRATIONPRODUCTAVAILABLE:
   from Products.contentmigration import walker
   from Products.contentmigration.basemigrator.migrator import CMFItemMigrator
   from Products.contentmigration.common import _createObjectByType
from Products.CMFCore.utils import getToolByName

from config import STATE_TRANSITION_MAP

logger = logging.getLogger('rebmigrator')


class RebMigrator(CMFItemMigrator):
    """Base class to migrate objects to a realestatebroker content type.

    In addition to contentmigration's functionality, RebMigrator also converts
    nested CMFPhotos.

    Methods that start with `migrate_` are automatically called after the
    regular contentmigration functionality has created the new product.
    """

    walkerClass = walker.CatalogWalker
    map = {# All the old fields (both REHome and REBusiness)
        'getAcceptance': 'setAcceptance',
        'getAddress': 'setAddress',
        'getAirco': 'setAirco',
        'getArea': 'setArea',
        'getBalcony': 'setBalcony',
        'getCity': 'setCity',
        'getConstructYear': 'setConstructYear',
        'getDesc': 'setDesc',
        'getFacilities': 'setFacilities',
        'getGarden': 'setGarden',
        'getHeating': 'setHeating',
        'getIsolation': 'setIsolation',
        'getKindOfBuilding': 'setKindOfBuilding',
        'getKindOfGarden': 'setKindOfGarden',
        'getKk_von': 'setKk_von',
        'getLocation': 'setLocation',
        'getMainText': 'setText',
        'getParking': 'setParking',
        'getPrice': 'setPrice',
        'getRent_buy': 'setRent_buy',
        'getRooms': 'setRooms',
        'getStorage': 'setStorage',
        'getType': 'setType',
        'getVat': 'setVat',
        'getVolume': 'setVolume',
        'getZipCode': 'setZipCode',

        # End of old fields
        }

    # def beforeChange_* (done before migration)
    # def last_migrate_* (done just before migration finishes)

    def migrate_cmfphotos(self):
        """Migrate nested CMFPhotos to regular ATImages.

        REHome/REBusiness have CMFPhotoAlbums with CMFPhotos in them, these
        photos must be moved directly into the (folderish)
        Residential/Commercial object as regular Images.

        First some setupcode needed for later _createObject stuff.

        >>> import Acquisition
        >>> class MockSomething(Acquisition.Implicit):
        ...     # just to allow us to set values on something.
        ...     pass
        >>> class MockPortalTypes:
        ...     def getTypeInfo(self, typename):
        ...         fti = MockSomething()
        ...         fti.product = typename
        ...         fti.factory = typename
        ...         return fti
        >>> class MockContentType(Acquisition.Implicit, dict):
        ...     #aq_parent = portal
        ...     typename = 'mock'
        ...     id = None
        ...     def __init__(self, id):
        ...         self.id = id
        ...     def getTypeInfo(self):
        ...         fti = MockSomething()
        ...         fti.product = self.typename
        ...         fti.factory = self.typename
        ...         return fti
        ...     def __getattr__(self, id):
        ...         return self[id]
        ...     def _getOb(self, id):
        ...         return self[id]
        ...     def objectValues(self):
        ...         return self.values()
        ...     def objectIds(self):
        ...         return self.keys()
        ...     def getId(self):
        ...         return self.id
        ...     def Title(self):
        ...         return self.title
        ...     def Description(self):
        ...         return self.description
        ...     def setTitle(self, title):
        ...         self.title = title
        ...     def setDescription(self, description):
        ...         self.description = description
        ...     def setImage(self, value):
        ...         self['data'] = value
        >>> class MockMigrator(RebMigrator):
        ...     def __init__(self):
        ...         # just to quiet down the init.
        ...         pass
        >>> migrator = MockMigrator()

        Now the actual work. An empty old object, so nothing happens.

        >>> migrator.old = MockContentType('dummy')
        >>> migrator.migrate_cmfphotos()

        If something has a different content type, leave it alone.

        >>> something_else = MockContentType('dummy')
        >>> something_else.portal_type = 'Something else'
        >>> migrator.old['something'] = something_else
        >>> migrator.migrate_cmfphotos()

        >>> album = MockContentType('dummy')
        >>> album.portal_type = 'Photo Album'
        >>> migrator.old['photos'] = album
        >>> migrator.migrate_cmfphotos()

        We'll fill the album with a dummy photo. The album can be accessed as
        a dict.

        >>> class MockPhoto:
        ...     data = str('simple string, no unicode')
        ...     def __init__(self, id):
        ...         self.id = id
        ...     def getId(self):
        ...         return self.id
        ...     def Format(self):
        ...         return 'image/mock'
        ...     def Title(self):
        ...         return 'dummy photo title'
        ...     def Description(self):
        ...         return 'dummy photo description'
        >>> dummy_photo = MockPhoto('photo1')
        >>> album['photo1'] = dummy_photo

        Some hairy stuff to get 'new' working with _createObject.

        >>> migrator.new = MockContentType('new')
        >>> migrator.new.manage_addProduct = {}
        >>> migrator.new.manage_addProduct['Image'] = MockSomething()
        >>> migrator.new.portal_types = MockPortalTypes()
        >>> def addImage(id):
        ...     migrator.new[id] = MockContentType('dummy')
        >>> migrator.new.manage_addProduct['Image'].Image = addImage

        >>> migrator.migrate_cmfphotos()

        There should be a new Image inside the new object.

        >>> migrator.new.objectIds()
        ['photo1']
        >>> new_image = migrator.new['photo1']
        >>> new_image.title
        'dummy photo title'
        >>> new_image.data
        'simple string, no unicode'

        """

        logger.info("Starting to migrate CMFPhoto objects.")
        for album in self.old.objectValues():
            if not album.portal_type == 'Photo Album':
                continue
            logger.info("Found a photo album (%s).", album.getId())
            for photo in album.values():
                photo_id = photo.getId()
                format = photo.Format()
                binary_data = photo.data
                title = photo.Title()
                description = photo.Description()
                _createObjectByType('Image', self.new, photo_id)
                image = getattr(self.new, photo_id)
                image.setTitle(title)
                image.setDescription(description)
                image.setImage(binary_data)
                logger.info("Migrated photo %s.", photo_id)
            # Find the CMFPhoto objects in the album.
        # Create new images based on the CMFPhotos.

    def migrate_withmap(self):
        """Copies over attributes according to a map{}.

        Overrides the contentmigration's method. The customization is that it
        checks whether the source/destination actually exist. Handy for
        migrating older versions of realestatebroker, for instance with a
        missing horrible kk_von attribute.

        >>> class Mock:
        ...     pass
        >>> class MockMigrator(RebMigrator):
        ...     def __init__(self):
        ...         # just to quiet down the init.
        ...         pass
        >>> migrator = MockMigrator()
        >>> migrator.old = Mock()
        >>> migrator.new = Mock()

        Copy over single regular attribute.

        >>> migrator.old.a = 'A'
        >>> migrator.map = {'a': ''}
        >>> migrator.migrate_withmap()
        >>> migrator.new.a
        'A'

        If the target attribute somehow already exists, it still works.

        >>> migrator.old.b = 'B'
        >>> migrator.new.b = 'C'
        >>> migrator.map = {'b': ''}
        >>> migrator.migrate_withmap()
        >>> migrator.new.b
        'B'

        If the source attribute is missing, just do nothing.

        >>> migrator.map = {'c': ''}
        >>> migrator.migrate_withmap()
        >>> hasattr(migrator.new, 'c')
        False

        If the source is a method, no problem.

        >>> class MockWithMethod:
        ...     def getE(self):
        ...         return self.e
        ...     def setE(self, value):
        ...         self.e = value
        >>> migrator.old = MockWithMethod()
        >>> migrator.new = MockWithMethod()
        >>> migrator.old.setE('Eeee')
        >>> migrator.map = {'getE': 'setE'}
        >>> migrator.migrate_withmap()
        >>> migrator.new.getE()
        'Eeee'

        If the source is a method, the target is assumed to be a method,
        too. General archetypes getter/setter behaviour. If the target misses
        the setter, assume that the field has been deprecated and forget about
        it. Note that not putting it in the map isn't always an option, as we
        might add a way (ISchema) to re-add custom fields later.

        >>> migrator.old = MockWithMethod()
        >>> migrator.old.setE('Eeee')
        >>> migrator.new = Mock()
        >>> migrator.map = {'getE': 'setE'}
        >>> migrator.migrate_withmap()
        >>> hasattr(migrator.new, 'getE')
        False
        >>> hasattr(migrator.new, 'setE')
        False
        >>> hasattr(migrator.new, 'e')
        False

        """
        NOTAVAILABLE = 'ouch, missing!'
        for oldKey, newKey in self.map.items():

            if not newKey:
                newKey = oldKey
            oldVal = getattr(self.old, oldKey, NOTAVAILABLE)
            newVal = getattr(self.new, newKey, NOTAVAILABLE)
            if oldVal == NOTAVAILABLE:
                return
            if callable(oldVal):
                value = oldVal()
                # newVal must be available
                if newVal == NOTAVAILABLE:
                    return
            else:
                value = oldVal
            if callable(newVal):
                newVal(value)
            else:
                setattr(self.new, newKey, value)

    def migrate_workflow(self):
        """We need to check for the status field of old content types. Since
        recent versions of reb use a special workflow for keeping track of
        the status, allowing automatic transitions based on the age of
        ModificationDate.

        >>> from Products.CMFCore.utils import getToolByName
        >>> class Mock:
        ...     def __init__(self):
        ...         self.status = 'offline'
        ...     def status(self):
        ...         "return status"
        ...         return self.status
        >>> class MockMigrator(RebMigrator):
        ...     def __init__(self):
        ...         # just to quiet down the init.
        ...         pass
        >>> class MockWorkflowTool:
        ...     def __init__(self):
        ...         self.transitions = ('publish','available','negotiate','sell')
        ...         self.chain = ('offline','new','available','negotiating','sold')
        ...         self.index = 0
        ...
        ...     def getInfoFor(self, obj, attr):
        ...         return self.chain[self.index]
        ...
        ...     def doActionFor(self, obj, transition, wf_id=None):
        ...         self.index += 1

        >>> migrator = MockMigrator()
        >>> migrator.old = Mock()
        >>> migrator.new = Mock()
        >>> wf_tool = MockWorkflowTool()
        >>> migrator.new.portal_workflow = wf_tool

        Content with 'available' in the status field should get that workflow
        state after migrating.

        >>> migrator.old.status = 'available'
        >>> wf_tool.getInfoFor(migrator.new, 'review_state')
        'offline'
        >>> migrator.migrate_workflow()
        >>> wf_tool.getInfoFor(migrator.new, 'review_state')
        'available'

        Let us try a state a little bit further up the chain. Note that we
        have to reset the index to 0 for each test.

        >>> wf_tool.index = 0
        >>> migrator.old.status = 'negotiating'
        >>> wf_tool.getInfoFor(migrator.new, 'review_state')
        'offline'
        >>> migrator.migrate_workflow()
        >>> wf_tool.getInfoFor(migrator.new, 'review_state')
        'negotiating'

        """
        NOTAVAILABLE = 'No status field on this object!'

        oldStatus = getattr(self.old, 'status', NOTAVAILABLE)
        if oldStatus == NOTAVAILABLE:
            # Dealing with recent version which has no status field
            return
        else:
            wf_tool = getToolByName(self.new, 'portal_workflow')
            current_review_state = wf_tool.getInfoFor(self.new, 'review_state')
            transition_chain = STATE_TRANSITION_MAP[oldStatus]
            if current_review_state != oldStatus:
                logger.info("Migrating the workflow for %r." % self.new)
                for transition in transition_chain:
                    wf_tool.doActionFor(self.new, transition,
                                        wf_id='realestate_workflow')
                if wf_tool.getInfoFor(self.new, 'review_state') == oldStatus:
                    # We succesfully migrated the status to a workflow state
                    logger.info("Finished migrating workflow for %r." % self.new)
                    return
                else:
                    logger.info("Failed to migrate workflow for %r." % self.new)
                    # something went wrong



class ResidentialMigrator(RebMigrator):
    """Migrate REHome to Residential content types.

    """
    walkerClass = walker.CatalogWalker
    src_meta_type = 'REHome'
    src_portal_type = 'REHome'
    dst_meta_type = 'Residential'
    dst_portal_type = 'Residential'


class CommercialMigrator(RebMigrator):
    """Migrate REHome to Residential content types.

    """
    src_meta_type = 'REBusiness'
    src_portal_type = 'REBusiness'
    dst_meta_type = 'Commercial'
    dst_portal_type = 'Commercial'


def migrate(portal, migrators=(ResidentialMigrator, CommercialMigrator)):
    """Run the migration

    `migrators` is settable for the benefit of testing.

    """
    out = StringIO()
    logger.info("Starting realestatebroker migration.")
    print >> out, "Starting migration"
    for migrator in migrators:
        walker = migrator.walkerClass(portal, migrator)
        walker.go(out=out)
        print >> out, walker.getOutput()
    print >> out, "Migration finished"
    return out.getvalue()
