import unittest
from zope.testing import doctest
from zope.component import testing


def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite('content/contenttypes.txt',
                             package='collective.realestatebroker',
                             optionflags=doctest.ELLIPSIS),
        doctest.DocFileSuite('tests/migration-unittest.txt',
                             package='collective.realestatebroker',
                             optionflags=doctest.ELLIPSIS),
        doctest.DocTestSuite(module='collective.realestatebroker'),
        doctest.DocTestSuite(module='collective.realestatebroker.migration'),
        ))
