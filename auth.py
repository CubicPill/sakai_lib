import requests
from bs4 import BeautifulSoup

from exceptions import SakaiException
from sakai import Sakai

LOGIN_URL = 'http://sakai.sustc.edu.cn/portal/pda/?force.login=yes'


def cas_login(sid, password):
    session = requests.Session()
    session.headers = {
        'Host': 'sakai.sustc.edu.cn',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) '
                      'AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'DNT': '1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4'
    }
    resp = session.get(LOGIN_URL)
    soup_login = BeautifulSoup(resp.content, 'html5lib')
    info = {}
    for element in soup_login.find('form', {'id': 'fm1'}).find_all('input'):
        if element.has_attr('name'):
            value = ''
            if element.has_attr('value'):
                value = element['value']
            info[element['name']] = value

    info['username'] = sid
    info['password'] = password

    r = session.post(resp.url, data=info, timeout=30)
    soup_response = BeautifulSoup(r.content, 'html5lib')
    err = soup_response.find('div', {'class': 'errors', 'id': 'msg'})
    if err:
        raise SakaiException('Login failed')

    return session.cookies.get('JSESSIONID', path='/')


class SakaiAuth(Sakai):
    """
    this class takes username and password for authentication
    """

    def __init__(self, sid, password):
        jsessionid = cas_login(sid, password)
        Sakai.__init__(self, jsessionid)
