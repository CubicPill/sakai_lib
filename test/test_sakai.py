from unittest import TestCase

from sakailib import SakaiAuth
from .test_config import config

sakai = SakaiAuth(config['usn'], config['pwd'])


class TestSakai(TestCase):
    def test_fetch(self):
        self.fail()

    def test_logout(self):
        self.fail()

    def test_sites_joined(self):
        self.fail()

    def test_get_sites_list(self):
        self.fail()

    def test_site_tools_list(self):
        self.fail()

    def test_site_assignment_list(self):
        self.fail()

    def test_site_resources_list(self):
        self.fail()
