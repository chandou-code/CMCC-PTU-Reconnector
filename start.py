import random
import subprocess

import requests
import time
import codecs
import ddddocr
import sys
import logging
from datetime import datetime

# 配置日志输出到文件
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

import requests


def check_internet_connection():
    websites = ['https://www.baidu.com', 'https://www.bilibili.com',
                'https://www.xn--wxtz62e.site/','https://4399.com/','https://7k7k.com/',
                'https://www.sojson.com/simple_json.html',
                'https://tool.lu/search/?q=%E5%8F%8D%E7%BC%96%E8%AF%91']  # 添加更多的网站到这个列表
    for website in websites:
        try:
            response = requests.get(website, timeout=0.5)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            print(website, '访问失败')
            continue  # 如果访问失败，继续下一个网站
    return False


# 测试函数
print(check_internet_connection())


# ... 其余代码省略 ...
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


def get_current_wifi_name():
    try:
        # 使用subprocess运行netsh命令并捕获输出
        result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)

        # 检查命令是否成功执行并且输出不为空
        if result.returncode == 0 and result.stdout.strip():
            # 解析输出以获取当前连接的Wi-Fi名称
            lines = result.stdout.split('\n')
            for line in lines:
                if "SSID" in line:
                    wifi_name = line.split(":")[1].strip()
                    return wifi_name
            return "Not connected to Wi-Fi."
        else:
            return "Error: Unable to retrieve Wi-Fi information."
    except Exception as e:
        return f"Error occurred: {e}"


def main():
    try:
        # 配置日志输出到控制台和文件
        console = logging.StreamHandler()
        file_handler = logging.FileHandler('log.txt')
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            handlers=[console, file_handler])
        password = ''
        username = ''
        try:
            with open('login.txt', 'r', encoding='utf-8') as f:
                lines = f.readlines()

            if len(lines) >= 2:
                username = lines[0].strip()
                password = lines[1].strip()
                # 在这里对账号和密码进行处理和使用
            else:
                print('文件内容不完整，请重新输入账号和密码')

        except FileNotFoundError:
            username = input('输入校园网账号：')
            password = input('输入校园网密码：')

            try:
                with open('login.txt', 'w', encoding='utf-8') as f:
                    f.write(f'{username}\n{password}')
            except IOError:
                print('写入文件时出现错误')

        print('login')
        i = 0

        while True:

            random_time = random.uniform(1, 4)
            time.sleep(random_time)
            print(f'休眠{random_time}')
            if get_current_wifi_name() == 'CMCC-JKL':
                if check_internet_connection():
                    i += 1

                    print(f'第{i}次正在断网检测')

                else:
                    current_time = datetime.now()
                    logging.info(f'正在重连 {current_time}')
                    res, DAT = get_yzm()
                    handle(res, DAT)
                    login(DAT, username, password)
    except Exception as e:
        current_time = datetime.now()
        # logging.exception(f'发生错误: {str(e)} {current_time}')
        input(f'按任意键退出{str(e)} {current_time}')
        sys.exit(1)


if __name__ == '__main__':
    # wifi_name = get_current_wifi_name()
    # print("Current Wi-Fi Name:", wifi_name)
    main()