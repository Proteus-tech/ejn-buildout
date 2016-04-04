# -*- coding: utf-8 -*-
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
import pycountry


@implementer(IVocabularyFactory)
class CountriesVocabulary(object):
    """Vocabulary factory for countries"""
    def __call__(self, context):
            items = [SimpleTerm(x.alpha2.encode('utf-8'), x.name.encode('utf-8'))
                     for x in pycountry.countries]
            items = [SimpleTerm(None,'Select a country...')] + items
            return SimpleVocabulary(items)

CountriesVocabularyFactory = CountriesVocabulary()
