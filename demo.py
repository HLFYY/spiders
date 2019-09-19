import re
import requests
from base_method import *
from urllib import parse
import pandas as pd
import base64
from lxml import etree
from urllib.parse import urljoin, quote


def ss():
    sheet = pd.read_excel(io='米读书库违禁章节列表(连尚书目集)_20190726.xlsx')
    # workbook = xlrd.open_workbook(file_path)
    dicts = dict()
    for tem in sheet.values:
        title = tem[0]
        chapter = tem[2]
        key = '""' + title + '""'
        chapter_id = re.findall(r'\d+', chapter, re.S)
        if chapter_id:
            chapter_id = int(chapter_id[0])
            if key in dicts:
                dicts[key].append(chapter_id)
            else:
                dicts[key] = [chapter_id]
    print(dicts)
    for key, val in dicts.items():
        print({key: val})





if __name__ == '__main__':
    headers = {
        # 'x-sessionid': 'd6c49f02-c2b3-4353-9048-a592f1126b6d',
        'user-agent': 'OPPO R9m_5.1_weibo_9.8.4_android',
        # 'x-validator': '5tkMdJskFyr2S6dXiJGUGsYIwp3CCCWjw5iTQ0w6t3Y=',
        # 'x-log-uid': '7302121261',
        # 'accept-encoding': 'gzip, deflate',
    }

    set_ = set()
    while True:
        url_pre = 'https://api.weibo.cn/2/searchall?'
        word = '网赚'
        params = {
            'networktype': 'wifi',
            'sensors_device_id': 'none',
            'orifid': '231619',
            'uicode': '10000003',
            'moduleID': '708',
            'featurecode': '10000085',
            'wb_version': '4033',
            'c': 'android',
            's': '8cf9718d',
            'ft': '0',
            'ua': 'OPPO-OPPO R9m__weibo__9.8.4__android__android5.1',
            'wm': '9847_0002',
            'aid': '01AwFT9zIcQYZKOa8Um8_4kXRfKxOgqsYsUOeciokoZ-wmID0.',
            'ext': 'orifid:231619|oriuicode:10000010',
            'fid': '100303type=1&q={}&t=0'.format(word),
            'lat': '31.211262',
            'lon': '121.622143',
            'uid': '7302121261',
            'v_f': '2',
            'v_p': '76',
            'from': '1098495010',
            'gsid': '_2A25wdyd7DeTxGeFN61AQ8i_OzT2IHXVRJT2zrDV6PUJbkdANLVLEkWpNQJgzZhr_JHIdp7hBLUEXK-m9p2ZZir4N',
            'lang': 'zh_CN',
            'lfid': '231619',
            'page': '1',
            'skin': 'default',
            'count': '10',
            'oldwm': '9847_0002',
            'sflag': '1',
            'oriuicode': '10000010',
            'containerid': '100303type=1&q={}&t=0'.format(word),
            'ignore_inturrpted_error': 'true',
            'luicode': '10000010',
            'sensors_mark': '0',
            'android_id': 'ef2c448e09c10aa9',
            'client_key': '1799aaa58503537c953cbd2656cffbc6_1224',
            'need_new_pop': '1',
            'sensors_is_first_day': 'none',
            'container_ext': 'newhistory:0|nettype:wifi|show_topic:1|gps_timestamp:{}'.format(int(time.time() * 1000)),
            'need_head_cards': '1',
            'cum': 'B002BE8C'
        }
        params_new = {key: quote(val, 'utf-8') for key, val in params.items()}
        url = url_pre + parse.urlencode(params)
        print('--'*10)
        response = requests.get(url, headers=headers)
        data_list = json.loads(response.text)['cards']
        print(len(data_list))
        for data in data_list:
            text = data.get('mblog', {}).get('text', '').replace(' ', '').replace(' ', '').replace('\n', '')
            recommend = data.get('mblog', {}).get('recommend', '')
            mblogid = data.get('mblog', {}).get('mblogid', '')
            if mblogid and (mblogid not in set_):
                set_.add(mblogid)
                print(recommend, mblogid, text)
            if text and recommend:
                print('+++++recommend:{}, text:{}'.format(recommend, text))
        time.sleep(2)

