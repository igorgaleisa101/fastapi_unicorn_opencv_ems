import requests
import base64
import os

LAST_CAPTCHA_PATH = 'last_captcha'
AZCAPTCHA_TOKEN = 'qw97ngfnjdwxktz3rmbhgplpfq2m4zjy'


def get_last_captcha_solution():
    # Get last captcha solution if exists
    isExist = os.path.exists(LAST_CAPTCHA_PATH)
    if isExist:
        with open(LAST_CAPTCHA_PATH, 'r') as f:
            answer, encoded_key = f.readline().split('||')
            print('=> Last captcha:', answer, encoded_key)
            return answer, encoded_key
    return '', ''


def save_captcha_solution(answer, encoded_key):
    with open(LAST_CAPTCHA_PATH, 'w') as f:
        f.write('||'.join([answer, encoded_key]))
        print('=> Captcha solution saved!')


def solve_captcha(image_base64):
    # Decoding the base64 string
    image_data = base64.b64decode(image_base64)
    # Saving the image
    with open("last_captcha.jpg", "wb") as f:
        f.write(image_data)
        
    # Sending captcha solve request
    payload = {'method': 'base64', 'key': AZCAPTCHA_TOKEN, 'body': image_base64, 'json': 1}
    r = requests.post('http://azcaptcha.com/in.php', data=payload)
    captcha_id = r.json()['request']
    # print(r.text)

    # Getting captcha answer
    if r.json()['status'] == 1:
        # Loop until getting answer or error
        while True:
            url = f"http://azcaptcha.com/res.php?key={AZCAPTCHA_TOKEN}&action=get&id={captcha_id}&json=1"
            r = requests.get(url)
            # print(response.json())
            if r.json()['status'] == 1:
                answer = r.json()['request']
                print('=> CAPCHA_SOLVED:', answer)
                return answer
            elif r.json()['request'] == 'CAPCHA_NOT_READY':
                print('=> CAPCHA_NOT_READY')
                continue
            else:
                print('=> [ERROR]', r.json()['request'])
                return


if __name__ == '__main__':
    from bs4 import BeautifulSoup

    s = requests.session()
    url = 'http://globaltracktrace.ptc.post/gtt.web/Search.aspx'
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    captcha_image = soup.select_one('#imgCaptcha').get('src').split('base64, ')[1]
    answer = solve_captcha(captcha_image)
    print(answer)
