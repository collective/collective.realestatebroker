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

In the end, the migrator is run like this:

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
>>> class MockPortal(Acquisition.Implicit):
...     portal_types = MockPortalTypes()
...     def _checkId(self, id):
...         return True
...     def _getOb(self, id):
...         return getattr(self, id)
...     def _delObject(self, id):
...         delattr(self, id)
...     def manage_delObjects(self, ids):
...         for id in ids:
...             self._delObject(id)
...     def _setObject(self, new_id, ob, set_owner=0):
...         setattr(self, new_id, ob)
...     def __init__(self):
...         self.aq_explicit = self
...     manage_addProduct = {}
...     manage_addProduct['Residential'] = MockSomething()
...     manage_addProduct['Commercial'] = MockSomething()
>>> portal = MockPortal()
>>> class MockContentType(Acquisition.Implicit):
...     aq_parent = portal
...     typename = 'mock'
...     def __init__(self, id):
...         self.id = id
...     def getTypeInfo(self):
...         fti = MockSomething()
...         fti.product = self.typename
...         fti.factory = self.typename
...         return fti
...     def getObject(self):
...         # Double as a brain ;-)
...         return self
...     def getPhysicalPath(self):
...         return ['root', self.id]
...     def getId(self):
...         return self.id
...     def absolute_url(self, *args):
...         return 'http://site/' + self.id
...     def CreationDate(self):
...         return 1
...     def ModificationDate(self):
...         return 1
...     def cb_isMoveable(self):
...         return True
...     def _notifyOfCopyTo(self, *args, **kw):
...         pass
...     def _setId(self, id):
...         self.id = id
...     def _postCopy(self, *args, **kw):
...         pass
>>> class MockREHome(MockContentType):
...     typename = 'REHome'
>>> class MockResidential(MockContentType):
...     typename = 'Residential'
>>> class MockREBusiness(MockContentType):
...     typename = 'REBusiness'
>>> class MockCommercial(MockContentType):
...     typename = 'Commercial'
>>> def addResidential(id):
...     portal._setObject(id, MockResidential(id))
>>> portal.manage_addProduct['Residential'].Residential = addResidential
>>> def addCommercial(id):
...     portal._setObject(id, MockCommercial(id))
>>> portal.manage_addProduct['Commercial'].Commercial = addCommercial
>>> portal._setObject('one', MockREHome('one'))
>>> portal._setObject('two', MockREBusiness('two'))
>>> class MockCatalog:
...     threshold = None
...     def __call__(self, query):
...         # Is expected to return brains.
...         if query['portal_type'] == 'REHome':
...             return [portal.one]
...         if query['portal_type'] == 'REBusiness':
...             return [portal.two]
>>> portal.portal_catalog = MockCatalog()
>>> class DisabledMigration:
...     # To prevent too much Mock* work, we'll disable migration of
...     # Title and Description and so. That'll just work.
...     def __init__(self, name):
...         self.name = name
...     def __call__(self):
...         print "Dummy migration: " + self.name
>>> from collective.realestatebroker.migration import ResidentialMigrator
>>> ResidentialMigrator.migrate_dc = DisabledMigration('DC')
>>> ResidentialMigrator.migrate_localroles = DisabledMigration('local roles')
>>> ResidentialMigrator.migrate_owner = DisabledMigration('owner')
>>> ResidentialMigrator.migrate_permission_settings = DisabledMigration('permission_settings')
>>> ResidentialMigrator.last_migrate_date = DisabledMigration('migration date')
>>> from collective.realestatebroker.migration import CommercialMigrator
>>> CommercialMigrator.migrate_dc = DisabledMigration('DC')
>>> CommercialMigrator.migrate_localroles = DisabledMigration('local roles')
>>> CommercialMigrator.migrate_owner = DisabledMigration('owner')
>>> CommercialMigrator.migrate_permission_settings = DisabledMigration('permission_settings')
>>> CommercialMigrator.last_migrate_date = DisabledMigration('migration date')

We have set up a dummy portal and dummy content types and we've disabled a
couple of non-interesting migration steps. So we can now run the migration.

>>> migrate(portal, migrators=(ResidentialMigrator, CommercialMigrator))
Dummy migration: DC
Dummy migration: local roles
Dummy migration: owner
Dummy migration: permission_settings
Dummy migration: migration date
Dummy migration: DC
Dummy migration: local roles
Dummy migration: owner
Dummy migration: permission_settings
Dummy migration: migration date
'Starting migration\\nMigrating root/one (REHome -> Residential)\\n\\nMigrating root/two (REBusiness -> Commercial)\\n\\nMigration finished\\n'
>>> portal.one.typename
'Residential'


"""
from StringIO import StringIO
from Products.contentmigration import walker
from Products.contentmigration.basemigrator.migrator import CMFItemMigrator
from Products.contentmigration import field
import logging
logger = logging.getLogger('rebmigrator')


class RebMigrator(CMFItemMigrator):
    """Base class to migrate objects to a realestatebroker content type.

    In addition to contentmigration's functionality, RebMigrator also converts
    nested CMFPhotos.

    Methods that start with `migrate_` are automatically called after the
    regular contentmigration functionality has created the new product.
    """

    # def beforeChange_* (done before migration)
    # def last_migrate_* (done just before migration finishes)

    def migrate_cmfphotos(self):
        """Migrate nested CMFPhotos to regular ATImages.

        REHome/REBusiness have CMFPhotoAlbums with CMFPhotos in them, these
        photos must be moved directly into the (folderish)
        Residential/Commercial object as regular Images.

        """

        logger.info("Starting to migrate CMFPhoto objects.")
        # Find the CMFPhotoAlbum object. Is this always `photos`?
        # Find the CMFPhoto objects in the album.
        # Create new images based on the CMFPhotos.


class ResidentialMigrator(RebMigrator):
    """Migrate REHome to Residential content types.

    """
    walkerClass = walker.CatalogWalker
    src_meta_type = 'REHome'
    src_portal_type = 'REHome'
    dst_meta_type = 'Residential'
    dst_portal_type = 'Residential'
    map = {#'getPrice': 'setPrice',
        }


class CommercialMigrator(RebMigrator):
    """Migrate REHome to Residential content types.

    """
    walkerClass = walker.CatalogWalker
    src_meta_type = 'REBusiness'
    src_portal_type = 'REBusiness'
    dst_meta_type = 'Commercial'
    dst_portal_type = 'Commercial'
    map = {#'getPrice': 'setPrice',
        }


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
