import csv
from plone import api
from zope.component.hooks import getSite
from DateTime import DateTime

users = api.user.get_users()
old_users = {}
DEFAULT_LOGIN_TIME = DateTime('2000/01/01 00:00:00 US/Pacific')
ONE_DAY_AGO_LOGIN_TIME = DateTime('2016/05/21 00:00:00 US/Pacific')

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
    if usr.getProperty('email') in old_users:
        continue
    last_login =  usr.getProperty('last_login_time')
    if last_login >= ONE_DAY_AGO_LOGIN_TIME:
        print 'user registered in the last day'
        continue
    if last_login == DEFAULT_LOGIN_TIME:
        new_users['no_login'].append(usr)
        continue
    import pdb;pdb.set_trace()
    new_users['login'].append(usr)


with open('new_users_no_login.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    for usr in new_users['no_login']:
        userid = usr.getProperty('fullname')
        email = usr.getProperty('email')
        description = usr.getProperty('description')
        last_login = usr.getProperty('last_login_time').strftime('%Y-%m-%d %H:%M')
        spamwriter.writerow([userid, email, last_login, description])

with open('new_users_login.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    for usr in new_users['login']:
        userid = usr.getProperty('fullname')
        email = usr.getProperty('email')
        description = usr.getProperty('description')
        last_login = usr.getProperty('last_login_time').strftime('%Y-%m-%d %H:%M')
        spamwriter.writerow([userid, email, last_login, description])
