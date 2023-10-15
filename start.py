import requests
import time
import codecs
import ddddocr
import sys


def check_internet_connection():
    try:
        response = requests.get('http://www.纯度.site/online', timeout=1)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False


def get_yzm():
    DAT = int(time.time() * 1000)
    yzm_url = f'http://192.168.116.8:801/eportal/?c=main&a=getCode&v=3.0_{DAT}'
    r = requests.get(yzm_url)

    with open('yzm.jpg', 'wb') as f:
        f.write(r.content)
    ocr = ddddocr.DdddOcr(beta=True)

    with open("yzm.jpg", 'rb') as f:
        image = f.read()

    res = ocr.classification(image)
    print('验证码识别', res)
    return res, DAT


def login(DAT, username, password):
    url = f'http://192.168.116.8/drcom/login?callback=dr{DAT}&DDDDD={username}&upass={password}&0MKKey=123456&R1=0&R3=0&R6=0&para=00&v6ip=&_={DAT}'
    r = requests.get(url)
    print('登录', r.status_code)


def handle(res, DAT):
    url = f'http://192.168.116.8:801/eportal/?c=Portal&a=check_captcha&callback=dr{DAT}&captcha={res}&_={DAT}'
    r = requests.get(url)
    print('提交验证码', r.status_code)


if __name__ == '__main__':
    try:
        while True:
            time.sleep(3)
            if check_internet_connection():
                print('已联网')
                pass
            else:
                print('正在重连')
                res, DAT = get_yzm()
                handle(res, DAT)

                username = input('输入校园网账号')
                password = input('输入校园网密码')
                login(DAT, username, password)
    except Exception as e:
        print('发生错误:', str(e))
        input('按任意键退出')
        sys.exit(1)
