# -*- coding: utf-8 -*-

from . import _
from .utils import get_funding_types
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implementer
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


@implementer(IVocabularyFactory)
class FundingRegisteredTypesVocabulary(object):
    """All of the dexterity IFundingReqBase registered
    """

    def __call__(self, context):
        terms = [SimpleTerm(value='', token='',
                            title=_(u'-- nothing --')),
                 ]
        terms.extend([
            SimpleTerm(
                value=t.id, token=t.id,
                title=t.getProperty('title')
            ) for t in get_funding_types(context)
        ])
        return SimpleVocabulary(terms)


fundingRegisteredTypesFactory = FundingRegisteredTypesVocabulary()
