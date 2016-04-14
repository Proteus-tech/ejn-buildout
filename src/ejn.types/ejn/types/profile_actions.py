from Products.CMFCore.utils import getToolByName
from zope.app.component import hooks 

from zLOG import LOG, INFO

def modify_access(object, event):
    """Modify project WF state and permissions
    """
    site = hooks.getSite()
    workflowTool = getToolByName(site, "portal_workflow")
    
    bioSharing = object.getBioSharing()
    proSharing = object.getProSharing()
    contactSharing = object.getContactSharing()
    
    status = workflowTool.getStatusOf("plone_workflow", object)
    
    if bioSharing == 'Public':
      if workflowTool.getInfoFor(object,'review_state') != 'published':
        workflowTool.doActionFor(object, "published")
        
    elif bioSharing == 'Unverified EJN members':
      if workflowTool.getInfoFor(object,'review_state') != 'visible':
        workflowTool.doActionFor(object, "show")
        
    elif bioSharing == 'Verified journalists':
      if workflowTool.getInfoFor(object,'review_state') != 'private':
        workflowTool.doActionFor(object, "hide")
        object.manage_addLocalRoles('verified-journalists', ('Reader',))
        object.reindexObjectSecurity()
    else: #this case matches when the sharing permission is set to EJN-staff
      if workflowTool.getInfoFor(object,'review_state') != 'private':
        workflowTool.doActionFor(object, "hide")
        object.manage_addLocalRoles('ejn-staff', ('Reader',))
        object.reindexObjectSecurity()

    if proSharing == 'Verified journalists' or contactSharing == 'Verified journalists':
      object.manage_addLocalRoles('verified-journalists', ('Reader',))
      object.reindexObjectSecurity()


