import requests
from requests.cookies import cookiejar_from_dict
from exceptions import SakaiException
from bs4 import BeautifulSoup


class Sakai:
    def __init__(self, jsessionid):
        self.session = requests.session()
        self.session.headers = {
            'Host': 'sakai.sustc.edu.cn',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) '
                          'AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'DNT': '1',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
        }
        self.session.cookies.set(name='JSESSIONID', value=jsessionid)

    def sites_joined(self):
        mp = self.session.get('http://sakai.sustc.edu.cn/portal')
        with open('t.html', 'wb') as f:
            f.write(mp.content)
        soup = BeautifulSoup(mp.content, 'html5lib')
        sites = dict()

        for li in soup.find('ul', {'id': 'pda-portlet-site-menu'}).find_all('li')[1:]:
            sites[li.span.a['href'].split('/')[-1]] = li.span.a.text.strip()

        return sites

    def assignments(self, site_id):
        pass
