#from Products.CMFCore.utils import getToolByName
#from collective.realestatebroker import config


def importVarious(context):
    """This is the main step that is called by genericsetup."""
    # Only run step if a flag file is present, otherwise it run every time
    # that generic setup runs all steps of *any* profile.
    if context.readDataFile('realestatebroker.txt') is None:
        return
    site = context.getSite()
    logger = context.getLogger('realestatebroker')
    migrate_old_content(site, logger)

def migrate_old_content(site, logger):
    try:
        import Products.contentmigration
        Products.contentmigration # PYFLAKES
    except:
        return
    from collective.realestatebroker.migration import migrate
    result = migrate(site)
    logger.info(result)
