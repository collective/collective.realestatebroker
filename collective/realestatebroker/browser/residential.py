"""Define a browser view for the Residential content type. 
"""

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ResidentialView(BrowserView):
    """Default view of a Residential Property
    """
    
    __call__ = ViewPageTemplateFile('residential_view.pt')
