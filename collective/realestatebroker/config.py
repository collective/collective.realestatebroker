"""Common configuration constants
"""

PROJECTNAME = "collective.realestatebroker"
#CUSTOM_PORTLET_COLUMN = u"plone.rightcolumn"

# This maps portal types to their corresponding add permissions.
# These are referenced in the root product __init__.py, during
# Archetypes/CMF type initialisation. The permissions here are
# also defined in content/configure.zcml, so that they can be
# looked up as a Zope 3-style IPermission utility.

# We prefix the permission names with our product name to group
# them sensibly. This is good practice, because it makes it
# easier to find permissions in the Security tab in the ZMI.

ADD_PERMISSIONS = {
    "Residential" : "realestatebroker : Add Residential real estate",
    "Commercial" : "realestatebroker : Add Commercial real estate",
}

# For migration from the status field to the Worklflow state we need to change
# the workflow state starting from the initial state. This map allows us to
# perform the necessary transitions to get to the given review_state.

STATE_TRANSITION_MAP = dict(offline=None,
                            new=('publish',),
                            available=('publish','available'),
                            negotiating=('publish','available',
                                         'negotiate',),
                            reserved=('publish','available','negotiate',
                                      'reserve'),
                            sold=('publish','available','negotiate',
                                  'reserve','sell'),
                            )
