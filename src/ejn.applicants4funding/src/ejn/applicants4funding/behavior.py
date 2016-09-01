# -*- coding: utf-8 -*-

from plone import api
from zope.component import adapter
from zope.i18nmessageid import MessageFactory
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.globalrequest import getRequest
from zope.interface import provider
from zope.interface import implementer
from . import _


def _get_data(profile, fieldName):
    field = profile.getField(fieldName)
    if not field:
        return None
    return field.get(profile).decode('utf-8')


def _default_from_profile(fieldName):
    user = api.user.get_current()
    catalog = api.portal.get_tool(name='portal_catalog')
    userid = user.getUserName()
    profile = catalog(
        portal_type='Member Profile', Creator=userid,
        sort_on='created',
    )
    if profile:
        return _get_data(profile[0].getObject(), fieldName)
    email = user.getProperty('email')
    profile = catalog(
        portal_type='Member Profile', email=email,
        sort_on='created',
    )
    if profile:
        return _get_data(profile[0].getObject(), fieldName)


@provider(IFormFieldProvider)
class IEJNFunding(model.Schema):

    nameFirst = schema.TextLine(
        title=_('First name'),
        defaultFactory=lambda: _default_from_profile('nameFirst')
    )

    nameLast = schema.TextLine(
        title=_('Last name'),
        defaultFactory=lambda: _default_from_profile('nameLast')
    )


@implementer(IEJNFunding)
@adapter(IDexterityContent)
class EJNFunding(object):

    def __init__(self, context):
        self.context = context
