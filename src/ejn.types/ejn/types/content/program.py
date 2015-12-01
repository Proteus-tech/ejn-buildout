"""Definition of the Program content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.configuration import zconf

from ejn.types.vocabs import ejn_programs
from ejn.types import typesMessageFactory as _
from ejn.types.interfaces import IProgram
from ejn.types.config import PROJECTNAME

ProgramSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    atapi.TextField(
        'text',
        searchable=1,
        default_output_type='text/x-html-safe',
        widget=atapi.TinyMCEWidget(
            label=_(u'label_program_narrative', default=u"Program Narrative"),
            rows=8,
            allow_file_upload=zconf.ATDocument.allow_document_upload,
        ),
    ),

    atapi.StringField(
        'sourceUID',
        schemata='categorization',
    ),

    atapi.LinesField(
        'program',
        vocabulary=ejn_programs,
        index='KeywordIndex',
        multiValued=True,
        widget=atapi.MultiSelectionWidget(
            label="Program",
            format='checkbox',
            description="",
            ),
    ),

    atapi.ReferenceField(
        'people',
        widget=atapi.MultiSelectionWidget(label='People'),
        allowed_types=('Member Profile'),
        relationship='program person',
        multiValued=True,
        vocabulary_display_path_bound=-1,
    ),

    atapi.ReferenceField(
        'parentProgram',
        widget=atapi.MultiSelectionWidget(label='Parent Program'),
        allowed_types=('Program'),
        relationship='parent program',
        multiValued=True,
        vocabulary_display_path_bound=-1,
    ),

    atapi.ImageField(
        'image',
        sizes={
            'large': (768, 768),
            'foursixeight': (468, 468),
            'preview': (400, 400),
            'threetwosix': (326, 326),
            'twotwoeight': (228, 228),
            'mini': (200, 200),
            'thumb': (128, 128),
            'tiny': (84, 84),
            'tile': (64, 64),
        },
        widget=atapi.ImageWidget(
            label="Image",
            description="",
            show_content_type=False,)
    ),
))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

ProgramSchema['title'].storage = atapi.AnnotationStorage()
ProgramSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(ProgramSchema, moveDiscussion=False)

ProgramSchema.changeSchemataForField('location', 'default')
ProgramSchema.moveField('location', after='text')


class Program(base.ATCTContent):
    """EJN Program"""
    implements(IProgram)

    meta_type = "Program"
    schema = ProgramSchema

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    def progs(self):
        return self.getProgram()

atapi.registerType(Program, PROJECTNAME)
