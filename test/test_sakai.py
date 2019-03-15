from unittest import TestCase

from sakailib import SakaiAuth, Sakai, Site
from sakailib.exceptions import NotLoggedIn
from .test_config import config

sakai = SakaiAuth(config['usn'], config['pwd'])
sakai_nologin = Sakai('')


class TestSakai(TestCase):
    def test_fetch(self):
        sakai.fetch('http://sakai.sustech.edu.cn')

    def test_fetch_no_login(self):
        try:
            sakai_nologin.fetch('http://sakai.sustech.edu.cn')
        except Exception as e:
            self.assertEqual(type(e), NotLoggedIn)

    def test_sites_joined(self):
        sakai.sites_joined()

    def test_get_sites_list(self):
        sakai.get_sites_list()

    def test_site_tools_list(self):
        site = sakai.sites_joined()[1]
        self.assertIsNotNone(sakai.site_tools_list(site['id']))

    def test_site_assignment_list(self):
        site: Site = sakai.get_sites_list()[1]
        self.assertIsNotNone(site.assignment_list())

    def test_site_resources_list(self):
        site: Site = sakai.get_sites_list()[1]
        self.assertIsNotNone(site.resources_list())
 