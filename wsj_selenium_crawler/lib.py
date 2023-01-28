import datetime
import re
import sys
import time
from colorama import init, Fore, Back, Style

driver_path = r"D:\Python Projects\Webdriver\msedgedriver.exe"
ex_path = r"D:/bypass/bypass-paywalls-chrome-master.crx"  # 拓展的路径
ex_path_chrome = r'"D:\bypass\bypass-paywalls-chrome-master"'

# proxy = '202.109.157.67:9000'

# proxies = '127.0.0.1:1080'
#
# socks5_proxies = 'socks5://'+proxies
# url = 'http://www.wsj.com'


def mkdir(path):
    import os

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    is_exists = os.path.exists(path)

    # 判断结果
    if not is_exists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)

        print(path + ' 创建成功')

        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录存在 ✔')
        return False


def sep_print(list):
    for i in list:
        print(i)


def cover_name():
    # 对封面源码文件进行明明
    date = datetime.datetime.now()
    Y, M, D = str(date.year), '_' + str(date.month), '_' + str(date.day)
    daily_coversourse_filename = './source/cover/' + Y + M + D + '_cover.html'
    return daily_coversourse_filename


def js_activator(driver, k=40, thread_n=None):
    # since multiprocess takes a long time, simple wait can easily be time-out
    # to make the demo robust, I accept the condition that the paywall is not passed
    content_0 = driver.page_source
    for i in range(k):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight/40)')
        time.sleep(0.5 * i)
        if driver.page_source != content_0:
            break
    try:
        assert content_0 != driver.page_source
    except Exception:
        if not thread_n:
            print('js failed to activate')

        else:
            print('js failed to activate for process{}'.format(thread_n))



    if not thread_n:
        print('js activated, scrolled {} time(s)'.format(i + 1))
    else:
        print('js activated, scrolled {} time(s) for process{}'.format(i + 1, thread_n))
    time.sleep(0.5)


def pure_scroll(driver):
    for _ in range(2):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight/20)')
        time.sleep(0.5)


def net_check():
    import requests
    init(autoreset=True)
    try:
        requests.get('https://www.baidu.com')
        print(Fore.LIGHTGREEN_EX + 'network connected')
    except Exception:
        print(Fore.LIGHTRED_EX + 'network if off')
        sys.exit()

    try:
        requests.get('https://www.google.com')
        print(Fore.LIGHTGREEN_EX + 'proxy working')
    except Exception:
        print(Fore.LIGHTRED_EX + 'proxy if off')
        sys.exit()


def essay_type(url):
    # print(url)
    essay_type = re.findall(r'https://www.wsj.com/(.*?)/', url)[0]
    return essay_type
