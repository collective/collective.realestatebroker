from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('collective.realestatebroker')


class IPDFPresentation(Interface):
    """Present objects as PDF in a file object
    """
    def read(size=-1):
        """Read data from file"""

    def tell():
        """Return the file's current position"""

    def seek(offset, whence=0):
        """Set the file's current position"""


class IHeaderAndFooter(Interface):
    """Utility (function) to add header/footer."""


class IStyleModifier(Interface):
    """Utility (function) to modify styles."""


class IFrontPage(Interface):
    """Utility (function) to replace frontpage."""


class IBackMatter(Interface):
    """Utility (function) to insert back matter."""
