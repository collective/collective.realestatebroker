import logging

from zope.traversing.api import getName
from zope.component import getMultiAdapter
from zope.publisher.browser import BrowserPage
from zope.cachedescriptors.property import Lazy

from collective.realestatebroker.pdf.interfaces import IPDFPresentation


logger = logging.getLogger('reb-pdf')


class PDFView(BrowserPage):

    def __call__(self):
        filename = self.context.getId() + '.pdf'
        response = self.request.response
        response.setHeader('Content-Disposition',
                           'attachment; filename=%s' % filename)
        response.setHeader('Content-Type', 'application/pdf')
        return self.pdf()

    @Lazy
    def cache_key(self):
        """Return the cache key.

        We depend on:

        * Zope startup time so that we catch product updates.
        * Last modification inside the residential object, including image
          updates.

        """
        zope_startup_time = None

    def get_cached_pdf(self):
        """Return cached pdf if the key is still valid, otherwise None."""
        return None

    def store_in_cache(self, pdf):
        """Store the pdf in the cache."""
        pass

    def pdf(self):
        """Try getting a cached copy first, otherwise generate a PDF."""

        pdf_file = self.get_cached_pdf()
        if pdf_file is not None:
            logger.info("Returned cached PDF for %s.",
                        self.context.absolute_url())
            return pdf_file
        pdf_file = getMultiAdapter((self.context, self.request),
                                   IPDFPresentation)
        self.store_in_cache(pdf_file)
        logger.info("Calculated (and cached) PDF for %s.",
                    self.context.absolute_url())
        return pdf_file
