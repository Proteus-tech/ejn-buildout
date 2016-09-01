# -*- coding: utf-8 -*-

from plone import api
from plone.dexterity.browser.view import DefaultView
from Products.PloneFormGen.interfaces import IPloneFormGenForm
from ..utils import get_funding_types


class FundingBaseView(DefaultView):

    def related_forms(self):
        context = self.context
        catalog = api.portal.get_tool(name='portal_catalog')
        funding_types = get_funding_types(context)
        forms = catalog(
            object_provides=IPloneFormGenForm.__identifier__,
            #fundingCategory=[t.id for t in funding_types]
            fundingCategory=context.portal_type
        )
        links = []
        for form in forms:
            applicant = catalog(
                portal_type='FundingReq',
                path=form.getPath(),
                creator=context.Creator(),
                sort_on='created'
            )
            if applicant:
                app = applicant[0]
                links.append(dict(
                    title='%s (%s)' % (form.Title, app.Title),
                    url=app.getURL() + '/edit',
                ))
            else:
                links.append(dict(
                    title=form.Title,
                    url=form.getURL(),
                ))
        return links
