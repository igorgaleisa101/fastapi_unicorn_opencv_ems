import os
import pickle
import random

from requests_html import HTMLSession


class Splash:
    COOKIES_PATH = 'usps_cookies.pickle'
    CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, proxy=False,):
        self.session = HTMLSession()
        self.proxy = proxy
        self.load_cookies()

    def update_session_cookies(self):
        print('=> [USPS] Updating cookies using splash...')
        # lua script render html and wait until result element to be exist

        if self.proxy:
            script_path = 'lua_scripts/get_cookies_with_proxy.lua'
        else:
            script_path = 'lua_scripts/get_cookies.lua'

        with open(os.path.join(self.CURRENT_PATH, script_path), 'r') as f:
            script = f.read()

        # Run lua script to get render and get cookies
        r = self.session.post(f'http://splash:8050/run', json={
            'lua_source': script,
            'url': 'https://tools.usps.com/go/TrackConfirmAction?qtc_tLabels1=xyz',
            'username': 'lum-customer-osoyoo-zone-static-session-{}'.format(random.randint(11111, 99999)),
            'password': 'sqtmcnel76x9'
        })

        # Filter cookies
        if 'cookies'in r.json():
            cookies = [c for c in r.json()['cookies'] if 'tools.usps.com' in c['domain']]
        else:
            print(r.json())

        # Set session cookies
        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])

        # Save cookies
        self.save_cookies(self.session.cookies)

    def save_cookies(self, cookies):
        print('=> [USPS] Saving cookies...')
        with open(os.path.join(self.CURRENT_PATH, self.COOKIES_PATH), 'wb') as f:
            pickle.dump(cookies, f)

    def load_cookies(self):
        try:
            with open(os.path.join(self.CURRENT_PATH, self.COOKIES_PATH), 'rb') as f:
                self.session.cookies = pickle.load(f)
        except FileNotFoundError:
            print('=> [USPS] Warning: Cookies file not exist.')
            self.update_session_cookies()

    def test_proxy(self):
        with open(os.path.join(self.CURRENT_PATH, 'lua_scripts/test_proxy.lua'), 'r') as f:
            script = f.read()

        # Run lua script to get render and get cookies
        r = self.session.post(f'http://172.105.5.58:8050/run', json={
            'lua_source': script,
            'url': 'http://api.myip.com',
            'username': 'lum-customer-osoyoo-zone-static-session-{}'.format(random.randint(11111, 99999)),
            'password': 'sqtmcnel76x9'
        })
        print(r.text)


if __name__ == '__main__':
    splash = Splash()
    input(splash.test_proxy())
    splash.update_session_cookies()
    r = splash.session.get('https://tools.usps.com/go/TrackConfirmAction?qtc_tLabels1=LR004324951CN')
    result = r.html.find('.track-statusbar', first=True)
    res = {'success': False}
    if result:
        res['success'] = True
        res['status'] = result.find('.banner-header', first=True).text
        res['desc'] = result.find('.banner-content', first=True).text
        res['value'] = []
        steps = [s for s in result.find('.tb-step') if s.find('p')]
        for step in steps:
            res['value'].insert(0, {s.attrs['class'][0].strip('tb-'): s.text.strip().replace('\xa0', ' ') for s in step.find('p')})
    else:
        print(r.text, r.status_code)

    print(res)



