import requests
from sakai import Sakai

LOGIN_URL = ''


def cas_login(sid, password):
    session = requests.Session()
    return session.cookies


class SakaiAuth(Sakai):
    def __init__(self, sid, password):
        cookies = cas_login(sid, password)
        Sakai.__init__(self, cookies)
