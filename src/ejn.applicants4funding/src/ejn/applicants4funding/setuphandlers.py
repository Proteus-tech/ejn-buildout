# -*- coding: utf-8 -*-

from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from Products.CMFCore.utils import getToolByName
from . import logger


# from : http://maurits.vanrees.org/weblog/archive/2009/12/catalog
def addKeyToCatalog(portal):
    '''Takes portal_catalog and adds a key to it
    @param portal: context providing portal_catalog
    '''

    catalog = getToolByName(portal, 'portal_catalog')
    indexes = catalog.indexes()
    # Specify the indexes you want, with ('index_name', 'index_type')

    indexables = []

    WANTED_INDEXES = (('fundingCategory', 'FieldIndex'),)

    for name, meta_type in WANTED_INDEXES:
        if name not in indexes:
            catalog.addIndex(name, meta_type)
            indexables.append(name)
            logger.info("Added %s for field %s.", meta_type, name)
    if len(indexables) > 0:
        logger.info("Indexing new index: %s.", ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'ejn.applicants4funding:uninstall',
        ]


def post_install(context):
    """Post install script"""
    if context.readDataFile('ejnapplicants4funding_default.txt') is None:
        return
    portal = context.getSite()
    addKeyToCatalog(portal)
    logger.info('Finished')


def uninstall(context):
    """Uninstall script"""
    if context.readDataFile('ejnapplicants4funding_uninstall.txt') is None:
        return
    # Do something during the uninstallation of this package
