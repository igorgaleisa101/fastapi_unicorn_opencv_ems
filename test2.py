import requests
import time

import random


id = random.randint(11111,55555)
print(id)
proxy = "http://lum-customer-osoyoo-zone-static-session-{}:sqtmcnel76x9@zproxy.lum-superproxy.io:22225".format(id)

PROXY = {
    "http": proxy,
    "https": proxy,
}
proxy_userpwd = "lum-customer-osoyoo-zone-static-session-{}:sqtmcnel76x9".format(id)

s = requests.session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
s.proxies = proxy
s.auth = requests.auth.HTTPBasicAuth(proxy_userpwd.split(':')[0], proxy_userpwd.split(':')[1])
r = s.get("https://api.myip.com/")


print(r.json())



id = 54808
print("sessionid=", id)
proxy = 'http://zproxy.lum-superproxy.io:22225'
proxy_userpwd = "lum-customer-osoyoo-zone-static-session-{id}:sqtmcnel76x9".format(id=id)

url = "https://api.myip.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
}
proxies = {
    "http": proxy,
    "https": proxy
}

response = requests.get(url, headers=headers, proxies=proxies, auth=requests.auth.HTTPBasicAuth(proxy_userpwd.split(':')[0], proxy_userpwd.split(':')[1]))

print(response.text)

