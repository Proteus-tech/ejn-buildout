# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IEjnApplicants4FundingLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IFundingReqBase(Interface):
    """Marker interface for funding request content type"""
