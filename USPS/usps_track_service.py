import requests

tracking_number = 'LR011995436CN'

session = requests.session()
session.headers.update({
    #'cookie': 'w3IsGuY1=A4Wux9mFAQAAAC7r_A86QSlsFd3z3w7m6r6vs14R_CTSaYmorn2-XyOoeufIAcU-cuuucnyzwH8AAEB3AAAAAA==;',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
})
r = session.get('https://tools.usps.com/go/TrackConfirmAction')
print(r.headers)

url = f"https://tools.usps.com/go/TrackConfirmAction?qtc_tLabels1={tracking_number}"
response = session.get(url)

if 'CHESAPEAKE' in response.text:
    print('OK')
