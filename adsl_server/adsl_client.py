import random
import requests
import subprocess
import time
import re
import hashlib
import redis
from adsl_settings import *

logger = logger(file_name='adsl_client')

ADSL_STOP = 'adsl-stop'
ADSL_START = 'adsl-start'
ADSL_IFNAME = 'ppp0'

r_cli = redis.Redis(**REDIS_CONFIG)

def adsl():
    (status_stop, output_stop) = subprocess.getstatusoutput(ADSL_STOP)
    # time.sleep(1)
    (status_start, output_start) = subprocess.getstatusoutput(ADSL_START)
    return status_stop, output_stop, status_start, output_start

def match_ip(ifname):
    (status, output) = subprocess.getstatusoutput('ifconfig')
    if status == 0:
        pattern = re.compile(ifname + '.*?inet.*?(\d+\.\d+\.\d+\.\d+).*?netmask', re.S)
        result = re.search(pattern, output)
        if result:
            ip = result.group(1)
            return ip

def get_ip(data, ifname=ADSL_IFNAME):
    # IP没有变化时，重试2次
    for num in range(3):
        current_ip = r_cli.get(data['name']).decode()

        # 拨号失败，重试2次
        for i in range(3):
            status_stop, output_stop, status_start, output_start = adsl()
            logger.info('----status_stop:{} , output_stop:{} , status_start:{} , output_start:{}'.format(status_stop, output_stop, status_start, output_start))
            if (status_start or status_stop) and i < 2 :
                logger.info('----拨号失败, 重试')
                if status_start:
                    for i in range(2):
                        subprocess.getstatusoutput(ADSL_STOP)
            else:
                break

        # 比对Ip的变化
        ip = match_ip(ifname)
        if current_ip != ip:
            return ip
        else:
            logger.info('----代理ip未变，重新拨号, ip:{}, pre_ip:{}'.format(ip, current_ip))
            # time.sleep(2)


def get_sign(sign_raw):
    salt = '46whetf6'
    sign = ''
    for index in range(8):
        sign += sign_raw[index] + salt[index]
    return sign

def run():
    key = str(random.randint(10**3, 10**5))
    sign_raw = MD5(key)
    data = {
        'key': key,
        'sign': get_sign(sign_raw),
        'name': 'houjie_001',
    }
    logger.info('----开始拨号')
    ip = get_ip(data)
    if not ip:
        logger.error('>>>>未获取ip')
        send_note('拨号失败，未获取IP')
        return

    data['ip'] = ip
    r_cli.set(data['name'], ip)
    logger.info('----post_data:{}'.format(data))
    response = requests.post('http://{}:8888'.format(r_cli.get(SERVER_IP_KEY).decode()), data=data)
    if response.status_code != 200:
        logger.error('>>>>返回状态码不是200, data:{}, status_code:{}'.format(data, response.status_code))
        send_note('推送IP失败,返回状态码不是200, data:{}, status_code:{}'.format(data, response.status_code))

if __name__ == '__main__':
    run()