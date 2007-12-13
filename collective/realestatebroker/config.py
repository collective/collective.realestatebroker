"""Common configuration constants
"""

PROJECTNAME = "collective.realestatebroker"

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
