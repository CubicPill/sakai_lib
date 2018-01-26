from unittest import TestCase

from sakailib import SakaiAuth, Sakai
from sakailib.exceptions import NotLoggedIn
from .test_config import config

sakai = SakaiAuth(config['usn'], config['pwd'])
sakai_nologin = Sakai('')


class TestSakai(TestCase):
    def test_fetch(self):
        sakai.fetch('https://sakai.sustc.edu.cn')

    def test_fetch_no_login(self):
        try:
            sakai_nologin.fetch('https://sakai.sustc.edu.cn')
        except Exception as e:
            self.assertEqual(type(e), NotLoggedIn)

    def test_logout(self):
        self.fail()

    def test_sites_joined(self):
        sakai.sites_joined()

    def test_get_sites_list(self):
        sakai.get_sites_list()

    def test_site_tools_list(self):
        self.fail()

    def test_site_assignment_list(self):
        self.fail()

    def test_site_resources_list(self):
        self.fail()
