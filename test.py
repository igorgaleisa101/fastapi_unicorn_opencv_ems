import requests
import time
from requests_ntlm import HttpNtlmAuth
import random, base64
from bs4 import BeautifulSoup




headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

s = requests.session()
s.headers.update(headers)
url = 'http://globaltracktrace.ptc.post/gtt.web/Search.aspx'
r = s.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
captcha_image = soup.select_one('#imgCaptcha').get('src').split('base64, ')[1]
# Decoding the base64 string
image_data = base64.b64decode(captcha_image)
# Saving the image
with open("image.jpg", "wb") as f:
    f.write(image_data)


az_key = 'qw97ngfnjdwxktz3rmbhgplpfq2m4zjy'
url = "http://azcaptcha.com/in.php"
payload = { 'method': 'base64', 'key': az_key, 'body': captcha_image, 'json': 1}
response = requests.post(url, data=payload)
captcha_id = response.json()['request']
print(response.text)
if response.json()['status'] == 1:
    while True:
        url = f"http://azcaptcha.com/res.php?key={az_key}&action=get&id={captcha_id}&json=1"
        response = requests.get(url)
        # print(response.json())
        if response.json()['status'] == 1:
            answer = response.json()['request']
            print('=> CAPCHA_SOLVED:', answer)
            break
        elif response.json()['request'] == 'CAPCHA_NOT_READY':
            print('=> CAPCHA_NOT_READY')
            continue
        else:
            print('=> [ERROR]', response.json()['request'])



input()
payload = {i.get('name'): i.get('value') for i in soup.select('form input')}
input(payload)

payload['txtCaptchaCode'] = '9V7K'
data = {
    'scriptManager': 'updatePanelMain|btnSearch',
    '__LASTFOCUS': '',
    'txtCaptchaCode': '9V7K',
    'txtCaptchaEncCode': 'ujaV5dO+0HIaL0KtQpRTzcze+psgnwbk5ZH+DW9FXeY=',
    'txtItemID': 'LV668750216CN',
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    '__VIEWSTATE': '/wEPDwUKLTUyNDE5ODE2MGRkpC45apxW95pzjOiMYkvlxbA9bV1wPdO0gPIrtVYZf2g=',
    '__VIEWSTATEGENERATOR': '0E00865D',
    '__EVENTVALIDATION': '/wEdAAVtF9D/zTbJMlB0lJrDgFuW3m1re+op15Ka7iC+pL+mZ0lO0NOkHtpldLktEn/yFqTzuppBasCM/T8F53teBd63jtTdVzRZn7DFyWrI8V/OY4r1pAA3zlZNo21eCtG8y5KkNHbAfgHAOxX6+tHaSSh1',
    '__ASYNCPOST': 'true',
    'btnSearch': 'Search',
}

response = requests.post('http://globaltracktrace.ptc.post/gtt.web/Search.aspx', headers=headers, data=data)