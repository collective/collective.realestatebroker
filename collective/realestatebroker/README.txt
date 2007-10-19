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
    ''

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

For the city field we make use of a vocabulary that reads it's values from a
propertysheet.

    >>> from collective.realestatebroker.content.base import CityVocabularyFactory
    >>> vocab = CityVocabularyFactory(self.portal)
    >>> [item.value for item in vocab]
    ['New York', 'London', 'Amsterdam', 'Paris', 'Tokyo', 'Alberschwende']

