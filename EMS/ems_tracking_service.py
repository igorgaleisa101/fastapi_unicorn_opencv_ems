import hashlib
import base64
import json, random, traceback
import requests
from requests.exceptions import ProxyError
from PIL import Image
from io import BytesIO
from EMS import CaptchaSolver


class EMSTrackingService:
    def __init__(self, proxy=False, session_id=None, lang='cn'):
        self.session = requests.Session()
        self.session.headers['Accept'] = 'application/json, text/plain, */*'
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        self.session.headers['Origin'] = 'https://www.ems.com.cn'
        self.session.headers['Host'] = 'www.ems.com.cn'
        self.session.headers['Referer'] = 'https://www.ems.com.cn/qps/yjcx/'
        self.session_id = session_id or random.randint(11111, 99999)
        self.lang = lang
        if proxy:
            proxy = "https://lum-customer-osoyoo-zone-static-session-{}:sqtmcnel76x9@zproxy.lum-superproxy.io:22225".format(self.session_id)
            self.session.proxies = {
                "http": proxy,
                "https": proxy,
            }

    def generate_ticket(self, waybill_list, timestamp, capcode, secret):
        waybill_string = ''.join(waybill_list)
        timestamp_3 = timestamp[0:3]
        timestamp_10 = timestamp[-10:]
        ticket_string = waybill_string + timestamp_3 + secret + timestamp_10 + capcode
        ticket = hashlib.md5(ticket_string.encode()).hexdigest().upper()
        ticket = hashlib.md5(ticket.encode()).hexdigest().upper()
        message_bytes = ticket.encode()
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode()
        return base64_message

    def get_timestamp(self, ):
        r = self.session.post('https://www.ems.com.cn/ems-web/currentTime/queryTime')
        return str(r.json()['value'])

    def get_captcha_challenge(self):
        try:
            r = self.session.post('https://www.ems.com.cn/ems-web/cutPic/getPic')
        except ProxyError as e:
            if 'ip_forbidden' in str(e):
                raise ProxyError('The server IP is not whitelisted in proxy provider.')
            else:
                raise ProxyError(str(e))

        # Handle proxy error
        if r.status_code == 407:
            raise ProxyError('The server IP is not whitelisted in proxy provider.')

        capcode = r.json()['value']['capcode']
        sliding_image = Image.open(BytesIO(base64.b64decode(r.json()["value"]["slidingImage"])))
        back_image = Image.open(BytesIO(base64.b64decode(r.json()["value"]["backImage"])))
        return sliding_image, back_image, capcode

    def get_captcha_challenge_solution(self, backImage, slidingImage):
        xspot = CaptchaSolver.find_coordinates(backImage, slidingImage)
        return xspot

    def submit_captcha_challenge_solution(self, tracking_number, xspot, capcode):
        # Get the timestamp to generate the ticket
        timestamp = self.get_timestamp()

        # Generate the ticket for the trackTestQuery request
        secret = '1163FA15CC9A425EA4B65B2A218FF5F8'
        ticket = self.generate_ticket(tracking_number, timestamp, capcode, secret)

        payload = {
            "value": {
                "customerIP": "127.0.0.1",
                "phoneNum": None,
                "waybillNoList": [
                    tracking_number
                ],
                "xpos": xspot,
                "capcode": capcode,
                "enFlag": "1"
            }
        }
        self.session.headers['time'] = timestamp
        self.session.headers['ticket'] = ticket
        r = self.session.post('https://www.ems.com.cn/ems-web/trackTestQuery/getLogisticsTestFlag', json=payload)
        return r.json()['success']

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

        try:
            # Solve captcha challenge
            xspot, capcode = self.solve_captcha_challenge(tracking_number)

            # Get the timestamp to generate the ticket
            timestamp = self.get_timestamp()

            # Generate the ticket for the queryTrack result request
            ENGLISH_KEY = '44FC5D74924447C1A9ABC8FD011CF9A0'
            CHINESE_KEY = '053B245CB1B74EBBB5FBB4A5889D66B8'

            if self.lang.upper() == 'EN':
                secret = ENGLISH_KEY
                query_track_url = 'https://www.ems.com.cn/ems-web/cutPicEnglish/queryTrack'
            elif self.lang.upper() == 'CN':
                secret = CHINESE_KEY
                query_track_url = 'https://www.ems.com.cn/ems-web/mailTrack/queryTrack'

            ticket = self.generate_ticket(tracking_number, timestamp, capcode, secret)

            # Make the queryTrack result request
            payload = {
                "value": [
                    {
                        "ip": "0.0.0.0",
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
            r = self.session.post(query_track_url, json=payload)
            if r.json()['success']:
                return r.json()
            else:
                print(r.text)
                return json.dumps({'success': False, 'msg': 'Failed'})
        except ProxyError as e:
            traceback.print_exc()
            return {'success': False, 'msg': 'Proxy Error!', 'error': str(e)}
        except Exception as e:
            traceback.print_exc()
            return {'success': False, 'msg': 'Internal Error!', 'error': str(e)}

    def test_request(self):
        try:
            r = self.session.get('https://api.myip.com/')
            print(r.text)
            print(self.session_id)
            res = r.json()
            res['session_id'] = self.session_id
            return res
        except ProxyError as e:
            return {'success': False, 'msg': 'Proxy Error!', 'error': str(e)}
        except Exception as e:
            traceback.print_exc()
            return {'success': False, 'msg': 'Internal Error!', 'error': f'{type(e).__name__}: {e.args}'}


if __name__ == '__main__':
    ems = EMSTrackingService(proxy=False, lang='cn')
    # ems.test_request()
    # secrets = '1163FA15CC9A425EA4B65B2A218FF5F8', '44FC5D74924447C1A9ABC8FD011CF9A0', '053B245CB1B74EBBB5FBB4A5889D66B8'
    # for secret in secrets:
    #     print(ems.generate_ticket('LV663202155CN', '1674483219680', '2810f2a3196041cf9cf1a8686adb7a8b20230123', secret), secret)
    # print(ems.generate_ticket('LV626850690CN ', '1674465510400', '417a238a7e874f0d96f711b8fb6279c920230123', secret))

    result = ems.get_tracking_result('LY932726434CN')
    print(result)

    result = ems.get_tracking_result('LY932726434CN')
    print(result)

    # result = ems.get_tracking_result('LV663202155CN')
    # print(result)
