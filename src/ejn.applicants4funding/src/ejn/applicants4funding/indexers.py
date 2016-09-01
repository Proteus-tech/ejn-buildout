# -*- coding: utf-8 -*-

from zope.interface import Interface
from Products.PloneFormGen.interfaces import IPloneFormGenForm
from plone.indexer import indexer


@indexer(Interface)
def default_funding_category(object):
    raise AttributeError()


@indexer(IPloneFormGenForm)
def pfg_funding_category(object):
    field = object.getField('fundingCategory')
    if not field:
        raise AttributeError()
    return field.get(object)
