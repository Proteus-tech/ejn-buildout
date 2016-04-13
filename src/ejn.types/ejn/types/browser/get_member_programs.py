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

        projects = []
        relations = catalog.findRelations(
            dict(
                to_id=intids.getId(aq_inner(self.context)),
                from_attribute='relatedItems')
        )
        for rel in relations:
                obj = intids.queryObject(rel.from_id)
                if obj is not None and checkPermission('zope2.View', obj):
                    projects.append(obj)
        return projects
