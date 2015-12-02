from plone.outputfilters.browser import resolveuid
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides


class ResolveUIDView(resolveuid.ResolveUIDView):
    """Resolve a URL like /resolveuid/<uuid> to a normalized URL.
    """

    def __init__(self, context, request):
        super(ResolveUIDView, self).__init__(context, request)
        alsoProvides(request, IDisableCSRFProtection)
