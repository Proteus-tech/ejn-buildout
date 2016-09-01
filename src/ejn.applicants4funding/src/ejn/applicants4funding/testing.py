# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import ejn.applicants4funding


class EjnApplicants4FundingLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=ejn.applicants4funding)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ejn.applicants4funding:default')


EJN_APPLICANTS4FUNDING_FIXTURE = EjnApplicants4FundingLayer()


EJN_APPLICANTS4FUNDING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EJN_APPLICANTS4FUNDING_FIXTURE,),
    name='EjnApplicants4FundingLayer:IntegrationTesting'
)


EJN_APPLICANTS4FUNDING_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EJN_APPLICANTS4FUNDING_FIXTURE,),
    name='EjnApplicants4FundingLayer:FunctionalTesting'
)


EJN_APPLICANTS4FUNDING_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        EJN_APPLICANTS4FUNDING_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='EjnApplicants4FundingLayer:AcceptanceTesting'
)
