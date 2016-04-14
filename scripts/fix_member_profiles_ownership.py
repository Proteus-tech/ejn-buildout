# -*- coding: utf-8 -*-
import argparse
import logging


USAGE = ("./bin/instance -O<plone_site_id> run scripts/fix_member_profiles_ownership.py "
         "[-dr --dryrun]]")
logger = logging.getLogger('fix_mps_owner')
logger.setLevel(logging.DEBUG)
#handler = logging.StreamHandler(sys.stdout)
fh = logging.FileHandler('fix_member_profiles_ownership.log')
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s", "%Y-%m-%d %H:%M:%S")
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

@timeit
def get_member_profiles(container):
    profiles = {'by_email':{}, 'by_id':{}}
    mps = [mp for mp in container.objectValues() if mp.meta_type == 'MemberProfile']
    
    logger.warning('Organizing all member profiles by email...')
    mps_without_email = []
    for mp in mps:
        email = mp.email
        id_ = mp.id
        if email:
            profiles['by_email'][email] = mp
        else:
            mps_without_email.append(mp)
        profiles['by_id'][id_] = mp
    return profiles
    

@timeit
def Command(app):
    totals = {
        'missing_mp': 0,
        'good_mp_ownership': 0,
        'fixed_mp_ownership': 0,
        'found_by_email': 0,
        'found_by_id': 0,
        'users_without_email': 0,
    }
    with api.env.adopt_user(username=params.admin_user):
        portal = getSite()
        mps_dir = portal['directory']
        profiles = get_member_profiles(mps_dir)
        
        if not portal:
            raise ValueError(
                "Site is not set. "
                "Please call this script with -O param. "
                "E.g. {}".format(USAGE))
        idx = 0
        tot = len(profiles['by_id'])
        for user in api.user.get_users():
            idx += 1
            mp = None
            email = user.getProperty('email')
            if not email or email == '':
                totals['users_without_email'] += 1
            else:
                mp = profiles['by_email'].get(email)
            if mp:
                totals['found_by_email'] += 1
            else:
                mp = profiles['by_id'].get(user.id)
                if mp:
                    totals['found_by_id'] += 1
                else:
                    logger.error("{idx}/{tot}: User doesn't have a member profile yet: {id}".format(id=user.id,idx=idx,tot=tot))
                    totals['missing_mp'] += 1
                    continue
            ownership_infos = mp.owner_info()
            if ownership_infos['id'] == user.id:
                logger.warning("{idx}/{tot}: Member profile already belongs to the corresponding user, skip it: {id}".format(id=user.id, idx=idx,tot=tot))
                totals['good_mp_ownership'] += 1
                continue
            mp.changeOwnership(user, recursive=True)
            mp.reindexObjectSecurity()
            logger.warning("{idx}/{tot}: Fixing member profile ownership: [userid: {id}] [mp: {mp}]".format(id=user.id, idx=idx, mp=mp.absolute_url_path(), tot=tot))
            totals['fixed_mp_ownership'] += 1
    for k in totals:
        logger.warning('Total {k}: {tot}'.format(k=k, tot=totals[k]))


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
