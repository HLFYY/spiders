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

def adsl():
    (status_stop, output_stop) = subprocess.getstatusoutput(ADSL_STOP)
    time.sleep(1)
    (status_start, output_start) = subprocess.getstatusoutput(ADSL_START)
    return status_stop, output_stop, status_start, output_start

def get_ip(ifname=ADSL_IFNAME):
    for i in range(3):
        status_stop, output_stop, status_start, output_start = adsl()
        logger.info('----time:{}, status_stop:{} , output_stop:{} , status_start:{} , output_start:{}'.format(time.strftime("%Y-%m-%d %H:%M:%S"), status_stop, output_stop, status_start, output_start))
        if (status_start or status_stop) and i < 2 :
            logger.info('----time:{}, 拨号失败, 重试'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
            if status_start:
                for i in range(2):
                    subprocess.getstatusoutput(ADSL_STOP)
        else:
            break

    (status, output) = subprocess.getstatusoutput('ifconfig')
    if status == 0:
        pattern = re.compile(ifname + '.*?inet.*?(\d+\.\d+\.\d+\.\d+).*?netmask', re.S)
        result = re.search(pattern, output)
        if result:
            ip = result.group(1)
            return ip

def get_sign(sign_raw):
    salt = '46whetf6'
    sign = ''
    for index in range(8):
        sign += sign_raw[index] + salt[index]
    return sign

def run():
    r_cli = redis.Redis(**REDIS_CONFIG)
    print('----time:{}, 开始拨号'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
    ip = get_ip()
    if not ip:
        logger.error('>>>>未获取ip')
        send_note('拨号失败，未获取IP')
        return
    key = str(random.randint(10**3, 10**5))
    sign_raw = MD5(key)
    data = {
        'ip': ip,
        'key': key,
        'sign': get_sign(sign_raw),
        'name': 'houjie_001',
    }
    logger.info('----time:{}, post_data:{}'.format(time.strftime("%Y-%m-%d %H:%M:%S"), data))
    response = requests.post('http://{}:8888'.format(r_cli.get(SERVER_IP_KEY).decode()), data=data)
    if response.status_code != 200:
        logger.error('>>>>返回状态码不是200, data:{}, status_code:{}'.format(data, response.status_code))
        send_note('推送IP失败,返回状态码不是200, data:{}, status_code:{}'.format(data, response.status_code))

if __name__ == '__main__':
    run()