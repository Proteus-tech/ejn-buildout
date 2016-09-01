# -*- coding: utf-8 -*-

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from Products.Archetypes import atapi
from Products.PloneFormGen.interfaces import IPloneFormGenForm
from zope.component import adapts
from zope.interface import implementer
from .interfaces import IEjnApplicants4FundingLayer


class ExtensionSelectField(ExtensionField, atapi.StringField):
    """ Retrofitted string field """


@implementer(IBrowserLayerAwareExtender)
class PFGExtender(object):
    """Add the EJN funding category to FormFolder"""
    adapts(IPloneFormGenForm)
    layer = IEjnApplicants4FundingLayer

    fields = [
        ExtensionSelectField("fundingCategory",
            vocabulary_factory='ejn.applicants4funding.fundingRegisteredTypes',
            enforceVpcabulary=True,
            widget = atapi.SelectWidget(
                label="EJN funding category",
                description=(u"Only use this if this PloneFormGen will be used "
                             u"for make calls for funding"),
            ),
        )
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
