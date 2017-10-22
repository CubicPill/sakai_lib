import requests
from bs4 import BeautifulSoup

from exceptions import *


class Sakai:
    """
    main class for the lib
    """

    def __init__(self, jsessionid):
        """
        :param jsessionid: JSESSIONID field in cookies
        """
        self.session = requests.session()
        self.__jsessionid = jsessionid
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

    def fetch(self, url):
        resp = self.session.get(url)
        if '"loggedIn": false' in resp.text:
            # TODO: fix this dirty solution
            raise NotLoggedIn
        return resp

    def sites_joined(self):
        """
        get all joined sites
        :return: list of dict {id, name}
        """
        mp = self.fetch('http://sakai.sustc.edu.cn/portal')
        with open('t.html', 'wb') as f:
            f.write(mp.content)
        soup = BeautifulSoup(mp.content, 'html5lib')
        sites = list()

        for li in soup.find('ul', {'id': 'pda-portlet-site-menu'}).find_all('li')[1:]:
            sites.append({
                'id': li.span.a['href'].split('/')[-1],
                'name': li.span.a.text.strip()
            })

        return sites

    def get_sites_list(self, prefetch=True):
        """
        get all joined sites, objects
        :param prefetch: if True, the tools list in site will be fetched on create
        :return: list of Site objects
        """
        sites = list()
        for site in self.sites_joined():
            sites.append(Site(self.__jsessionid, site['id'], site['name'], prefetch))
        return sites

    def site_tools_list(self, site_id):
        """
        get tool list of given site
        :param site_id:
        :return: list od dict {id, name}
        """
        resp = self.fetch('http://sakai.sustc.edu.cn/portal/pda/' + site_id)
        soup = BeautifulSoup(resp.content, 'html5lib')
        tools = list()
        for li in soup.find('ul', {'id': 'pda-portlet-page-menu'}).find_all('li'):
            tools.append({
                'id': li.span.a['href'].split('/')[-1],
                'name': li.span.a['title']
            })
        return tools

    def site_assignment_list(self, site_id, tool_id):
        """
        get assignment list of given site
        :param site_id: site id
        :param tool_id: site's assignment tool's id
        :return: list of dict {title, status, start_date, due_date}
        """
        resp = self.fetch('http://sakai.sustc.edu.cn/portal/pda/{}/tool/{}'.format(site_id, tool_id))
        soup = BeautifulSoup(resp.content, 'html5lib')
        assignments = list()
        for tr in soup.find('table').find_all('tr')[1:]:
            assignments.append({
                'title': tr.find('td', {'headers': 'title'}).text.strip(),
                'status': tr.find('td', {'headers': 'status'}).text.strip(),
                'start_date': tr.find('td', {'headers': 'openDate'}).text.strip(),
                'due_date': tr.find('td', {'headers': 'dueDate'}).text.strip()
            })
        return assignments


class Site(Sakai):
    """
    represents a joined site
    """

    def __init__(self, jsessionid, site_id, name, prefetch=True):
        """
        :param jsessionid:
        :param site_id:
        :param name:
        :param prefetch: if fetch tools list on create
        """
        Sakai.__init__(self, jsessionid)
        self._site_id = site_id
        self._name = name
        self.tools_list = None
        if prefetch:
            self.tools_list = super().site_tools_list(self._site_id)

    def assignment_list(self):
        """
        get assignment list of this site
        :return: list of dict {title, status, start_date, due_date}
        """
        if not self.tools_list:
            self.tools_list = super().site_tools_list(self._site_id)
        assignment_tool_id = None
        for tool in self.tools_list:
            if tool['name'] == 'Assignments':
                assignment_tool_id = tool['id']
                break
        if not assignment_tool_id:
            raise NoSuchItem('Assignments')
        return super().site_assignment_list(self._site_id, assignment_tool_id)

    def __repr__(self):
        return '<SakaiSite {}>'.format(self._site_id)
