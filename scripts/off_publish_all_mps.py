# -*- coding: utf-8 -*-
import argparse
import logging

NAME = 'publish_all_mps'
USAGE = ("./bin/instance -O<plone_site_id> run scripts/{name}.py "
         "[-dr --dryrun]]".format(name=NAME))
logger = logging.getLogger(NAME)
logger.setLevel(logging.DEBUG)
#handler = logging.StreamHandler(sys.stdout)
fh = logging.FileHandler(NAME + '.log')
formatter = logging.Formatter(
	"%(asctime)s %(levelname)s %(name)s %(message)s", "%Y-%m-%d %H:%M:%S")
fh.setFormatter(formatter)
logger.addHandler(fh)

parser = argparse.ArgumentParser()
parser.add_argument("-c", help="this script...")
parser.add_argument(
    "--admin-user",
    type=str,
    help="the admin user of the installation",
    metavar='USERID',
    default='admin')
parser.add_argument(
    "--start-index",
    type=int,
    help="",
    metavar='START_INDEX',
    default=0)
parser.add_argument(
    "-dr", "--dryrun", action="store_true", help="Save changes or not")

params = parser.parse_args()


try:  # pyflakes
    import app
except:
    pass

import transaction
import time
from plone import api
from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName


def timeit(method):

    def timed(*args, **kw):

        print 'START', method.__name__
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print 'STOP', method.__name__

        print 'TIME %r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te - ts)
        return result

    return timed


def select_wf_state(obj, wfinfo, wftool):

    bioSharing = obj.getBioSharing()
    proSharing = obj.getProSharing()
    contactSharing = obj.getContactSharing()

    changed = False    

    if bioSharing == 'Public':
      if wfinfo['review_state'] != 'published':
        wftool.doActionFor(obj, "publish")
        changed = True
        
    elif bioSharing == 'Unverified EJN members':
      if wfinfo['review_state'] != 'visible':
        wftool.doActionFor(obj, "show")
        changed = True
        
    elif bioSharing == 'Verified journalists':
      if wfinfo['review_state'] != 'private':
        wftool.doActionFor(obj, "hide")
        obj.manage_addLocalRoles('verified-journalists', ('Reader',))
        obj.reindexObjectSecurity()
        changed = True
    else: #this case matches when the sharing permission is set to EJN-staff
      if wfinfo['review_state'] != 'private':
        wftool.doActionFor(obj, "hide")
        obj.manage_addLocalRoles('ejn-staff', ('Reader',))
        obj.reindexObjectSecurity()
        changed = True

    if proSharing == 'Verified journalists' or contactSharing == 'Verified journalists':
      obj.manage_addLocalRoles('verified-journalists', ('Reader',))
      obj.reindexObjectSecurity()
      changed = True
    return changed
    

@timeit
def Command(app):
    totals = {
        'already_visible': 0,
        'without_workflow': 0,
        'generic_errors': 0,
        'wrong_portal_type': 0,
        'state_changed': 0,
    }
    with api.env.adopt_user(username=params.admin_user):
        portal = getSite()
        
        if not portal:
            raise ValueError(
                "Site is not set. "
                "Please call this script with -O param. "
                "E.g. {}".format(USAGE))
        mps_dir = portal['directory']
        wftool = getToolByName(portal, "portal_workflow")
        idx = 0 + params.start_index
        tot = len(mps_dir.objectIds())
        for mp in mps_dir.objectValues():
            idx += 1
            if totals['state_changed'] and totals['state_changed'] % 1000 == 0:
                break
            if mp.meta_type != 'MemberProfile':
                continue
            if mp.portal_type == 'MemberProfile':
                logger.error('{idx}/{tot}: Member profile has incorrect portal_type "MemberProfile" instead of "Member Profile": {mp}'.format(mp=mp.id, idx=idx, tot=tot))
                totals['wrong_portal_type'] += 1
                mp.portal_type = 'Member Profile'
                mp.reindexObject()
                continue
            wfchain = wftool.getChainFor(mp)
            if not wfchain:
                logger.error('{idx}/{tot}: Member profile has no associated workflow: {mp}'.format(mp=mp.id, idx=idx, tot=tot))
                totals['without_workflow'] += 1
                continue
            elif 'member_profile_workflow' not in wfchain:
                logger.error('{idx}/{tot}: Member profile has generic error: {mp}'.format(mp=mp.id, idx=idx, tot=tot))
                totals['generic_errors'] += 1
                continue
            wfinfo = wftool.getStatusOf('member_profile_workflow', mp)
            if not wfinfo:
                logger.error('{idx}/{tot}: Member profile has no wf info associated: {mp}'.format(mp=mp.id, idx=idx, tot=tot))
                totals['without_workflow'] += 1
                continue
#            if wfinfo['review_state'] == 'private':
#                logger.info('{idx}/{tot}: Member profile already published: {mp}'.format(mp=mp.id, idx=idx, tot=tot))
#                totals['already_visible'] += 1
#                continue
#            try:
#                wftool.doActionFor(mp, "hide")
#            except:
#                logger.error('{idx}/{tot}: Member profile has generic error: {mp}'.format(mp=mp.id, idx=idx, tot=tot))
#                totals['generic_errors'] += 1
#                continue
#            logger.info('{idx}/{tot}: Member profile was published: {mp}'.format(mp=mp.id, idx=idx, tot=tot))
#            totals['state_changed'] += 1
            if select_wf_state(mp, wfinfo, wftool):
                logger.info('{idx}/{tot}: Member profile state was changed: {mp}'.format(mp=mp.id, idx=idx, tot=tot))
                totals['state_changed'] += 1
            else:
                logger.info('{idx}/{tot}: Member profile state was not changed: {mp}'.format(mp=mp.id, idx=idx, tot=tot))
    for k in totals:
        logger.info('Total {k}: {tot}'.format(k=k, tot=totals[k]))


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
