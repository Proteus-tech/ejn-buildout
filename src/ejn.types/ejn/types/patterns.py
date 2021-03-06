import json
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.patterns import PloneSettingsAdapter
from plone.uuid.interfaces import IUUID


class EJNSettingsAdapter(PloneSettingsAdapter):

    DEFAULT_UPLOAD_FOLDER = 'images'

    def tinymce(self):
        purl = getToolByName(self.context, 'portal_url')
        options = super(EJNSettingsAdapter, self).tinymce()
        portal = purl.getPortalObject()

        try:
            folder = portal.restrictedTraverse(self.DEFAULT_UPLOAD_FOLDER)
        except KeyError:
            pass
        else:
            tiny_options = json.loads(options['data-pat-tinymce'])
            tiny_options['upload']['initialFolder'] = IUUID(folder)
            tiny_options['upload']['currentPath'] = '/' + \
                self.DEFAULT_UPLOAD_FOLDER
            options['data-pat-tinymce'] = json.dumps(tiny_options)
        return options
