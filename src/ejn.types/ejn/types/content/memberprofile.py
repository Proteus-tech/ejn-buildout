"""Definition of the Member Profile content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.configuration import zconf

from ejn.types.vocabs import occupations
from ejn.types.vocabs import media_types
from ejn.types.vocabs import site_themes

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

  atapi.StringField('phone',
            searchable=1,
            widget=atapi.StringWidget(label="Phone Number"),
            ),

  atapi.StringField('phoneTwo',
            searchable=1,
            widget=atapi.StringWidget(label="Secondary Phone Number"),
            ),

  atapi.StringField('fax'),

  atapi.StringField('email'),

  atapi.TextField('personalURL',
             widget=atapi.StringWidget(label="Personal URL")
             ), 

  atapi.TextField('mediaHouse',
             widget=atapi.StringWidget(label="Media House")
             ), 

  atapi.TextField('mediaHouseURL',
             widget=atapi.StringWidget(label="Media House website")
             ), 

  atapi.StringField('address',
             widget=atapi.StringWidget(label="Media House Address"),
             ),
             
  atapi.StringField('addressTwo',
             widget=atapi.StringWidget(label="Media House Address Line 2"),
             ),
             
  atapi.StringField('city',
             searchable=1,
             widget=atapi.StringWidget(label="Media House City"),
             ),
             
  atapi.StringField('stateProv',
             searchable=1,
             widget=atapi.StringWidget(label="Media House State/Provence"),
             ),
             
  atapi.StringField('postalCode',
             searchable=1,
             widget=atapi.StringWidget(label="Media House Zip/Postal Code"),
             ),
             
  atapi.StringField('country',
             searchable=1,
             widget=atapi.StringWidget(label="Media House Country"),
             ),

  atapi.StringField('skypeUser',
            searchable=1,
            widget=atapi.StringWidget(label="Skype username"),
            ),

  atapi.StringField('twitterUser',
            searchable=1,
            widget=atapi.StringWidget(label="Twitter username"),
            ),

  atapi.DateTimeField('dateOfBirth',
            searchable=1,
            widget=atapi.CalendarWidget(label="Date of Birth",
                                        show_hm = False,
                                        ),
            ),

  atapi.StringField('gender',
            widget=atapi.StringWidget(label="Gender"),
            ),

  atapi.StringField('citizenship',
            widget=atapi.StringWidget(label="Country of Citizenship"),
            ),

  atapi.StringField('countriesOfResidence',
            widget=atapi.StringWidget(label="Country of Residence"),
            ),

  atapi.StringField('languagesSpoken',
            widget=atapi.StringWidget(label="Languages"),
            ),

  atapi.BooleanField('passport',
              widget=atapi.BooleanWidget(label="Holds a passport valid?"),
              ),

  atapi.StringField('timezoneName',
            widget=atapi.StringWidget(label="Timezone"),
            ),

  atapi.StringField('timezoneNum',
            widget=atapi.StringWidget(label="Timezone integer"),
            schemata='categorization',
            ),

  atapi.TextField('profile',
            searchable=1,
            widget=atapi.RichWidget(label="Biography/Profile"),
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

  atapi.LinesField('interests',
           vocabulary=site_themes,
           index='KeywordIndex',
           multiValued=True,
           widget=atapi.MultiSelectionWidget(label="Area of Environmental Journalism Interest",
                                format='checkbox',
                                description="",
                                ),
           ),

  atapi.StringField('interests_extra',
            widget=atapi.StringWidget(label="Additional Areas of Environmental Journalism Interest"),
            ),

  atapi.StringField('occupation',
            widget=atapi.SelectionWidget(label="Occupation"),
            schemata='professional info',
            vocabulary=occupations,
            ),

  atapi.StringField('organization',
            widget=atapi.StringWidget(label="Organization name"),
            schemata='professional info',
            ),

  atapi.LinesField('mediaTypes',
            widget=atapi.MultiSelectionWidget(label="Media type"),
            vocabulary=media_types,
            multiValued=True,
            schemata='professional info',
            ),

  atapi.StringField('audience',
            widget=atapi.StringWidget(label="Circulation/audience size"),
            schemata='professional info',
            ),

  atapi.TextField('orgURL',
             widget=atapi.StringWidget(label="Organization website"),
             schemata='organization',
             ), 

  atapi.StringField('phoneOrg',
            searchable=1,
            widget=atapi.StringWidget(label="Phone Number"),
            schemata='organization',
            ),

  atapi.StringField('addressOrg',
             widget=atapi.StringWidget(label="Address"),
             schemata='organization',
             ),
             
  atapi.StringField('addressTwoOrg',
             widget=atapi.StringWidget(label="Address Line 2"),
             schemata='organization',
             ),
             
  atapi.StringField('cityOrg',
             searchable=1,
             widget=atapi.StringWidget(label="City"),
             schemata='organization',
             ),
             
  atapi.StringField('stateProvOrg',
             searchable=1,
             widget=atapi.StringWidget(label="State/Provence"),
             schemata='organization',
             ),
             
  atapi.StringField('postalCodeOrg',
             searchable=1,
             widget=atapi.StringWidget(label="Zip/Postal Code"),
             schemata='organization',
             ),
             
  atapi.StringField('countryOrg',
             searchable=1,
             widget=atapi.StringWidget(label="Country"),
             schemata='organization',
             ),

  atapi.StringField('periodicity',
            widget=atapi.StringWidget(label="Periodicity"),
            schemata='organization',
            ),

  atapi.StringField('circulation',
            widget=atapi.StringWidget(label="Circulation/audience size"),
            schemata='organization',
            ),

  atapi.StringField('nameSupervisor',
            searchable=1,
            widget=atapi.StringWidget(label="Supervisor's Name"),
            schemata='organization',
            ),

  atapi.StringField('phoneSupervisor',
            searchable=1,
            widget=atapi.StringWidget(label="Supervisor's Phone Number"),
            schemata='organization',
            ),

  atapi.StringField('emailSupervisor',
            searchable=1,
            widget=atapi.StringWidget(label="Supervisor's email"),
            schemata='organization',
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
        return self.getNameLast() + ", " + self.getNameFirst()

atapi.registerType(MemberProfile, PROJECTNAME)
