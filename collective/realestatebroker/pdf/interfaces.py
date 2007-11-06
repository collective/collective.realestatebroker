from zope.interface import Interface
from zope.schema import Bytes
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
