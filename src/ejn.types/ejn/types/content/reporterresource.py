"""Definition of the Reporter Resource content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.configuration import zconf

from ejn.types import typesMessageFactory as _
from ejn.types.vocabs import site_themes
from ejn.types.vocabs import site_regions
from ejn.types.interfaces import IReporterResource
from ejn.types.config import PROJECTNAME

ReporterResourceSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    atapi.TextField(
        'text',
        searchable=1,
        default_output_type='text/x-html-safe',
        widget=atapi.TinyMCEWidget(
            label=_(u'label_story_text', default=u"Story Text"),
            rows=8,
            allow_file_upload=zconf.ATDocument.allow_document_upload,
        ),
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

ReporterResourceSchema['title'].storage = atapi.AnnotationStorage()
ReporterResourceSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(ReporterResourceSchema, moveDiscussion=False)

ReporterResourceSchema.changeSchemataForField('location', 'default') 
ReporterResourceSchema.moveField('location', after='publisher')

ReporterResourceSchema.changeSchemataForField('subject', 'default') 
ReporterResourceSchema.moveField('subject', after='themes')

class ReporterResource(base.ATCTContent):
    """Reporter Resource"""
    implements(IReporterResource)

    meta_type = "ReporterResource"
    schema = ReporterResourceSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(ReporterResource, PROJECTNAME)
