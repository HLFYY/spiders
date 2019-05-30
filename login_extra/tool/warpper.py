from settings.conf import *
from pymongo import MongoClient
import platform
import time
from base_method import *

def get_cookie(plat, acc):
    client = MongoClient(MONGO_STR)
    col = client[MONGO_STR['db']][MONGO_STR['col']]
    _id = '{}_{}'.format(plat, acc)
    data = col.find_one({'_id':_id})
    if data:
        cookie_list = data['cookies']
        cookie = {}
        for cookie_dict in cookie_list:
            cookie[cookie_dict['name']] = cookie_dict['value']
        return cookie

def warning(message):
    """可以接入微信，邮件，短信报警"""
    print(message)
    content = 'date: {} || {} || {}'.format(time.strftime('%Y-%m-%d %H:%M:%S'), platform.node(), message)


def post_data_to_nsq(data, crawl_time=None, _type='xxl'):
    """可以设置数据的处理方式：写入文件、存数据库"""
    pass

def save_ad_cookies(acc, plat, cookies):
    client = MongoClient(MONGO_SETTING['host'], MONGO_SETTING['port'])
    col = client[MONGO_SETTING['db']][MONGO_SETTING['col']]
    _id = '{}_{}'.format(plat, acc)
    col.save(dict(
        _id=_id,
        cookies=cookies,
    ))
    client.close()


def read_ad_cookies(acc, plat):
    client = MongoClient(MONGO_SETTING['host'], MONGO_SETTING['port'])
    col = client[MONGO_SETTING['db']][MONGO_SETTING['col']]
    _id = '{}_{}'.format(plat, acc)
    data = col.find_one({'_id': _id})
    client.close()
    return data['cookies'] if data else []


