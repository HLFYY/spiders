import random

from classes import extract_data
import requests
import json
from datetime import datetime
from tool.warpper import warning, post_data_to_nsq
import time


class BaiduExtract(extract_data.ExtractData):
    today_str = datetime.now().strftime('%Y-%m-%d')

    def __init__(self, acc, *args, **kwargs):
        super(BaiduExtract, self).__init__(*args, **kwargs)
        self.acc = acc
        self.first_page = 0

    def get_request_url(self, page):
        url = 'http://baitong.baidu.com/request.ajax?path=appads/GET/plan/index/list&reqid={}_{}'.format(int(time.time()*1000), random.randint(11, 99))
        return url, ''

    def get_info_data(self, json_data):
        return json_data.get('data').get('listData')

    def parse(self, json_data, page, headers):
        info_data = self.get_info_data(json_data)
        if not info_data:
            return

        for item in info_data:
            op = self.extract_item(item)
            if str(op) == '0':
                continue
            elif str(op) == '1':
                continue
            else:
                pass
        time.sleep(0.8)

    def extract_item(self, item):
        name = item.get('planName')
        consumption = item.get('report').get('consume')
        view_count = 0
        click_count = item.get('report').get('data')[-1]['value']
        activation = 0

        consumption = 0 if '-' in str(consumption) else consumption
        view_count = 0 if '-' in str(view_count) else int(view_count)
        click_count = 0 if '-' in str(click_count) else int(click_count)

        status = item.get('planStatusText').strip()
        if status not in ['有效', '预算不足下线']:
            return '0'
        self.ad_data[self.plat].append(dict(
            name=name,
            consumption=consumption,
            view=view_count,
            click=click_count,
            activation=activation,
            account=self.acc,

            channel_category_id=self.channel_category_id,
            channel_id=self.channel_id,
            agent_id=self.agent_id,
        ))

    def get_data(self, url, headers, timeout=30, data=None):
        try:
            res = requests.get(url, headers=headers, verify=False, timeout=timeout) if not data \
                else requests.post(url, headers=headers, verify=False, timeout=timeout, data=data)
        except Exception as e:
            warning('访问报错 plat: {} || {}'.format(self.plat, e))
            return False
        return res.text

    def deal_end(self):
        self.ad_data['baitong_app'] = self.ad_data['baidu']
        del self.ad_data['baidu']
        #print('--', self.ad_data)
