from unittest import TestCase

from sakailib.exceptions import SakaiException
from .test_config import config
from .. import sakailib


class TestCas_login(TestCase):
    def test_cas_login(self):
        session_id = sakailib.cas_login(config['usn'], config['pwd'])
        self.assertIsNotNone(session_id)

    def test_cas_login_error(self):
        try:
            sakailib.cas_login('thatcannotbecorrect', 'wewqweweq')
        except Exception as e:
            print(e.__cause__)
            self.assertEqual(type(e), SakaiException)
