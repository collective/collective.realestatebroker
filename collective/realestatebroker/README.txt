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
