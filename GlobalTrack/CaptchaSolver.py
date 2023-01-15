import requests
import base64


def solve_captcha(image_base64):
    # # Decoding the base64 string
    # image_data = base64.b64decode(image_base64)
    # # Saving the image
    # with open("image.jpg", "wb") as f:
    #     f.write(image_data)

    az_key = 'qw97ngfnjdwxktz3rmbhgplpfq2m4zjy'

    # Sending captcha solve request
    print('=> Solving captcha...')
    payload = {'method': 'base64', 'key': az_key, 'body': image_base64, 'json': 1}
    r = requests.post('http://azcaptcha.com/in.php', data=payload)
    captcha_id = r.json()['request']
    # print(r.text)

    # Getting captcha answer
    if r.json()['status'] == 1:
        # Loop until getting answer or error
        while True:
            url = f"http://azcaptcha.com/res.php?key={az_key}&action=get&id={captcha_id}&json=1"
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
