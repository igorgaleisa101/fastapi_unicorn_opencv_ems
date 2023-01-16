import hashlib
import base64
import json, random, traceback
import requests
from requests.exceptions import ProxyError
from bs4 import BeautifulSoup
from GlobalTrack.CaptchaSolver import solve_captcha, save_captcha_solution, get_last_captcha_solution


class GlobalTrackingService:
    def __init__(self, proxy=False, session_id=None):
        self.session = requests.Session()
        self.session.headers[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        self.session_id = session_id or random.randint(11111, 99999)
        if proxy:
            proxy = "https://lum-customer-osoyoo-zone-static-session-{}:sqtmcnel76x9@zproxy.lum-superproxy.io:22225".format(
                self.session_id)
            self.session.proxies = {
                "http": proxy,
                "https": proxy,
            }

    def solve_captcha_challenge(self, captcha_image, payload, azcaptcha=False):
        print('=> Solving Captcha Challenge...')
        if azcaptcha:
            # Solve captcha challenge
            payload['txtCaptchaCode'] = solve_captcha(captcha_image)
        else:
            # Get last captcha solution
            captcha_answer, encoded_key = get_last_captcha_solution()
            payload['txtCaptchaCode'] = captcha_answer
            payload['txtCaptchaEncCode'] = encoded_key
        return payload

    def get_captcha_challenge(self, tracking_number):
        # Get initial request payload
        r = self.session.get('http://globaltracktrace.ptc.post/gtt.web/Search.aspx')

        # Get captcha image
        soup = BeautifulSoup(r.text, 'html.parser')
        captcha_image = soup.select_one('#imgCaptcha').get('src').split('base64, ')[1]

        payload = {i.get('name'): i.get('value') for i in soup.select('form input')}
        payload['txtItemID'] = tracking_number

        return captcha_image, payload

    def get_track_details(self, payload):
        r = self.session.post('http://globaltracktrace.ptc.post/gtt.web/Search.aspx', data=payload)

        # Handle proxy error
        if r.status_code == 407:
            raise ProxyError('Your IP is not whitelisted.')

        # Get track details
        soup = BeautifulSoup(r.text, 'html.parser')
        track_details = soup.select_one('#resultsPanel')
        return track_details

    def handle_track_details(self, track_details):
        # Remove 'New Search' button
        track_details.select_one('#btnNewSearch').decompose()
        return str(track_details)

    def get_tracking_result(self, tracking_number):
        print('=> Get Tracking Result:', tracking_number)
        try:
            # Get captcha challenge
            captcha_image, original_payload = self.get_captcha_challenge(tracking_number)

            # Solve captcha challenge using last captcha solution
            solved_payload = self.solve_captcha_challenge(captcha_image, original_payload, azcaptcha=False)

            # Get track details
            track_details = self.get_track_details(solved_payload)

            # Verify track details
            if track_details:
                print('=> Success results.')
                return {'success': True, 'html': self.handle_track_details(track_details)}
            else:  # The last captcha solution failed!
                attempts = 0
                while True:
                    print('=> Failed, trying again with AZCaptcha...')

                    if attempts > 0:
                        # Get new captcha challenge
                        captcha_image, original_payload = self.get_captcha_challenge(tracking_number)
                    if attempts >= 2:
                        print('=> Error: AZCaptcha failed many times.')
                        return {'success': False, 'msg': 'Internal Error!',
                                'error': 'AZCaptcha failed many times. Try again.'}

                    # Solve captcha challenge using solver service
                    solved_payload = self.solve_captcha_challenge(captcha_image, original_payload, azcaptcha=True)
                    print(original_payload)
                    print(solved_payload)
                    attempts += 1

                    # Get track details
                    track_details = self.get_track_details(solved_payload)

                    # Verify track details
                    if track_details:
                        print('=> Success results.')
                        # Save captcha solution
                        save_captcha_solution(solved_payload['txtCaptchaCode'], solved_payload['txtCaptchaEncCode'])
                        return {'success': True, 'html': self.handle_track_details(track_details)}

        except ProxyError as e:
            return {'success': False, 'msg': 'Proxy Error!', 'error': str(e)}
        except Exception as e:
            traceback.print_exc()
            return {'success': False, 'msg': 'Internal Error!', 'error': f'{type(e).__name__}: {e.args}'}


if __name__ == '__main__':
    service = GlobalTrackingService(proxy=False)
    result = service.get_tracking_result('EB780555102CN')
    print(result)

    tracking_numbers = [
        'LV611586092CN', 'LV617908564CN', 'LV611585684CN', 'RG008482666CN', 'CY012011836CN', 'LV627660811CN',
        'CY012373804CN', 'LA151249639CN', 'LP582688401CN', 'EV029066604CN', 'LV651582139CN', 'LV663202155CN',
        'LV651582350CN', 'LV660539880CN', 'LV668750216CN', 'LV668550223CN', 'LV669594781CN', 'LV668077772CN',
        'LV668077622CN', 'EB780555102CN', 'LR021365770CN', 'LV673862524CN'
    ]

    for tracking_number in tracking_numbers:
        result = service.get_tracking_result(tracking_number)
        print(result)
        print('=' * 50)
