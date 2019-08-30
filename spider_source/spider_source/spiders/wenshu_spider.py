# -*- coding: utf-8 -*-
import re
import json
import scrapy
import execjs
from urllib import parse
from spider_source.lib import random_str


class WenshuSpiderSpider(scrapy.Spider):
    name = 'wenshu_spider'
    allowed_domains = ['']
    start_urls = ['http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1+AJLX++案件类型:刑事案件']

    def __init__(self):
        with open('code_js/wenshu_vl5x.js', 'r') as f:
            self.js_data = f.read()

    def get_wenshu_vl5x(self, vjkl5):
        js_data = self.js_data.replace('572f1d93ff9d70a801561801e7baf21e53ec2f65', vjkl5)
        context = execjs.compile(js_data)
        sign = context.call("getKey")
        return sign

    def parse(self, response):
        set_cookie = response.headers.get('Set-Cookie', '')
        vjkl5 = re.findall(r'vjkl5=([^;]+)', set_cookie.decode(), re.S)[0]
        print(vjkl5)
        url = 'http://wenshu.court.gov.cn/List/ListContent'
        data = {
            'Param': '案件类型:民事案件',
            'Index': '1',
            'Page': '10',
            'Order': '法院层级',
            'Direction': 'asc',
            'vl5x': self.get_wenshu_vl5x(vjkl5),
            'number': 'wens',
            'guid': '{}-{}-{}-{}'.format(random_str(8), random_str(4), random_str(8), random_str(12)),
        }
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '237',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'wenshu.court.gov.cn',
            'Origin': 'http://wenshu.court.gov.cn',
            'Referer': 'http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        cookies = {
           '_gscu_2116842793': '58355596svcohx13',
           '_gscs_2116842793': '65258175o07y5692|pv:1',
           # 'vjkl5': vjkl5,

        }
        # yield scrapy.Request(url, callback=self.parse_list, headers=headers, cookies=cookies, body=json.dumps(data), method='POST', dont_filter=True)
        yield scrapy.FormRequest(url, callback=self.parse_list, headers=headers, cookies=cookies, formdata=data, dont_filter=True)

    def parse_list(self, response):
        data_list = json.loads(response.text)
        for data in data_list:
            print(data)
