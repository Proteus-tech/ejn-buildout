from Products.CMFCore.utils import getToolByName
from Products.Archetypes.config import REFERENCE_CATALOG

from Products.Five.browser import BrowserView
from Acquisition import aq_inner
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from zc.relation.interfaces import ICatalog


class GetMemberProgramsView(BrowserView):

    def __call__(self):
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)

        reference_catalog = getToolByName(self, REFERENCE_CATALOG)

        relations = reference_catalog.getBackReferences(self,
                                                        relationship="relatesTo")

        projects = []

        for rel in relations:
                obj = rel.getSourceObject()
                if obj is not None and checkPermission('zope2.View', obj):
                    projects.append(obj)
        return projects
