import random
from base_settings import *
from twilio.rest import Client
import yagmail
import hashlib


def send_note(body):
    """发送短信"""
    data = 'date: {} || platform {} || content {}'.format(time.strftime('%Y-%m-%d %H:%M:%S'), platform.node(), body)
    r = redis.Redis(**REDIS_CONFIG)
    datas = r.get(SEND_NODE_KEY)
    data_dict = json.loads(datas.decode())
    account_sid = data_dict['account_sid']
    auth_token = data_dict['auth_token']
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    # 这里中国的号码前面需要加86
    to='+86' + data_dict['to_phone'],
    from_='+' + data_dict['from_phone'],
    body=data)
    # print(message.sid)

def send_email(body, title='报警'):
    """发送邮件"""
    data = 'date: {} || platform {} || content {}'.format(time.strftime('%Y-%m-%d %H:%M:%S'), platform.node(), body)
    r = redis.Redis(**REDIS_CONFIG)
    datas = r.get(SEND_EMAIL_KEY)
    data_dict = json.loads(datas.decode())
    yag = yagmail.SMTP(user=data_dict['user'], password=data_dict['password'], host='smtp.yeah.net', port=465)
    yag.send(data_dict['to_email'], title, [data], [])


def loads_data(response, key=''):
    if key:
        return json.loads(response.text)[key]
    else:
        return json.loads(response.text)

def get_headers(type='web'):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': random.choice(APP_USER_AGENT)
    }
    if type == 'web':
        headers['User-Agent'] = random.choice(BROWSER_USER_AGENT)
    return headers

def MD5(data_str):
    object = hashlib.md5()
    object.update(data_str.encode('utf-8'))
    return object.hexdigest()

def get_proxy():
    r = redis.Redis(**REDIS_CONFIG)
    ip = r.get(SERVER_IP_KEY).decode()
    proxy = requests.get('http://{}:8888'.format(ip))
    proxy_dict = {
        'http': 'http://{}'.format(proxy.text),
        'https': 'https://{}'.format(proxy.text)
    }
    return proxy_dict

if __name__ == '__main__':
    # send_note('hello')
    print(get_proxy())