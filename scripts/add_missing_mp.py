import logging
from plone.api import user
from plone.api import content
import geocoder
import chardet
import transaction

name = 'add_missings_member_profiles'

logger = logging.getLogger(name)
hdlr = logging.FileHandler(name + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)

logger.info('Collecting all users...')
allusers = user.get_users()

site = app['Plone']
mps_dir = site['directory']
logger.info('Collecting all member profiles...')
mps = [mp for mp in mps_dir.objectValues() if mp.meta_type == 'MemberProfile']

profiles = {}

logger.info('Organizing all member profiles by email...')
for mp in mps:
    email = mp.email
    if email not in profiles:
        profiles[email] = []
    profiles[email].append(mp)

present = []
absent = []
logger.info('Create googlemaps connection...')
#API_KEY = 'AIzaSyDN7w_HqoberCZTPJVUoeOmc-MS8gYr78o'
#API_KEY = 'AIzaSyCZom4DjPNomHRqktSPGn5IETSNeJqB52o'
tot = len(allusers)
idx = 1

def safe_decode(name):
    return fullname.decode(chardet.detect(fullname)['encoding'])

def get_country_code(location):
    if not location:
        return None
    loc = geocoder.osm(location)
    if loc and loc.country:
        return loc.country
    partial_location = ''.join(location.split(',')[-1:])
    loc = geocoder.osm(partial_location)
    if loc and loc.country:
        return loc.country
    partial_location = ''.join(location.split()[-1:])
    loc = geocoder.osm(partial_location)
    if loc and loc.country:
        return loc.country

done = 0
for member in allusers:
    email = member.getProperty('email')
    fullname = member.getProperty('fullname')
    logger.info('%s/%s - Processing member: "%s <%s>"' % (idx, tot, fullname, email))
    idx += 1
    if email in profiles:
        present.append(member)
        logger.info('Member profile found.Skip')
#        data = {}
#        location = member.getProperty('location')
#        gm_loc = google_maps.search(location=location)
#        if gm_loc and len(gm_loc.list_data):
#            data['country'] = gm_loc.list_data[0].country_shortcut
#        print data
    else:
        absent.append(member)
        data = {}
        data['email'] = email
        if not fullname:
            logger.error('No fullname found. Skip')
            continue
        fullname = safe_decode(fullname)
        fullname_parts = fullname.split()
        data['nameFirst'] = ' '.join(fullname_parts[:-1])
        data['nameLast'] = ' '.join(fullname_parts[-1:])
        logger.info('FirstName: %s - LastName: %s' % (data['nameFirst'], data['nameLast']))
        location = member.getProperty('location')
        if location:
             cc = get_country_code(location)
             if cc:
                  data['country'] = cc
#                  data['citizenship'] = cc
                  data['countriesOfResidence'] = cc
        try:
            newm = content.create(type='Member Profile', title=fullname, container=mps_dir, **data)
        except Exception as e:
            import pdb;pdb.set_trace()
        logger.info('New member profile created at: %s' % newm.absolute_url())
        done += 1
        if done % 50 == 0:
            transaction.get().commit()
logger.warning('Total found: %s' % len(present))
logger.warning('Total missing: %s' % len(absent))
