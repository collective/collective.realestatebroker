"""Define a browser view for the Residential content type. 
"""

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ResidentialView(BrowserView):
    """Default view of a Residential Property
    """
    
    __call__ = ViewPageTemplateFile('residential.pt')

    def CookedPrice(self):
        """Return formatted price"""
        pr = str(self.context.price)
        elements = []
        
        if len(pr) > 9:
            elements.append(pr[-12:-9])
        if len(pr) > 6:
            elements.append(pr[-9:-6])
        if len(pr) > 3:
            elements.append(pr[-6:-3])
        elements.append(pr[-3:])
        return '.'.join(elements)

    def fredtest(self):
        return "tekstje"
        
    def CookedBody(self):
        """Dummy attribute to allow drop-in replacement of Document"""
        return self.getMainText()

    def CookedAcceptance(self):
        """Dummy attribute to allow drop-in replacement of Document"""
        return self.getAcceptance()