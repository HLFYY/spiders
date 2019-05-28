import random
import requests
import subprocess
import time
import re
import hashlib

ADSL_STOP = 'adsl-stop'
ADSL_START = 'adsl-start'
ADSL_IFNAME = 'ppp0'

def MD5(data_str):
    object = hashlib.md5()
    object.update(data_str.encode('utf-8'))
    return object.hexdigest()

def adsl():
    (status_stop, output_stop) = subprocess.getstatusoutput(ADSL_STOP)
    time.sleep(10)
    (status_start, output_start) = subprocess.getstatusoutput(ADSL_START)
    return status_stop, output_stop, status_start, output_start



def get_ip(ifname=ADSL_IFNAME):
    status_stop, output_stop, status_start, output_start = adsl()
    print('status_stop:{} , output_stop:{} , status_start:{} , output_start:{}'.format(status_stop, output_stop, status_start, output_start))
    if status_start or status_stop:
        print('>>>>time:{}, 拨号失败'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
        return

    time.sleep(5)
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
    while True:
        ip = get_ip()
        if not ip:
            time.sleep(60)
            continue
        key = str(random.randint(10**3, 10**5))
        sign_raw = MD5(key)
        data = {
            'ip': ip,
            'key': key,
            'sign': get_sign(sign_raw),
            'name': 'houjie_001',
        }
        print('----time:{}, post_data:{}'.format(time.strftime("%Y-%m-%d %H:%M:%S"), data))
        response = requests.post('http://{}', data=data)
        if response.status_code != 200:
            print('>>>>返回状态码不是200, url:{}, data:{}, status_code:{}'.format(response.url, data, response.status_code))
        time.sleep(600)

if __name__ == '__main__':
    run()