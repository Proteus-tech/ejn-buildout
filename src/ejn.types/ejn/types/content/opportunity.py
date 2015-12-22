"""Definition of the Program content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.configuration import zconf

from ejn.types import typesMessageFactory as _
from ejn.types.interfaces import IOpportunity
from ejn.types.config import PROJECTNAME

OpportunitySchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    atapi.TextField(
        'text',
        searchable=1,
        default_output_type='text/x-html-safe',
        widget=atapi.TinyMCEWidget(
            label=_(u'label_program_narrative', default=u"Opportunity Narrative"),
            rows=8,
            allow_file_upload=zconf.ATDocument.allow_document_upload,
        ),
    ),

    atapi.StringField(
        'linkURL',
        widget=atapi.StringWidget(
            label=_(u'label_link_URL', default=u"Link URL"),
        ),
    ),


))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

OpportunitySchema['title'].storage = atapi.AnnotationStorage()
OpportunitySchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(OpportunitySchema, moveDiscussion=False)


class Opportunity(base.ATCTContent):
    """EJN Opportunity"""
    implements(IOpportunity)

    meta_type = "Opportunity"
    schema = OpportunitySchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')


atapi.registerType(Opportunity, PROJECTNAME)
