History of collective.realestatebroker
======================================

2.3 (2012-10-14)
----------------

- Moved to https://github.com/collective/collective.realestatebroker

- Reintroduce version specific pin of Products.contentmigration==1.0b4
  because with other versions there are test failures.
  [maurits]

- No longer require specific versions of archetypes.schemaextender
  (1.0b1) and Products.contentmigration (1.0b4), but let those be
  minimum versions.
  [maurits]


2.2 (2009-06-10)
----------------

- Use unicode_vocabulary instead of SimpleVocabulary in all
  vocabularies to catch UnicodeEncodeErrors like in
  http://plone.org/products/realestatebroker/issues/6
  [maurits]

- Copied code from Products.PloneFlashUpload 1.2rc so the upload on
  the album management works again.  (At least with Flash 10 on
  Linux).  [maurits]


2.1 (2009-03-26)
----------------

- Added French translations thanks to Benjamin Klups. [jladage]


2.0.9 (2009-03-04)
------------------

- Allow access to the AlbumView.first_image; an Unauthorized error is
  triggered when using this in for example a collection portlet.
  [maurits]


2.0.8 (2009-01-27)
------------------

- Fixed bug in floorplan filter: the photo management page also filtered them,
  making them impossible to edit. [reinout]


2.0.7 (2009-01-27)
------------------

- Filtering out floorplans from all the photo lists. [reinout]


2.0.6 (2008-12-18)
------------------

- Some html fixes by jladage?


2.0.5 (2008-12-17)
------------------

- Fixed keyerror when floorplans aren't attached to floors. The keyerror
  itself is caught now and the cause has also been removed. [reinout]


2.0.4 (2008-07-30)
------------------

- Added ReportLab and Products.Maps as dependencies in setup.py.
  [maurits]


2.0.3 (2008-07-03)
------------------

- Unchanged from rc4.


2.0.3 rc4 (2008-07-02)
----------------------

- Creating our own img tags from catalog brains instead of doing a
  .getObject() to use archetypes tag() method which wakes up the
  object. [reinout]


2.0.3 rc3 (2008-06-25)
----------------------

- Fixed strange attributeerror on plone 3.1.2. Moving to that plone version
  fixes a kss bug in the album view. [reinout]


2.0.3 rc2 (2008-06-25)
----------------------

- Added optional max_height attribute to insert_image() to allow protection
  for overly large portrait image on the pdf's homepage. [reinout]

- Added css class to table cells that contain an image in the res/comm
  listings so that the image can be aligned vertically if desired. [reinout]

- Added caching of rendered pdf in an annotation. Saves a lot of cpu
  time. [reinout]


2.0.3 rc1 (released)
--------------------

- Moved rent_buy to the financial schemata for the edit view so that all
  financial fields are on the same screen. [fredvd]

- Added a field for indicating if the price is a fixed price or is still
  negotiable. Not used (yet) in the collective.realestatebroker package view
  templates, but can be exposed in your own template overrides [fredvd]


2.0.2 (released 2008-04-21)
---------------------------

- no changes, make a final release for references [fredvd]


2.0.1 rc4 (released 2008-03-06)
-------------------------------
- Add new rented state and accompanying transition so that rented houses
  have a proper listing [fred]


2.0.1 rc3 (released 2008-02-29)
-------------------------------

- View order fixed (state first, creation date second). [joris]

- Fixed test to reflect change done in rc2. [reinout]

- add house_type to the portal_catalog index (getHouse_type) [fred]

- added discreet color on formHelp [mirella]

2.0.1 rc2 (released 2008-02-04)
-------------------------------

- Fixed bug in the condition for googlemaps' javascript: it was not loaded on
  the edit form. [reinout]

2.0.1 rc (released 2008-02-04)
------------------------------

- Fixed bug in display of houses/offices: the main thumbnail picture now
  points at /album instead of /photo. /photo could result in an orgy of
  redirects. [reinout]

2.0.1 beta3 (released 2008-01-25)
---------------------------------

- Google maps' js is only enabled if the url ends on '/map' now, so the other
  tabs don't have to load it. [reinout]

- Changed sort_order in the realestate view, so that 'new' real estate
  objects are always on top of the list. These are the most interesting for
  visitors checking your real_estate. [fred]

- Removed size limit on the construction year field. This allows you to add
  '2007-2008' as a construction year, for instance. [reinout]

2.0.1 beta2 (released 2008-01-17)
---------------------------------

- Added manager-only textual search form to the listing templates. [reinout]

2.0.1 beta  (released 2008-01-15)
---------------------------------

- Capitalized the 'view' action so that the translation is picked up. [reinout]

- Dutch translation fix ("opslag"). [reinout]

- Removed an unused viewletmanager configuration and enabled the titlemanager
  for every skin.

- Added two extra safe_unicode() calls to the pdf generator to prevent decode
  errors.

2.0 final
---------

- Released on 2008-01-11, no changes from the rc6.

2.0 rc6
-------

- README updated. [reinout]

- Old temporary image size name renamed to something more
  appropriate. [fredvd]

- Disabling special kk_von handling as the values of the field are the same
  again as in the old database. Sorry for the noise. [reinout]

2.0 rc5
-------

- Fix for faulty images (width==0, so you get a division by zero error)
  [reinout]

2.0 rc4
-------

- rent_buy vocabulary is handled by the propertysheet again.

2.0 rc2
-------

- Optionally disabled filtering of empty fields. [reinout]

- Translation improvement for boolean fields. [reinout]

- Small pdf page margin changes. [reinout]

- Rent/buy is now a fixed vocabulary (needed for a userfriendly default
  value). [reinout]

- Added try/except for corrupt images (read: unaccessible images that redirect
  to a login page). [Reinout]

2.0 rc
------

- Translated the schemata names and the workflow names (in a separate
  old-style Product: reb_i18n) [Reinout van Rees]

- Added rent/buy field to Residential, too.
