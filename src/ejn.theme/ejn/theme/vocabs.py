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
            items = []
            for country in pycountry.countries:
                value = country.alpha2.encode('utf-8')
                title = 'Taiwan' in country.name and 'Taiwan' or country.name
                title = title.encode('utf-8')
                items.append(SimpleTerm(value, title))
#            items = [SimpleTerm(x.alpha2.encode('utf-8'), x.name.encode('utf-8'))
#                     for x in countries]
            items = [SimpleTerm(None,'Select a country...')] + items
            return SimpleVocabulary(items)

CountriesVocabularyFactory = CountriesVocabulary()
