# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from ejn.applicants4funding.testing import EJN_APPLICANTS4FUNDING_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that ejn.applicants4funding is properly installed."""

    layer = EJN_APPLICANTS4FUNDING_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if ejn.applicants4funding is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'ejn.applicants4funding'))

    def test_browserlayer(self):
        """Test that IEjnApplicants4FundingLayer is registered."""
        from ejn.applicants4funding.interfaces import (
            IEjnApplicants4FundingLayer)
        from plone.browserlayer import utils
        self.assertIn(IEjnApplicants4FundingLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = EJN_APPLICANTS4FUNDING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['ejn.applicants4funding'])

    def test_product_uninstalled(self):
        """Test if ejn.applicants4funding is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'ejn.applicants4funding'))

    def test_browserlayer_removed(self):
        """Test that IEjnApplicants4FundingLayer is removed."""
        from ejn.applicants4funding.interfaces import IEjnApplicants4FundingLayer
        from plone.browserlayer import utils
        self.assertNotIn(IEjnApplicants4FundingLayer, utils.registered_layers())
