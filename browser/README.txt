Hm. Almost nothing is tested in here. Let's import everything so that the code
coverage report starts to expose this.

    >>> from collective.realestatebroker.browser import base
    >>> from collective.realestatebroker.browser import commercial
    >>> from collective.realestatebroker.adapters import floor
    >>> from collective.realestatebroker.browser import interfaces
    >>> from collective.realestatebroker.browser import map
    >>> from collective.realestatebroker.browser import residential
    >>> from collective.realestatebroker.browser import viewlets
