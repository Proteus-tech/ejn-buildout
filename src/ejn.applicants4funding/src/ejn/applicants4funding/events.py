# -*- coding: utf-8 -*-

from plone import api
from zExceptions import Forbidden
from .interfaces import IFundingReqBase



def funding_added(context, event):
    catalog = api.portal.get_tool(name='portal_catalog')
    user = api.user.get_current()
    userid = user.getUserName()
    portal_type = context.portal_type
    results = catalog(
        portal_type=portal_type,
        Creator=userid
    )
    if results.actual_result_count > 1:
        message = 'User %s already have a %s content' % (
            userid, portal_type
        )
        api.portal.show_message(
            message=message, request=context.REQUEST,
            type='error'
        )
        # transaction.abort()
        raise(Forbidden(message))
