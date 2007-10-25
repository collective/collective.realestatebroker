Real estate broker
==================

The real estate broker product turns plone into a real estate broker website.
Show your commercial and residential real estate with the two real estate
content types.  Allow visitors to search the database with the provided forms.
Email updates for registered visitors.  Google map support.  Easy addition of
images.

Verified documentation
----------------------

Documentation should be correct and up to date.  To assure that, the
documentation is used to test the software.  So both the software and the
documentation are assured to be correct.  That is why you will see code
examples throughout this document.

First a small bit of setup: adding an admin user and a registered visitor.

    >>> self.loginAsPortalOwner()
    >>> self.portal.portal_membership.addMember('admin', 'secret', ['Manager'], [])
    >>> self.portal.portal_membership.addMember('visitor', 'secret', ['Reader'], [])

Installing real estate broker
-----------------------------

TODO: Describe buildout.

Inside plone, log in with an administrator account and install real estate
broker through the quickinstaller (in the plone control panel: "add/remove
products").

    >>> self.login('admin')
    >>> qi = self.portal.portal_quickinstaller
    >>> qi.installProduct('collective.realestatebroker')
    
(This returns not an empty string because we're using Extensions/Install.py which starts
GS installation after installing the Maps product dependency.) 


Testing for Maps Product Dependency
-----------------------------------

RealEstateBroker makes use of the Maps product to integrate Google Maps. Check
that this product is also available in the site after RealEstateBroker has 
been installed

    >>> self.portal.portal_quickinstaller.isProductInstalled('Maps')
    True

Commercial and residential real estate content types
----------------------------------------------------

    >>> self.portal.invokeFactory('Residential', id='home1')
    'home1'
    >>> self.portal.invokeFactory('Commercial', id='office1')
    'office1'


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


Portal Properties
--------------------

RealEstateBroker installs under portal_properties a file with default attributes

    >>> pptool = self.portal.portal_properties
    >>> self.failUnless('realestatebroker_properties' in pptool.objectIds())


Vocabularies
------------

For the city field we make use of a vocabulary that reads it's values from a
propertysheet.

    >>> from collective.realestatebroker.content.vocabularies import CityVocabularyFactory
    >>> vocab = CityVocabularyFactory(self.portal)
    >>> [item.value for item in vocab]
    ['New York', 'London', 'Amsterdam', 'Paris', 'Tokyo', 'Alberschwende']

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

For the k.k./v.o.n. field we make use of a vocabulary that reads it's values from a
propertysheet.

    >>> from collective.realestatebroker.content.vocabularies import KKVONVocabularyFactory
    >>> vocab = KKVONVocabularyFactory(self.portal)
    >>> [item.value for item in vocab]
    ['Kosten koper (k.k.)', 'Vrij op naam (v.o.n.)']


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
    >>> view = home1.restrictedTraverse('@@maps_googlemaps_enabled_view')
    >>> view.enabled # We want to show maps.
    True
