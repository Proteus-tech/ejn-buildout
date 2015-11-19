"""Definition of the Story content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from ejn.types.vocabs import site_themes
from ejn.types.vocabs import site_regions

# -*- Message Factory Imported Here -*-

from ejn.types.interfaces import IStory
from ejn.types.config import PROJECTNAME

StorySchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

  atapi.TextField('text',
            searchable=1,
            default_output_type = 'text/x-html-safe',
            widget=atapi.RichWidget(label="Story Text"),
            ),

    atapi.ImageField('image',
              sizes= {'large'  : (768, 768),
                     'preview' : (400, 400),
                     'twoeightfive' : (285, 285),
                     'mini'    : (200, 200),
                     'thumb'   : (128, 128),
                     'tiny'    :  (84, 84),
                     'tile'    :  (64, 64),
                    },
               widget = atapi.ImageWidget(
                        label= "Image",
                        description = "",
                        show_content_type = False,)
               ),

    atapi.ImageField('imageHome',
              sizes= {'twosixtyeight' : (268, 268),
                      'mini'    : (200, 200),
                      'thumb'   : (128, 128),
                      'tile'    :  (64, 64),
                    },
               widget = atapi.ImageWidget(
                        label= "Homepage image (16:9)",
                        description = "Dimensions: 268px x 150px",
                        show_content_type = False,)
               ),


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


  atapi.StringField('publisher',
            searchable=1,
            ),

  atapi.StringField('publisherURL',
            searchable=1,
            ),

  atapi.StringField('byline',
            searchable=1,
            ),

  atapi.DateTimeField('pubDateOriginal',
           widget=atapi.CalendarWidget(label="Publication date",
                                description="",
                                show_hm = False,
                                ),
           ),


  atapi.ReferenceField('program',
            widget=atapi.SelectionWidget(label='Program'),
            allowed_types=('Program'),
            relationship='under program',
            multiValued=0,
            vocabulary_display_path_bound=-1,
            ),

   atapi.StringField('sourceUID',
             schemata='categorization',
             ),

   atapi.StringField('authorUID',
             schemata='categorization',
             ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

StorySchema['title'].storage = atapi.AnnotationStorage()
StorySchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(StorySchema, moveDiscussion=False)

StorySchema.changeSchemataForField('location', 'default') 
StorySchema.moveField('location', after='publisher')

StorySchema.changeSchemataForField('subject', 'default') 
StorySchema.moveField('subject', after='themes')

class Story(base.ATCTContent):
    """EJN Program Story"""
    implements(IStory)

    meta_type = "Story"
    schema = StorySchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Story, PROJECTNAME)
