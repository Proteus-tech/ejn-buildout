from Products.CMFCore.utils import getToolByName

def getStoriesForProject(context):

    project = context
    reference_catalog = getToolByName(context, 'reference_catalog')

    # relationship: field name used
    # Plone 4.1: objects=True argument to fetch full objects, not just
    # index brains
    references = reference_catalog.getBackReferences(
                        project.UID(),
                        relationship="under program")
    # Resolve Reference objects to full objects
    # Return a generator method which will yield all full objects
    return [ ref.getSourceObject() for ref in references ]


def getPublishedStoriesForProject(context):

    project = context
    reference_catalog = getToolByName(context, 'reference_catalog')
    portal_workflow = getToolByName(context, "portal_workflow")

    # relationship: field name used
    # Plone 4.1: objects=True argument to fetch full objects, not just
    # index brains
    references = reference_catalog.getBackReferences(
                        project.UID(),
                        relationship="under program")
    # Resolve Reference objects to full objects
    # Return a generator method which will yield all full objects
    # 
    results = []
    for ref in references:
      obj = ref.getSourceObject()
      # status = portal_workflow.getStatusOf("featured_publication_workflow", obj)
      status = portal_workflow.getInfoFor(obj, 'review_state')
      if status in ['published','featured']:
        results.append(obj)
    return results

def getChildrenForProject(context):

    project = context
    reference_catalog = getToolByName(context, 'reference_catalog')

    # relationship: field name used
    # Plone 4.1: objects=True argument to fetch full objects, not just
    # index brains
    references = reference_catalog.getBackReferences(
                        project.UID(),
                        relationship="parent program")
    # Resolve Reference objects to full objects
    # Return a generator method which will yield all full objects
    return [ ref.getSourceObject() for ref in references ]
