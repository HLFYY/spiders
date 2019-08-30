import random
import base64
from base_settings import *
from twilio.rest import Client
import yagmail
import hashlib

def sub_str(a, b):
    c = a[:int(b[0])]
    d = a[int(b[0]): int(b[0]) + int(b[1])]
    return c + a[int(b[0]):].replace(d, '')


def str2list(str_data):
    return str_data.replace('', '=')[1:-1].split('=')


def decrypt_download_url(a):
    """
    美拍详情页的视频下载链接解密
    :param a:
    :return:
    """
    b_str, b_hex = a[4:], a[:4][::-1]
    b = str(int(b_hex, 16))
    c_pre, c_tail = str2list(b[:2]), str2list(b[2:])
    d = sub_str(b_str, c_pre)
    c_tail[0] = len(d) - int(c_tail[0]) - int(c_tail[1])
    data = sub_str(d, c_tail)
    # return base64.b64decode(data, '-_').decode()
    print(len(data))
    return base64.urlsafe_b64decode(data).decode()


def response_retry(response, url='', data_log={}, retry_times_max=1):
    """
    scrapy重试, 调用方式: yield response_retry(response)
    :param response: response对象
    :param url: 指定的重试链接
    :param data_log: 需要记录log的信息
    :param retry_times_max: 最大重试次数
    :return: request对象
    """
    # raw_url 为自定义设置的初始请求URL，在用IP代理时部分代理会修改URL
    request = response.request.replace(url=url if url else response.meta.get('raw_url', response.url))
    # retry_times 为自定义重试次数
    retry_times = request.meta.get('retry_times', 0)
    if retry_times < retry_times_max:
        request.dont_filter = True  # 这个一定要有，否则重试的URL会被过滤
        request.meta['retry_times'] = retry_times + 1
        return request
    else:
        logging.error('>>>>多次重试失败,data:{}, retry_times:{}'.format(data_log, retry_times))

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

def get_proxy():
    r = redis.Redis(**REDIS_CONFIG)
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


def MD5(data_str):
    object = hashlib.md5()
    object.update(data_str.encode('utf-8'))
    return object.hexdigest()


def kasi_data_sign(time_raw, key_word=''):
    """
    卡思数据，搜索接口的headers参数sign构成
    :param time_raw: time.time(), headers里的salt=int(time_raw*1000)
    :param key_word: 关键词
    :return:
    """
    today = int(time.strftime("%d", time.localtime(time_raw)))
    time_str = str(int(time_raw * 1000))
    dicts = {
        '0': 3,
        '1': 2,
        '2': 8,
        '3': 9,
        '4': 0,
        '5': 5,
        '6': 7,
        '7': 1,
        '8': 4,
        '9': 6
    }
    one = ''
    for i in time_str:
        one += str(dicts[i])
    two = int(one) * int(time_str[-3:]) + today
    three = ''
    for i in str(two):
        three += chr(int(i) + 65)
    if key_word:
        return MD5('[{"keyword":"%s"}]&%s&%s' % (key_word, three, time_str))
    else:
        return MD5('&%s&%s' % (three, time_str))

if __name__ == '__main__':
    # send_note('hello')
    # print(get_proxy())
    # print(MD5("/jp/dash?tvid=11878510309&bid=500&abid=100&src=02027221010000000000&ut=0&ori=h5&ps=0&messageId=1559650754970&pt=0&lid=&cf=&ct=&locale=zh_cn&k_tag=1&dfp=a038afc5a7d37744f493c2030b915b91eb7b2265f33215877881bd2887b108a886&k_ft1=17729624997888&k_uid=1559650754971&qd_v=1&qdy=a&qds=0&tm=1559650754971&callback=onSuccess"))
    # print(decrypt_download_url('2e32aHR0cDovLN212dmlkZW8xMC5tZWl0dWRhdGEuY29tLzVhZWMzZjcxMjQ0MWM0Nzg1X0gyNjRfevYBVZMTEubXA0'))
    dd = MD5('"/jp/dash?tvid=933089300&bid=500&abid=100&src=02027221010000000000&ut=0&ori=h5&ps=0&messageId=1566792304077&pt=0&lid=&cf=&ct=&locale=zh_cn&k_tag=1&dfp=a0442051fe4feb46dea0d8ff2400add4d6ba818ea3f574902fa2d8a3a3d0c28fef&k_ft1=17729624997888&k_uid=1566792304083&qd_v=2&tm=1566792304082&qdy=a&qds=0&callback=onSuccess"')
    print(dd)