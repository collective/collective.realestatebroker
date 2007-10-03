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

"""
from Products.contentmigration import walker
from Products.contentmigration import migrator
from Products.contentmigration import field
import logging
logger = logging.getLogger('rebmigrator')


class RebMigrator: # TODO: subclass from a migrator.*
    """Base class to migrate objects to a realestatebroker content type.

    In addition to contentmigration's functionality, RebMigrator also converts
    nested CMFPhotos.

    Methods that start with `migrate_` are automatically called after the
    regular contentmigration functionality has created the new product.
    """

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
    """Migrate REHome to Residential content types."""
    walkerClass = walker.CatalogWalker
    src_meta_type = 'REHome'
    src_portal_type = 'REHome'
    dst_meta_type = 'Residential'
    dst_portal_type = 'Residential'
    map = {} # {'getOldField': 'setNewField'}


# TODO: add CommercialMigrator


def migrate(self):
    """Run the migration"""

    out = StringIO()
    logger.info("Starting realestatebroker migration.")
    print >> out, "Starting migration"
    portal_url = getToolByName(self, 'portal_url')
    portal = portal_url.getPortalObject()
    migrators = (ResidentialMigrator,)
    for migrator in migrators:
        walker = migrator.walkerClass(portal, migrator)
        walker.go(out=out)
        print >> out, walker.getOutput()
    print >> out, "Migration finished"
    return out.getvalue()
