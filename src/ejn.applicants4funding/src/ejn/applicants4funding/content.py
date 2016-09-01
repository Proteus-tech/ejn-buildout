# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from zope.interface import implements
from .interfaces import IFundingReqBase


# Although this is a dexterity content type, it's not registered as portal type
# You must use this as base class for TTW created types

class FundingReqBase(Container):
    implements(IFundingReqBase)
