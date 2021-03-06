from Products.CMFCore.utils import getToolByName
from Products.Archetypes.config import REFERENCE_CATALOG

from Products.Five.browser import BrowserView
from Acquisition import aq_inner
from zope.security import checkPermission


class GetRelatedProjectsView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):

        relations = self.context.getParentProgram()

        projects = []

        for obj in relations:
            if obj is not None and checkPermission('zope2.View', obj):
                projects.append(obj)
        return projects
