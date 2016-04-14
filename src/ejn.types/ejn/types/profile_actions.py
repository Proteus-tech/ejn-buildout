from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite


def modify_access(obj, event):
    """Modify project WF state and permissions
    """
    site = getSite()
    wftool = getToolByName(site, "portal_workflow")

    bioSharing = obj.getBioSharing()
    proSharing = obj.getProSharing()
    contactSharing = obj.getContactSharing()

    wfinfo = wftool.getStatusOf('member_profile_workflow', obj)
    if not wfinfo:
        return
    state = wfinfo['review_state']

    if bioSharing == 'Public':
        if state != 'published':
            wftool.doActionFor(obj, "publish")

    elif bioSharing == 'Unverified EJN members':
        if state != 'visible':
            wftool.doActionFor(obj, "show")

    elif bioSharing == 'Verified journalists':
        if state != 'private':
            wftool.doActionFor(obj, "hide")
            obj.manage_addLocalRoles('verified-journalists', ('Reader',))
            obj.reindexObjectSecurity()
    else:  # this case matches when the sharing permission is set to EJN-staff
        if state != 'private':
            wftool.doActionFor(obj, "hide")
            obj.manage_addLocalRoles('ejn-staff', ('Reader',))
            obj.reindexObjectSecurity()

    if proSharing == 'Verified journalists' or contactSharing == 'Verified journalists':
        obj.manage_addLocalRoles('verified-journalists', ('Reader',))
        obj.reindexObjectSecurity()
