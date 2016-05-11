from Products.CMFCore.utils import getToolByName
from Products.Archetypes.config import REFERENCE_CATALOG

from Products.Five.browser import BrowserView
from Acquisition import aq_inner
from zope.security import checkPermission


class GetRelatedProjectUIDsView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):

        relations = self.context.getParentProgram()

        uids = []

        for obj in relations:
            uids.append(obj.UID)

        return uids
