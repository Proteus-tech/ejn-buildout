"""Definition of the Slider Item content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

# -*- Message Factory Imported Here -*-

from zen.slideritem.interfaces import ISliderItem
from zen.slideritem.config import PROJECTNAME

OVERLAY_FORMATS = atapi.DisplayList((
  ('left', 'Left'),
  ('right', 'Right'),
))

SliderItemSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    atapi.ImageField('image',
               sizes= {'large'   : (960, 475),},
               widget = atapi.ImageWidget(
                        label= "Slider Image",
                        description = "Image dimensions: 960px x 475px",
                        show_content_type = False,)
               ),

    atapi.StringField('linkTarget',
              searchable=0,
              required = True,
              relationship='link_target',
              widget=atapi.StringWidget(label="Link Target")
              ),

    atapi.StringField('overlay',
             default = 'left',
             vocabulary=['left','right'],
             widget=atapi.SelectionWidget(label="Overlay format",
                                  description="Controls the presentation of the text overlay above the image",
                                  ),
             ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

SliderItemSchema['title'].storage = atapi.AnnotationStorage()
SliderItemSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(SliderItemSchema, moveDiscussion=False)


class SliderItem(base.ATCTContent):
    """Slider Item content-type"""
    implements(ISliderItem)

    meta_type = "SliderItem"
    schema = SliderItemSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(SliderItem, PROJECTNAME)
