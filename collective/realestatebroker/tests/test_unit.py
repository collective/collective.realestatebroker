import unittest
from zope.testing import doctest
from zope.testing import doctestunit
from zope.component import testing
from collective.realestatebroker.config import MIGRATIONPRODUCTAVAILABLE


OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

def setUp(test):
    testing.setUp(test)

def tearDown(test):
    testing.tearDown(test)


def test_suite():
    normal_suites = (
        doctestunit.DocFileSuite('content/contenttypes.txt',
                             package='collective.realestatebroker',
                             optionflags=OPTIONFLAGS,
                             setUp=setUp,
                             tearDown=tearDown),
        doctestunit.DocTestSuite(module='collective.realestatebroker',
                             setUp=setUp,
                             tearDown=tearDown,
                             optionflags=OPTIONFLAGS),
        doctestunit.DocTestSuite(module='collective.realestatebroker.utils',
                             setUp=setUp,
                             tearDown=tearDown,
                             optionflags=OPTIONFLAGS),
        )
    if MIGRATIONPRODUCTAVAILABLE:
        migration_suites = (
            doctestunit.DocFileSuite('tests/migration-unittest.txt',
                                     package='collective.realestatebroker',
                                     optionflags=OPTIONFLAGS),
            doctestunit.DocTestSuite(module='collective.realestatebroker.migration',
                                     setUp=setUp,
                                     tearDown=tearDown,
                                     optionflags=OPTIONFLAGS),
            )
    if MIGRATIONPRODUCTAVAILABLE:
        suites = normal_suites + migration_suites
    else:
        suites = normal_suites
    return unittest.TestSuite(suites)
