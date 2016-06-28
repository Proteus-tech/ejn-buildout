"""Definition of the Member Profile content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.configuration import zconf

import pytz

from ejn.types import typesMessageFactory as _
from ejn.types.vocabs import occupations
from ejn.types.vocabs import media_types
from ejn.types.vocabs import site_themes
from ejn.types.vocabs import sharing_roles
from ejn.types.vocabs import site_regions
from ejn.types.vocabs import genders

from ejn.types.interfaces import IMemberProfile
from ejn.types.config import PROJECTNAME

MemberProfileSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

  atapi.StringField('nameFirst',
            searchable=1,
            widget=atapi.StringWidget(label="First name"),
            ),

  atapi.StringField('nameLast',
            searchable=1,
            widget=atapi.StringWidget(label="Last name",
                                      description="Surname or Family Name",),
            ),

  atapi.ImageField('image',
             languageIndependent=True,
             swallowResizeExceptions = zconf.swallowImageResizeExceptions.enable,
             pil_quality = zconf.pil_config.quality,
             pil_resize_algo = zconf.pil_config.resize_algo,
             max_size = zconf.ATImage.max_image_dimension,
             sizes= {'large'   : (768, 768),
                     'preview' : (400, 400),
                     'mini'    : (200, 200),
                     'thumb'   : (128, 128),
                     'tile'    :  (64, 64),
                     'icon'    :  (32, 32),
                     'listing' :  (16, 16),
                    },
             widget = atapi.ImageWidget(
                      description = "",
                      label= "Image",
                      label_msgid = "label_image",
                      i18n_domain = "plone",
                      show_content_type = False,)
  ),

  atapi.TextField(
      'profile',
      searchable=1,
      default_output_type='text/x-html-safe',
      widget=atapi.TinyMCEWidget(
          label=_(u'label_biography_profile', default=u"Biography/Profile"),
          rows=8,
          allow_file_upload=zconf.ATDocument.allow_document_upload,
      ),
  ),

  atapi.LinesField('interests',
           vocabulary=site_themes,
           index='KeywordIndex',
           multiValued=True,
           widget=atapi.MultiSelectionWidget(label="Area of Environmental Journalism Interest",
                                format='checkbox',
                                description="",
                                ),
           ),

  atapi.LinesField('regions_of_interests',
           vocabulary=site_regions,
           index='KeywordIndex',
           multiValued=True,
           widget=atapi.MultiSelectionWidget(label="Regions of Interest",
                                format='checkbox',
                                description="",
                                ),
           ),

  atapi.StringField('gender',
            widget=atapi.SelectionWidget(label="Gender"),
            vocabulary=genders,
            ),

  atapi.DateTimeField('dateOfBirth',
            searchable=1,
            widget=atapi.CalendarWidget(label="Date of Birth",
                                        show_hm = False,
                                        ),
            ),

  atapi.IntegerField('birthYear',
            widget=atapi.IntegerWidget(label="Birth Year",),
            ),

  atapi.StringField('occupation',
            widget=atapi.SelectionWidget(label="Occupation"),
            schemata='professional info',
            vocabulary=occupations,
            ),

  atapi.StringField('jobTitle',
            searchable=1,
            widget=atapi.StringWidget(label="Job title",),
            ),

  atapi.StringField('organization',
            widget=atapi.StringWidget(label="Organization name"),
            schemata='professional info',
            ),

  atapi.TextField('orgURL',
             widget=atapi.StringWidget(label="Organization website"),
             schemata='professional info',
             ), 

  atapi.StringField('country',
             searchable=1,
             widget=atapi.StringWidget(label="Organization country"),
             schemata='professional info',
             ),

  atapi.LinesField('mediaTypes',
            widget=atapi.MultiSelectionWidget(label="Media type",
                                              format="checkbox"),
            vocabulary=media_types,
            multiValued=True,
            schemata='professional info',
            ),

  atapi.StringField('audience',
            widget=atapi.StringWidget(label="Circulation/audience size"),
            schemata='professional info',
            ),

  atapi.StringField('city',
             searchable=1,
             widget=atapi.StringWidget(label="City"),
             schemata='professional info',
             ),

  atapi.StringField('country',
             searchable=1,
             widget=atapi.StringWidget(label="Country"),
             schemata='professional info',
             ),


  atapi.StringField('citizenship',
            widget=atapi.StringWidget(label="Country of Citizenship"),
            schemata='professional info',
            ),

  atapi.StringField('countriesOfResidence',
            widget=atapi.StringWidget(label="Country of Residence"),
            schemata='professional info',
            ),

  atapi.StringField('languagesSpoken',
            widget=atapi.StringWidget(label="Languages"),
            schemata='professional info',
            ),

  atapi.BooleanField('passport',
              widget=atapi.BooleanWidget(label="Valid passport"),
              schemata='professional info',
              ),

  atapi.StringField('phone',
            searchable=1,
            widget=atapi.StringWidget(label="Phone Number"),
            schemata='contact',
            ),

  atapi.StringField('phoneTwo',
            searchable=1,
            widget=atapi.StringWidget(label="Secondary Phone Number"),
            schemata='contact',
            ),

  atapi.StringField('fax',
            schemata='contact',
            ),

  atapi.StringField('email',
            schemata='contact',
            ),

  atapi.TextField('personalURL',
             widget=atapi.StringWidget(label="Personal URL"),
             schemata='contact',
             ), 

  atapi.StringField('skypeUser',
            searchable=1,
            widget=atapi.StringWidget(label="Skype username"),
            schemata='contact',
            ),

  atapi.StringField('twitterUser',
            searchable=1,
            widget=atapi.StringWidget(label="Twitter username"),
            schemata='contact',
            ),

  atapi.StringField('twitterUser',
            searchable=1,
            widget=atapi.StringWidget(label="Twitter username"),
            schemata='contact',
            ),

  atapi.StringField('comNetworkOther',
            widget=atapi.StringWidget(
                               label="Other Communication Network",
                               description="e.g. WeChat, Telegram, etc.  Use the next for your username"),
            schemata='contact',
            ),

  atapi.StringField('comNetworkOtherID',
            widget=atapi.StringWidget(label="Other Communication Network User ID"),
            schemata='contact',
            ),

  atapi.StringField('preferredCommunication',
            widget=atapi.StringWidget(label="Preferred Contact Method"),
            schemata='contact',
            ),

  atapi.StringField('timezoneName',
            widget=atapi.SelectionWidget(label="Timezone"),
            schemata='contact',
            vocabulary=pytz.all_timezones,
            ),

  atapi.StringField('timezoneNum',
            widget=atapi.StringWidget(label="Timezone integer"),
            schemata='contact',
            ),

  atapi.StringField(
      'bioSharing',
      vocabulary=sharing_roles,
      default='EJN staff',
      widget=atapi.SelectionWidget(
          label="Biography Section Sharing",
          description="",
          ),
      ),

  atapi.StringField(
      'proSharing',
      vocabulary=sharing_roles,
      default='EJN staff',
      widget=atapi.SelectionWidget(
          label="Professional Section Sharing",
          description="",
          ),
      ),

  atapi.StringField(
      'contactSharing',
      vocabulary=sharing_roles,
      default='EJN staff',
      widget=atapi.SelectionWidget(
          label="Contact Section Sharing",
          description="",
          ),
      ),

   atapi.StringField('sourceUID',
             schemata='categorization',
             ),

   atapi.StringField('sourceNID',
             schemata='categorization',
             ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

MemberProfileSchema['title'].storage = atapi.AnnotationStorage()
MemberProfileSchema['description'].storage = atapi.AnnotationStorage()
MemberProfileSchema['subject'].widget.label = 'Other interests'

MemberProfileSchema['title'].widget.visible={'edit':'hidden', 'view':'hidden'}
MemberProfileSchema['title'].required=False
MemberProfileSchema['description'].widget.visible={'edit':'hidden', 'view':'hidden'}
MemberProfileSchema['dateOfBirth'].widget.visible={'edit':'hidden', 'view':'hidden'}
MemberProfileSchema['citizenship'].widget.visible={'edit':'hidden', 'view':'hidden'}
MemberProfileSchema['countriesOfResidence'].widget.visible={'edit':'hidden', 'view':'hidden'}
MemberProfileSchema['phoneTwo'].widget.visible={'edit':'hidden', 'view':'hidden'}
MemberProfileSchema['fax'].widget.visible={'edit':'hidden', 'view':'hidden'}
MemberProfileSchema['timezoneNum'].widget.visible={'edit':'hidden', 'view':'hidden'}


schemata.finalizeATCTSchema(MemberProfileSchema, moveDiscussion=False)

MemberProfileSchema.changeSchemataForField('subject', 'default') 
MemberProfileSchema.moveField('subject', after='interests')


class MemberProfile(base.ATCTContent):
    """EJN Member Profile"""
    implements(IMemberProfile)

    meta_type = "MemberProfile"
    schema = MemberProfileSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    def Title(self, **kwargs):
        return "%s %s" %(self.getNameFirst(), self.getNameLast())

atapi.registerType(MemberProfile, PROJECTNAME)
