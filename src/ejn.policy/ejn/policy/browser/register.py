from plone.app.users.browser.register import AddUserForm as BaseAddUserForm
from collective.registrationcaptcha.registrationform import CaptchaRegistrationForm as BaseRegistrationForm
# from plone.app.users.browser.register import RegistrationForm as BaseRegistrationForm

from plone.api import portal
from plone.api import content
from plone.api import user


from ejn.policy.utils import execute_under_special_role


BASE_FIELDS = [
    'fullname', 'email', 'mail_me', 'username'
]


def add_member_profile(data, customfields=None):
    userid = data.get('user_id', data.get('username'))

    member = user.get(userid=userid)
    site = portal.get()
    mps_dir_id = 'directory'
    mps_dir = hasattr(site, mps_dir_id) and site[mps_dir_id] or None
    if not mps_dir:
        return

    mdata = {}
    fullname = member.getProperty('fullname')
    fullname_parts = fullname.split()
    mdata['nameFirst'] = ' '.join(fullname_parts[:-1])
    mdata['nameLast'] = ' '.join(fullname_parts[-1:])
    mdata['email'] = member.getProperty('email')
    mdata['country'] = member.getProperty('country')
    mdata['countriesOfResidence'] = member.getProperty('country')
    mdata['gender'] = member.getProperty('gender')
    for f in customfields:
        if f in BASE_FIELDS or f in ['country', 'gender']:
            continue
        mdata[f] = member.getProperty(f)
    mp = content.create(
        container=mps_dir,
        type='Member Profile',
        id=userid,
        safe_id=True,
        **mdata)
    site = portal.get()
    site.plone_utils.changeOwnershipOf(mp, userid)
    # mp.changeOwnership(member, recursive=True)
    mp.setCreators([userid])
    mp.reindexObjectSecurity()
    mp.reindexObject()
    return mp


class AddUserForm(BaseAddUserForm):

    def handle_join_success(self, data):
        super(AddUserForm, self).handle_join_success(data)
        allfields = [f for f in self.fields]
        customfields = [f for f in allfields if f not in BASE_FIELDS]
        add_member_profile(data, customfields=customfields)


class RegistrationForm(BaseRegistrationForm):

    def handle_join_success(self, data):
        super(RegistrationForm, self).handle_join_success(data)
        site = portal.get()
        allfields = [f for f in self.fields]
        customfields = [f for f in allfields if f not in BASE_FIELDS]
        execute_under_special_role(
            portal=site,
            role='Manager',
            function=add_member_profile,
            data=data,
            customfields=customfields
        )
