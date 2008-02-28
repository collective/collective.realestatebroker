from Products.CMFCore.utils import getToolByName
from pkg_resources import parse_version
import transaction


def importVarious(context):
    """This is the main step that is called by genericsetup."""
    # Only run step if a flag file is present, otherwise it run every time
    # that generic setup runs all steps of *any* profile.
    if context.readDataFile('realestatebroker.txt') is None:
        return
    site = context.getSite()
    logger = context.getLogger('realestatebroker')
    migrate_old_content(site, logger)
    remove_upload_action(site, logger)
    add_indexes(site, logger)
    update_schemas(site, logger)
    fix_schema_bug(site, logger)


def fix_schema_bug(site, logger):
    """Copied from http://dev.plone.org/collective/browser/eXtremeManagement
    /trunk/Extensions/fix_schema.py"""
    catalog = getToolByName(site, 'portal_catalog')
    brains = catalog()
    logger.debug("%s brains found.", len(brains))
    count = 0
    for brain in brains:
        try:
            obj = brain.getObject()
        except AttributeError:
            logger.warning('Ignoring dead brain pointing to %s.',
                           brain.getPath())
        if 'schema' in obj.__dict__:
            logger.warning('Removing schema attribute from %s.',
                           obj.absolute_url())
            del obj.schema
            count += 1
    logger.info('In total %s schemas were removed.', count)
    transaction.savepoint(optimistic=True)


def update_schemas(site, logger):
    qi = getToolByName(site, 'portal_quickinstaller')
    installed_version = qi.getProductVersion('collective.realestatebroker')
    installed_version = parse_version(installed_version)
    update = [] # List of schemas to update.
    # Now for some if/else, this could be expanded later on.
    if installed_version < parse_version('2.0 rc3'):
        update.append('collective.realestatebroker.Residential')
        update.append('collective.realestatebroker.Commercial')
    # Update the schemas
    at = getToolByName(site, 'archetype_tool')

    class dummy:
        form = {}

    dummyRequest = dummy()
    for name in update:
        logger.info("Migrating schema for %s.", name)
        dummyRequest.form[name] = 1
    at.manage_updateSchema(update_all=1,
                           REQUEST=dummyRequest)
    transaction.savepoint(optimistic=True)


def migrate_old_content(site, logger):
    from collective.realestatebroker.migration import migrate
    result = migrate(site)
    logger.info(result)


def remove_upload_action(site, logger):
    atool = site.portal_actions
    # Note that this only works with a clean Plone 3 Site
    atool.deleteActions([0])
    logger.info('Removed legacy folderflashupload action from portal_actions')


def add_indexes(site, logger):
    """Add indexes needed by collective.realestatebroker

    If we have to add some code here to reindex our indexes after catalog.xml
    has been imported, we might as well add some code instead to only add them
    when they are not there yet.

    """
    catalog = getToolByName(site, 'portal_catalog')
    indexes = catalog.indexes()

    # fieldindexes
    for idx in ('getPrice', 'getCity','getHouse_type'):
        if idx not in indexes:
            catalog.addIndex(idx, 'FieldIndex')
            catalog.reindexIndex(idx,REQUEST=None)
            logger.info('Added FieldIndex for %s.', idx)

    # KeyordIndexes
    for idx in ('is_floorplan', ):
        if idx not in indexes:
            catalog.addIndex(idx, 'KeywordIndex')
            logger.info('Added KeywordIndex for %s.', idx)
