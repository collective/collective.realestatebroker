from Products.CMFCore.utils import getToolByName


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
    for idx in ('getPrice', 'getCity'):
        if idx not in indexes:
            catalog.addIndex(idx, 'FieldIndex')
            logger.info('Added FieldIndex for %s.', idx)

    # KeyordIndexes
    for idx in ('is_floorplan', ):
        if idx not in indexes:
            catalog.addIndex(idx, 'KeywordIndex')
            logger.info('Added KeywordIndex for %s.', idx)
