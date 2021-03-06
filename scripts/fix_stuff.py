import argparse
import logging


USAGE = ("./bin/instance -O<plone_site_id> run scripts/fix_stuff.py "
         "[-dr --dryrun]]")

logger = logging.getLogger('fix_stuff')

parser = argparse.ArgumentParser()
parser.add_argument("-c", help="this script...")
parser.add_argument(
    "--admin-user",
    type=str,
    help="the admin user of the installation",
    metavar='USERID',
    default='admin')
parser.add_argument(
    "-dr", "--dryrun", action="store_true", help="Save changes or not")

params = parser.parse_args()


try:  # pyflakes
    import app
except:
    pass

import transaction
from plone import api
from zope.component.hooks import getSite
from zope.component import getUtility
from zope.lifecycleevent import ObjectCreatedEvent
from zope.intid.interfaces import IIntIds
from five.intid.site import add_intids
from five.intid.intid import addIntIdSubscriber


DELETE_CONTENT = (
    ('/Plone/opportunities/applications/2013/2014-ejn-grants-applications/'
     'ejn-grants-blank-budget-form'),
)


def Command(app):
    """Questo script migra i contenuti di un vecchio sito eprice
    con collective.transmogrifier.

    Le pipelines sono definite in eprice.migrations
    """
    with api.env.adopt_user(username=params.admin_user):
        portal = getSite()
        if not portal:
            raise ValueError(
                "Site is not set. "
                "Please call this script with -O param. "
                "E.g. {}".format(USAGE))
        userids = {}
        emails = {}
        deleted = []
        for user in api.user.get_users():
            email = user.getProperty('email').lower()
            raw_userid = user.getUserId()
            userid = user.getUserId().lower()
            needs_deletion_reason = []
            if emails.get(email, 0) == 0:
                emails[email] = 1
            else:
                emails[email] = emails[email] + 1
                needs_deletion_reason.append('duplicate email')
            if userids.get(userid, 0) == 0:
                userids[userid] = 1
            else:
                userids[userid] = userids[userid] + 1
                needs_deletion_reason.append('duplicate userid')
            if len(needs_deletion_reason) > 0:
                api.user.delete(user=user)
                deleted.append([raw_userid, needs_deletion_reason])
        if len(deleted) > 1:
            logger.warning("We have deleted some users:\n%s" % (
                '\n'.join('%s: %s' % (d[0], ', '.join(d[1])) for d in deleted)
            ))
        # Adding intid to every content
        logger.info("Now adding intids")
        add_intids(portal)
        catalog = portal.portal_catalog
        intids = getUtility(IIntIds)
        results = catalog.searchResults(
            object_provides=(
                'Products.CMFCore.interfaces._content.IContentish',
            )
        )
        for brain in results:
            obj = brain.getObject()
            addIntIdSubscriber(obj, ObjectCreatedEvent(obj))
            intids.getId(obj)
        # Delete problematic content
        for path in DELETE_CONTENT:
            obj = portal.restrictedTraverse(path)
            api.content.delete(obj=obj, check_linkintegrity=False)


if "app" in locals():
    try:
        Command(app)
    except:
        transaction.abort()
        raise
    else:
        if not params.dryrun:
            transaction.commit()
            logger.warning('Changes Saved')
        else:
            transaction.abort()
            logger.warning('Dry Run mode - nothing changed')
