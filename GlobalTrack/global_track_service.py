import hashlib
import base64
import json, random
import requests
from PIL import Image
from io import BytesIO


class GlobalTrackingService:
    def __init__(self, proxy=False, session_id=None):
        self.session = requests.Session()
        self.session.headers['Accept'] = 'application/json, text/plain, */*'
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        self.session_id = session_id or random.randint(11111, 99999)
        if proxy:
            proxy = "https://lum-customer-osoyoo-zone-static-session-{}:sqtmcnel76x9@zproxy.lum-superproxy.io:22225".format(self.session_id)
            self.session.proxies = {
                "http": proxy,
                "https": proxy,
            }

    def solve_captcha_challenge(self, tracking_number):
        print('=> Solving Captcha Challenge...')
        while True:
            # Get the captcha challenge and capcode
            slidingImage, backImage, capcode = self.get_captcha_challenge()

            # getting captcha image solution
            xspot = self.get_captcha_challenge_solution(backImage, slidingImage)

            # Submit captcha challenge solution
            success = self.submit_captcha_challenge_solution(tracking_number, xspot, capcode)
            if success:
                print('=> Captcha Challenge Solved!')
                return xspot, capcode
            else:
                print('=> Wrong solution, trying again...')

    def get_tracking_result(self, tracking_number):
        print('=> Get Tracking Result:', tracking_number)

        # Solve captcha challenge
        xspot, capcode = self.solve_captcha_challenge(tracking_number)

        # Get the timestamp to generate the ticket
        timestamp = self.get_timestamp()

        # Generate the ticket for the queryTrack result request
        secret = '44FC5D74924447C1A9ABC8FD011CF9A0'
        ticket = self.generate_ticket(tracking_number, timestamp, capcode, secret)

        # Make the queryTrack result request
        payload = {
            "value": [
                {
                    "xpos": xspot,
                    "capcode": capcode,
                    "mailStatus": "a",
                    "orderNum": [
                        tracking_number
                    ],
                    "orderType": "1",
                    "noRulesNum": [],
                    "appleFlag": None
                }
            ],
            "list": [
                tracking_number
            ]
        }
        self.session.headers['time'] = timestamp
        self.session.headers['ticket'] = ticket
        r = self.session.post('https://www.ems.com.cn/ems-web/cutPicEnglish/queryTrack', json=payload)
        if r.json()['success']:
            return r.json()
        else:
            return json.dumps({'success': False, 'msg': 'Failed'})

    def test_request(self):
        r = self.session.get('https://api.myip.com/')
        print(r.text)
        print(self.session_id)
        res = r.json()
        res['session_id'] = self.session_id
        return res


if __name__ == '__main__':
    ems = GlobalTrackingService(proxy=True)
    ems.test_request()
    # result = ems.get_tracking_result('LY932726434CN')
    # print(result)
    #
    # result = ems.get_tracking_result('LV663202155CN')
    # print(result)
