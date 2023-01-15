import hashlib
import base64
import json, random, traceback
import requests
from bs4 import BeautifulSoup
from GlobalTrack.CaptchaSolver import solve_captcha, save_captcha_solution, get_last_captcha_solution


def solve_captcha_challenge(captcha_image):
    print('=> Solving Captcha Challenge...')
    answer = solve_captcha(captcha_image)
    return answer


class GlobalTrackingService:
    def __init__(self, proxy=False, session_id=None):
        self.session = requests.Session()
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        self.session_id = session_id or random.randint(11111, 99999)
        if proxy:
            proxy = "https://lum-customer-osoyoo-zone-static-session-{}:sqtmcnel76x9@zproxy.lum-superproxy.io:22225".format(self.session_id)
            self.session.proxies = {
                "http": proxy,
                "https": proxy,
            }

    def solve_captcha_challenge(self, captcha_image, payload, force=False):
        if force:
            # Solve captcha challenge
            payload['txtCaptchaCode'] = solve_captcha_challenge(captcha_image)
        else:
            # Get last captcha solution
            captcha_answer, encoded_key = get_last_captcha_solution()
            payload['txtCaptchaCode'] = captcha_answer
            payload['txtCaptchaEncCode'] = encoded_key
        return payload

    def get_tracking_result(self, tracking_number):
        print('=> Get Tracking Result:', tracking_number)
        try:
            # Get initial request payload
            r = self.session.get('http://globaltracktrace.ptc.post/gtt.web/Search.aspx')
            soup = BeautifulSoup(r.text, 'html.parser')
            payload = {i.get('name'): i.get('value') for i in soup.select('form input')}
            payload['txtItemID'] = tracking_number
            encoded_key = payload['txtCaptchaEncCode']

            # Get captcha image
            captcha_image = soup.select_one('#imgCaptcha').get('src').split('base64, ')[1]

            # Solve captcha challenge using last solution
            payload = self.solve_captcha_challenge(captcha_image, payload)

            while True:
                # Getting request result
                r = self.session.post('http://globaltracktrace.ptc.post/gtt.web/Search.aspx', data=payload)
                soup = BeautifulSoup(r.text, 'html.parser')
                results = soup.select_one('#resultsPanel')

                if results:
                    print('=> Success results.')
                    # Save captcha solution
                    save_captcha_solution(payload['txtCaptchaCode'], payload['txtCaptchaEncCode'])

                    # Remove 'New Search' button
                    results.select_one('#btnNewSearch').decompose()
                    return {'success': True, 'html': str(results)}
                else:
                    print('=> Failed, trying again...')

                    # Solve captcha challenge using solver service
                    payload['txtCaptchaEncCode'] = encoded_key
                    payload = self.solve_captcha_challenge(captcha_image, payload, force=True)
        except requests.exceptions.ProxyError as e:
            return {'success': False, 'msg': 'Proxy Error!', 'error': str(e)}
        except Exception as e:
            traceback.print_exc()
            if r.status_code == 407:
                e = 'Proxy Auth Failed (code: ip_forbidden)'
            errors_note = {
                "Proxy Auth Failed (code: ip_forbidden)": 'Your proxy zone is configured with Whitelist IPs permission, and the machine IP (bot) is not part of that list.'
            }
            return {'success': False, 'msg': 'Internal Error!', 'error': e, 'notes': errors_note}



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
        print('='*50)


