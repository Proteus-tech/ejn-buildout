from Products.CMFCore.utils import getToolByName
from Products.Archetypes.config import REFERENCE_CATALOG

from Products.Five.browser import BrowserView
from Acquisition import aq_inner
from zope.security import checkPermission


class GetProjectTeamUIDsView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):

      reference_catalog = getToolByName(self, REFERENCE_CATALOG)

      relations = reference_catalog.getReferences(self.context,
                                                      relationship="relatesTo")

      team = []

      for rel in relations:
          team.append(rel.targetUID)

      return team
