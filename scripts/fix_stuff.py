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


def Command(app):
    """Questo script migra i contenuti di un vecchio sito eprice
    con collective.transmogrifier.

    Le pipelines sono definite in eprice.migrations
    """
    from AccessControl.SecurityManagement import newSecurityManager

    # Use Zope application server user database (not plone site)
    admin = app.acl_users.getUserById(params.admin_user)
    newSecurityManager(None, admin)
    portal = getSite()
    if not portal:
        raise ValueError(
            "Site is not set. "
            "Please call this script with -O param. "
            "E.g. {}".format(USAGE))
    emails = {}
    for user in api.user.get_users():
        email = user.getProperty('email').lower()
        emails.setdefault(email, []).append(user.getUserId())
        if len(emails[email]) > 1:
            name, domain = email.split('@', 1)
            new_email = '{name}{counter}@{domain}'.format(
                name=name,
                counter=len(emails[email]),
                domain=domain
            )
            logger.warning('Found duplicate for %s (%s): using %s' % (
                user,
                email,
                new_email
            ))
            user.setMemberProperties(mapping={'email': new_email})


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
