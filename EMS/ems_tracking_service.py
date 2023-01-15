import hashlib
import base64
import json, random, traceback
import requests
from PIL import Image
from io import BytesIO
from EMS import CaptchaSolver


class EMSTrackingService:
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
        r = self.session.post('https://www.ems.com.cn/ems-web/cutPic/getPic')
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
        except requests.exceptions.ProxyError as e:
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
        except requests.exceptions.ProxyError as e:
            return {'success': False, 'msg': 'Internal Error!', 'error': str(e)}
        except Exception as e:
            traceback.print_exc()
            return {'success': False, 'msg': 'Internal Error!', 'error': str(e)}


if __name__ == '__main__':
    ems = EMSTrackingService(proxy=True)
    ems.test_request()
    # result = ems.get_tracking_result('LY932726434CN')
    # print(result)
    #
    # result = ems.get_tracking_result('LV663202155CN')
    # print(result)
