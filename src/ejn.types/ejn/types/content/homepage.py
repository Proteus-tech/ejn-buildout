"""Definition of the Homepage content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from ejn.types.vocabs import site_themes
from ejn.types.vocabs import site_regions

from ejn.types.interfaces import IHomepage
from ejn.types.config import PROJECTNAME

HomepageSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

  atapi.LinesField('themes',
           vocabulary=site_themes,
           index='KeywordIndex',
           multiValued=True,
           widget=atapi.MultiSelectionWidget(label="Themes",
                                format='checkbox',
                                description="",
                                ),
           ),

  atapi.LinesField('regions',
           vocabulary=site_regions,
           index='KeywordIndex',
           multiValued=True,
           widget=atapi.MultiSelectionWidget(label="Regions",
                                format='checkbox',
                                description="",
                                ),
           ),


  atapi.ReferenceField('program',
            widget=atapi.SelectionWidget(label='Program'),
            allowed_types=('Program'),
            relationship='display program',
            multiValued=0,
            vocabulary_display_path_bound=-1,
            ),

  atapi.StringField('memberJournalists',
            widget=atapi.StringWidget(label="Member Journalists"),
            ),

  atapi.StringField('trainedJournalists',
            widget=atapi.StringWidget(label="Journalists Trained"),
            ),

  atapi.StringField('storiesPublished',
            widget=atapi.StringWidget(label="Stories Published"),
            ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

HomepageSchema['title'].storage = atapi.AnnotationStorage()
HomepageSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(HomepageSchema, moveDiscussion=False)


class Homepage(base.ATCTContent):
    """Home page"""
    implements(IHomepage)

    meta_type = "Homepage"
    schema = HomepageSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Homepage, PROJECTNAME)
