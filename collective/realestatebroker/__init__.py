"""Main product initializer
"""

from zope.i18nmessageid import MessageFactory
from collective.realestatebroker import config

from Products.Archetypes import atapi
from Products.CMFCore import utils as cmfutils

# Define a message factory for when this product is internationalised.
# This will be imported with the special name "_" in most modules. Strings
# like _(u"message") will then be extracted by i18n tools for translation.
REBMessageFactory = MessageFactory('collective.realestatebroker')

# We want the original_size of an image field set to (768,768)
from Products.ATContentTypes.content.image import ATImage

def initialize(context):
    """Initializer called when used as a Zope 2 product.

    This is referenced from configure.zcml. Regstrations as a "Zope 2 product"
    is necessary for GenericSetup profiles to work, for example.

    Here, we call the Archetypes machinery to register our content types
    with Zope and the CMF.

      >>> from collective.realestatebroker import initialize
      >>> class MockContext:
      ...     def registerClass(*args, **kw):
      ...         pass
      >>> context = MockContext()
      >>> initialize(context)
    """

    # Retrieve the content types that have been registered with Archetypes
    # This happens when the content type is imported and the registerType()
    # call in the content type's module is invoked. Actually, this happens
    # during ZCML processing, but we do it here again to be explicit. Of
    # course, even if we import the module several times, it is only run
    # once!

    from content import residential
    from content import commercial
    residential, commercial  # pyflakes


    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes(config.PROJECTNAME),
        config.PROJECTNAME)

    # Now initialize all these content types. The initialization process takes
    # care of registering low-level Zope 2 factories, including the relevant
    # add-permission. These are listed in config.py. We use different
    # permisisons for each content type to allow maximum flexibility of who
    # can add which content types, where. The roles are set up in rolemap.xml
    # in the GenericSetup profile.

    for atype, constructor in zip(content_types, constructors):
        cmfutils.ContentInit(
            "%s: %s" % (config.PROJECTNAME, atype.portal_type),
            content_types = (atype,),
            permission = config.ADD_PERMISSIONS[atype.portal_type],
            extra_constructors = (constructor,),
            ).initialize(context)

    # Add an extra scaling size to the ATImage scaling list
    image_sizes = ATImage.schema['image'].sizes
    if not image_sizes.has_key('tile96'):
        image_sizes['tile96'] = (96,96)
        ATImage.schema['image'].sizes = image_sizes


    ATImage.schema['image'].original_size = (768,768)
