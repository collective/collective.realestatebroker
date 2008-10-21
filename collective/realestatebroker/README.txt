Real estate broker
==================

The real estate broker product turns plone into a real estate broker website.
Show your commercial and residential real estate with the two real estate
content types.  Allow visitors to search the database with the provided forms.
Email updates for registered visitors.  Google map support.  Easy
mass-addition of images.  PDF export.


Verified documentation
----------------------

Documentation should be correct and up to date.  To assure that, the
documentation is used to test the software.  So both the software and the
documentation are assured to be correct.  That is why you will see code
examples throughout this document.

First a small bit of setup: adding an admin user and a registered visitor.

    >>> self.loginAsPortalOwner()
    >>> self.portal.portal_membership.addMember('admin', 'secret',
    ...                                         ['Manager'], [])
    >>> self.portal.portal_membership.addMember('visitor', 'secret',
    ...                                         ['Reader'], [])

Installing real estate broker
-----------------------------

The handiest way to get up and running with plone 3.0 and realestatebroker is
to use the buildout. The basic setup can be done with::

 https://svn.plone.org/svn/collective/collective.realestatebroker/buildout/reb30/trunk

If you have old 1.0 content you can migrate that by uncommenting two lines in
the buildout, as indicated there with a comment.

Inside plone, log in with an administrator account and install real estate
broker through the quickinstaller (in the plone control panel: "add/remove
products").

    >>> self.login('admin')
    >>> qi = self.portal.portal_quickinstaller
    >>> qi.installProduct('collective.realestatebroker')


Add-on products
---------------

RealEstateBroker makes use of the Maps product to integrate Google Maps. Check
that this product is also available in the site after RealEstateBroker has
been installed.

    >>> self.portal.portal_quickinstaller.isProductInstalled('Maps')
    True

PloneFlashUpload is used for easy mass-uploading of images.

    >>> self.portal.portal_quickinstaller.isProductInstalled('PloneFlashUpload')
    True

Behind the scenes, the reportlab library is used to export PDF.


Commercial and residential real estate content types
----------------------------------------------------

There are two content types, residential and commercial. They differ in a few
fields.

    >>> self.portal.invokeFactory('Residential', id='home1')
    'home1'
    >>> self.portal.invokeFactory('Commercial', id='office1')
    'office1'


Migration support for the old 1.0 version to 2.0
------------------------------------------------

If you installed using the migration buildout, a reinstall of realestatebroker
will perform a migration. The migration does the following:

- Replace old REHome/REBusiness objects with Residential/Commercial objects.

- REHome/REBusiness have CMFPhotoAlbums with CMFPhotos in them, these photos
  are moved directly into the (folderish) Residential/Commercial object as
  regular Images.

- Migrate old workflow states OR old status field to new workflow states.

- Copy over all the fields if still present in the new content types.

It is probably best to create a new site in 3.0 and to selectively move things
over. You cannot do a direct 2.0 to 3.0 plone migration anyway. It works to
make a `.zexp` export of the old houses and offices and to import them in a
3.0 site, assuming you have the migration buildout installed: that buildout
includes hacked-up versions of the old RealEstateBroker product, CMFPhoto and
CMFPhotoAlbum that lets you load the old objects.


Customization
-------------

Almost surely, realestatebroker will need to be adapted to local
circumstances. In the Netherlands, an airco is not common, but in the south of
the USA it might be something you want to keep track of.

archetypes.schemaextender is a great tool for cleanly adapting the schema. See
realestatebroker's documentation_ section on plone.org for a how-to.

Also, the PDF export will need work like adding a header/footer. And choosing
a different font. Here also: see the plone.org documentation_.


Real Estate Workflow
--------------------

Real Estate Broker comes with a special workflow named 'realestate_workflow'
which is mapped to both the Residential and Commmercial content type.

    >>> home1 = self.portal.home1
    >>> wftool = self.portal.portal_workflow
    >>> self.failUnless('realestate_workflow' in wftool.objectIds())
    >>> wftool.getChainForPortalType('Commercial')
    ('realestate_workflow',)
    >>> wftool.getChainForPortalType('Residential')
    ('realestate_workflow',)

The initial state of real estate content should be offline, which means
anonymous can't view it and only owner, editor and manager can edit it. From
this state we can publish the content, which will bring it to the 'new' state.

    >>> wftool.getInfoFor(home1, 'review_state')
    'offline'
    >>> wftool.doActionFor(home1, 'publish', wf_id='realestate_workflow')
    >>> wftool.getInfoFor(home1, 'review_state')
    'new'

After two weeks, new items will become regular items so that new items can be
displayed more prominently in the listing. Similarly, sold items will remain
visible for two weeks (which is important for getting the "this realestate
broker really sells quite some houses" impression).

Portal Properties
-----------------

RealEstateBroker installs under portal_properties a property sheet with
default attributes.

    >>> pptool = self.portal.portal_properties
    >>> self.failUnless('realestatebroker_properties' in pptool.objectIds())


Site Properties
---------------

Don't show Resdiential or Commecial objects in the navigation tree.

    >>> navtree_props = pptool.navtree_properties
    >>> types_not_to_list = navtree_props.getProperty('metaTypesNotToList')
    >>> self.failUnless('Residential' in types_not_to_list)
    >>> self.failUnless('Commercial' in types_not_to_list)


Vocabularies
------------

For the city field we make use of a vocabulary that reads it's values from a
propertysheet.

    >>> from collective.realestatebroker.content.vocabularies import CityVocabularyFactory
    >>> vocab = CityVocabularyFactory(self.portal)
    >>> [item.value for item in vocab]
    [u'New York', u'London', u'Amsterdam', u'Paris', u'Tokyo', u'Alberschwende']

For the house type field we make use of a vocabulary that reads it's values from a
propertysheet.

    >>> from collective.realestatebroker.content.vocabularies import HouseTypeVocabularyFactory
    >>> vocab = HouseTypeVocabularyFactory(self.portal)
    >>> [item.value for item in vocab]
    ['Apartment', 'Villa', 'Mansion']

For the rooms field we make use of a vocabulary that reads it's values from a
propertysheet.

    >>> from collective.realestatebroker.content.vocabularies import RoomsVocabularyFactory
    >>> vocab = RoomsVocabularyFactory(self.portal)
    >>> [item.value for item in vocab]
    ['1', '2', '3', '4', '5', '6', '7', '8']

portal_catalog Indexes
----------------------

Test if the index have been created in the portal_catalog tool.

    >>> indexes = self.portal.portal_catalog.indexes()
    >>> for idx in ('getPrice', 'getCity', 'is_floorplan'):
    ...     self.failUnless(idx in indexes)

Google maps support
-------------------

Realestatebroker uses the 'Maps' product for google map support. Our
contenttypes can be used by Maps:

    >>> from collective.realestatebroker.interfaces import IRealEstateContent
    >>> from collective.realestatebroker.interfaces import IResidential
    >>> IRealEstateContent.providedBy(home1)
    True
    >>> IResidential.providedBy(home1)
    True
    >>> from Products.Maps.interfaces import IMapView

The maps javascripts aren't loaded on the main view (and several others) for
performance reasons:

    >>> view = home1.restrictedTraverse('@@maps_googlemaps_enabled_view')
    >>> view.enabled
    False

We're showing it on the "edit" form and the "map" tab:

    >>> class Dummy:
    ...     url = 'dummy'
    ...     def getURL(self):
    ...         return self.url
    >>> view.request = Dummy()
    >>> view.enabled # still no.
    False
    >>> view.request.url = 'something/edit'
    >>> view.enabled
    True
    >>> view.request.url = 'something/map'
    >>> view.enabled
    True

Authors
-------

Original 1.0 version made by Ahmad Hadi and Jean-Paul Ladage.

2.0 re-write done by `Reinout van Rees <http://vanrees.org/>`_, `Jean-Paul
Ladage <mailto:j.ladage@zestsoftware.nl>`_, `Fred van
Dijk <http://zestsoftware.nl/home/team/fvandijk>`_ and `Mirella van
Teulingen <http://zestsoftware.nl/home/team/mirellavanteulingen>`_, all of `Zest
software <http://zestsoftware.nl/>`_ .


.. _documentation: http://plone.org/products/realestatebroker/documentation/