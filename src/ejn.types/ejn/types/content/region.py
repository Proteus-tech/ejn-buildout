"""Definition of the Region content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.configuration import zconf

from ejn.types.vocabs import site_regions
from ejn.types import typesMessageFactory as _
from ejn.types.interfaces import IRegion
from ejn.types.config import PROJECTNAME

RegionSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    atapi.TextField(
        'text',
        searchable=1,
        default_output_type='text/x-html-safe',
        widget=atapi.TinyMCEWidget(
            label=_(u'label_intro_text', default=u"Intro Text"),
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

    atapi.LinesField('region',
            vocabulary=site_regions,
            index='FieldIndex',
            multiValued=False,
            widget=atapi.SelectionWidget(label="Region",
                                 description="",
                                 ),
            ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

RegionSchema['title'].storage = atapi.AnnotationStorage()
RegionSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(RegionSchema, moveDiscussion=False)


class Region(base.ATCTContent):
    """Geographical Region"""
    implements(IRegion)

    meta_type = "Region"
    schema = RegionSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')


atapi.registerType(Region, PROJECTNAME)
