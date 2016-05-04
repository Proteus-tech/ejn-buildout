from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from plone import api


class GetPermsForContext(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        bioSharing = self.context.getBioSharing()
        proSharing = self.context.getProSharing()
        contactSharing = self.context.getContactSharing()

        current = api.user.get_current()
        location = current.getProperty('username')
        creator = self.context.Creator()
        
        ugroups = api.group.get_groups(username=userid)

        results = {}

        results['user'] = userid
        results['groups'] = ugroups
        results['creator'] = creator

        if userid == creator:
          results['bioSharing'] = True
          results['proSharing'] = True
          results['contactSharing'] = True
          return results
        else:
          pass

        if bioSharing == 'Public':
          results['bioSharing'] = True
        elif bioSharing == 'Unverified EJN members':
          if member is not None:
            results['bioSharing'] = True
          else:
            results['bioSharing'] = False
        elif bioSharing == 'Verified journalists':
          if 'verified-journalists' in ugroups:
            results['bioSharing'] = True
          else:
            results['bioSharing'] = False
        else:
          if 'ejn-staff' in ugroups:
            results['bioSharing'] = True
          else:
            results['bioSharing'] = False


        if proSharing == 'Public':
          results['proSharing'] = True
        elif proSharing == 'Unverified EJN members':
          if member is not None:
            results['proSharing'] = True
          else:
            results['proSharing'] = False
        elif proSharing == 'Verified journalists':
          if 'verified-journalists' in ugroups:
            results['proSharing'] = True
          else:
            results['proSharing'] = False
        else:
          if 'ejn-staff' in ugroups:
            results['proSharing'] = True
          else:
            results['proSharing'] = False


        if contactSharing == 'Public':
          results['contactSharing'] = True
        elif contactSharing == 'Unverified EJN members':
          if member is not None:
            results['contactSharing'] = True
          else:
            results['contactSharing'] = False
        elif contactSharing == 'Verified journalists':
          if 'verified-journalists' in ugroups:
            results['contactSharing'] = True
          else:
            results['contactSharing'] = False
        else:
          if 'ejn-staff' in ugroups:
            results['contactSharing'] = True
          else:
            results['contactSharing'] = False

        return results
