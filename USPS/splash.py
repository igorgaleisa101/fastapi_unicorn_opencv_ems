import os
import pickle

from requests_html import HTMLSession


class Splash:
    COOKIES_PATH = 'usps_cookies.pickle'

    def __init__(self):
        self.session = HTMLSession()
        self.load_cookies()
        self.current_path = os.path.dirname(os.path.abspath(__file__))

    def update_session_cookies(self):
        print('=> [USPS] Updating cookies using splash...')
        # lua script render html and wait until result element to be exist

        with open(os.path.join(self.current_path, 'lua_scripts/get_cookies.lua'), 'r') as f:
            script = f.read()

        # Run lua script to get render and get cookies
        r = self.session.post(f'http://localhost:8050/run', json={
            'lua_source': script,
            'url': 'https://tools.usps.com/go/TrackConfirmAction?qtc_tLabels1=xyz'
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
        with open(os.path.join(self.current_path, self.COOKIES_PATH), 'wb') as f:
            pickle.dump(cookies, f)

    def load_cookies(self):
        try:
            with open(os.path.join(self.current_path, self.COOKIES_PATH), 'rb') as f:
                self.session.cookies = pickle.load(f)
        except FileNotFoundError:
            print('=> [USPS] Warning: Cookies file not exist.')
            self.update_session_cookies()


if __name__ == '__main__':
    splash = Splash()
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



