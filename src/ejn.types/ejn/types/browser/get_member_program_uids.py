from Products.CMFCore.utils import getToolByName
from Products.Archetypes.config import REFERENCE_CATALOG

from Products.Five.browser import BrowserView
from Acquisition import aq_inner
from zope.security import checkPermission


class GetMemberProgramUIDsView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):

        reference_catalog = getToolByName(self, REFERENCE_CATALOG)

        relations = reference_catalog.getBackReferences(self.context,
                                                        relationship="relatesTo")

        projects = []

        for rel in relations:
            projects.append(rel.targetUID())
        return projects
