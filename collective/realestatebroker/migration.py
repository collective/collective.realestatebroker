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

    def migrate_withmap(self):
        """Copies over attributes according to a map{}.

        Overrides the contentmigration's method. The customization is that it
        checks whether the source/destination actually exist. Handy for
        migrating older versions of realestatebroker, for instance with a
        missing horrible kk_von attribute.

        >>> class Dummy:
        ...     pass
        >>> class DummyMigrator(RebMigrator):
        ...     def __init__(self):
        ...         # just to quiet down the init.
        ...         pass
        >>> migrator = DummyMigrator()
        >>> migrator.old = Dummy()
        >>> migrator.new = Dummy()

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

        >>> class DummyWithMethod:
        ...     def getE(self):
        ...         return self.e
        ...     def setE(self, value):
        ...         self.e = value
        >>> migrator.old = DummyWithMethod()
        >>> migrator.new = DummyWithMethod()
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

        >>> migrator.old = DummyWithMethod()
        >>> migrator.old.setE('Eeee')
        >>> migrator.new = Dummy()
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
