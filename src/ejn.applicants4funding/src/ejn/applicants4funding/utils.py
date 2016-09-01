# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName


def get_funding_types(context):
    """Get all of the FTI types that are funding"""
    types_tool = getToolByName(context, 'portal_types')
    return [
        t for t in types_tool.objectValues()
        if t.meta_type == 'Dexterity FTI' and
        t.getProperty('klass') == 'ejn.applicants4funding.content.FundingReqBase'
    ]
