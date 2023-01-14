import requests
import time
from requests_ntlm import HttpNtlmAuth
import random
from bs4 import BeautifulSoup




headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

s = requests.session()
s.headers.update(headers)
url = 'http://globaltracktrace.ptc.post/gtt.web/Search.aspx'
r = s.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
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