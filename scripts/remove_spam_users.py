# -*- coding: utf-8 -*-
import csv
import argparse
import logging
from plone import api
from DateTime import DateTime


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

old_users = {}
users = api.user.get_users()
DEFAULT_LOGIN_TIME = DateTime('2000/01/01 00:00:00 US/Pacific')
ONE_DAY_AGO_LOGIN_TIME = DateTime('2016/05/21 00:00:00 US/Pacific')

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
        'new_users': 0,
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
        with open('users.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                fullname, email, last_login, description = row
                tmp = {
                    'fullname': fullname,
                    'email': email,
                    'last_login': last_login,
                    'description': description
                }
                old_users[email] = tmp
        
        new_users = {
            'no_login': [],
            'login': []
        }
        
        idx = 0
        tot = len(users)
        portal = getSite()
        mps_dir = portal['directory']
        profiles = get_member_profiles(mps_dir)
        for usr in users:
            idx += 1
            print '{idx}/{tot}'.format(idx=idx, tot=tot)
            import pdb;pdb.set_trace()
            if usr.getProperty('email') not in old_users:
                email = usr.getProperty('email')
                last_login =  usr.getProperty('last_login_time')
                mp = profiles['by_email'].get(email)
                if last_login >= ONE_DAY_AGO_LOGIN_TIME or (mp and mp.creation_date >= ONE_DAY_AGO_LOGIN_TIME):
                    print 'user registered in the last day'
                    totals['new_users'] += 1
                    continue
                if last_login == DEFAULT_LOGIN_TIME:
                    print 'NEW user'
                    new_users['no_login'].append(usr)
            else:
                print 'OLD user'
            #new_users['login'].append(usr)
        idx = 0
        #tot = len(new_users['no_login'] + new_users['login'])
        tot = len(new_users['no_login'])
        #for usr in new_users['no_login'] + new_users['login']:
        for usr in new_users['no_login']:
            email = usr.getProperty('email')
            print '{idx}/{tot}: removing user: {email}'.format(
                idx=idx, tot=tot, email=email)
            idx += 1
            mp = profiles['by_email'].get(email)
            if mp:
                mps_dir.manage_delObjects([mp.getId()])
            api.user.delete(user=usr)
            if idx % 100 == 0:
                transaction.commit()
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
