import random
from base_settings import *
from twilio.rest import Client
import yagmail
import hashlib


def send_note(body):
    """发送短信"""
    # data = 'date: {} || platform {} || content {}'.format(time.strftime('%Y-%m-%d %H:%M:%S'), platform.node(), body)
    r = redis.Redis(**REDIS_CONFIG)
    datas = r.get(SEND_NODE_KEY)
    data_dict = json.loads(datas.decode())
    print(data_dict)
    account_sid = data_dict['account_sid']
    auth_token = data_dict['auth_token']
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    # 这里中国的号码前面需要加86
    to='+86' + data_dict['to_phone'],
    from_='+' + data_dict['from_phone'],
    body=body)
    print(message.sid)

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
    print(PROXY_AUTH)
    ip = r.get(SERVER_IP_KEY).decode()
    auth = r.get(PROXY_AUTH).decode()
    response = requests.get('http://{}:8888/proxy'.format(ip))
    data_dict = json.loads(response.text)
    if data_dict['message'] == 'SUCCESS':
        proxy = data_dict['proxy']
    proxy_dict = {
        'http': 'http://{}@{}'.format(auth, proxy),
        'https': 'https://{}@{}'.format(auth, proxy)
    }
    return proxy_dict

if __name__ == '__main__':
    # send_note('hello')
    print(get_proxy())
    # print(MD5("/jp/dash?tvid=11878510309&bid=500&abid=100&src=02027221010000000000&ut=0&ori=h5&ps=0&messageId=1559650754970&pt=0&lid=&cf=&ct=&locale=zh_cn&k_tag=1&dfp=a038afc5a7d37744f493c2030b915b91eb7b2265f33215877881bd2887b108a886&k_ft1=17729624997888&k_uid=1559650754971&qd_v=1&qdy=a&qds=0&tm=1559650754971&callback=onSuccess"))
