"""Migration support for the old 1.0 version to 2.0.

We have to accomplish several tasks:

- Replace old REHome/REBusiness objects with Residential/Commercial objects.

- REHome/REBusiness have CMFPhotoAlbums with CMFPhotos in them, these photos
  must be moved directly into the (folderish) Residential/Commercial object as
  regular Images.

- Migrate old property sheets to new ones.

- Clean up leftover junk like skin layers and old portal types and two portal
  actions.

- Remove RealEstateBroker/CMFPhoto(Album) from the quickinstaller.

"""
from Products.contentmigration import walker
from Products.contentmigration import migrator
from Products.contentmigration import field
