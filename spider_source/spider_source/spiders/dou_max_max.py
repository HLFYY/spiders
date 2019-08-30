# -*- coding: utf-8 -*-
import json
import sys
import logging
import random
import time
from pymongo import MongoClient
import redis
import scrapy
from scrapy_redis.spiders import RedisSpider
from spider_source.settings import BOT_NAME, REDIS_SPIDER, kasi_data_sign, response_retry, MONGO_STR, APP_USER_AGENT

headers_history = {}
r = redis.Redis(**REDIS_SPIDER)


def get_headers():
    global headers_history
    data = r.get('dou_max_max:headers')
    if data:
        headers = json.loads(data.decode())
        # if headers_history != headers:
        #     print('data', data.decode())
        #     print('headers_history', headers_history)
        headers_history = headers
    else:
        headers = headers_history
    if headers:
        # for key in ['referer']:
        #     if key in headers:
        #         del headers[key]
        # headers['User-Agent'] = random.choice(APP_USER_AGENT)
        return headers
    else:
        sys.exit()
    # headers = {
    #     'charset': 'utf-8',
    #     'Accept-Encoding': 'gzip',
    #     'referer': 'https://servicewechat.com/wxb921d1f536e87f5e/119/page-frame.html',
    #     'd1': '8767423672',
    #     'd4': '3802929732',
    #     'd2': '2745103300',
    #     'd5': '1914578416',
    #     'content-type': 'application/json',
    #     'd3': '1119023001',
    #     'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1; OPPO R9m Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36 MicroMessenger/7.0.6.1460(0x27000634) Process/appbrand0 NetType/WIFI Language/zh_CN',
    #     'Host': 'xcx.meizhuahuyu.com',
    #     'Connection': 'Keep-Alive'
    # }
    # return headers

# tokens = ['d34baa81885d39fdf2fbafd7b61d648b', 'f8ed4340eb8e42d79bcc34fe32e2724a']
tokens = ['d34baa81885d39fdf2fbafd7b61d648b']
mcn_list_url = 'https://xcx.meizhuahuyu.com/douyin/xcx/mcn/list?token={}&page={}&pageSize=10&keywords='
mcn_detail_url = 'https://xcx.meizhuahuyu.com/douyin/xcx/mcn/detail?token={}&page={}&pageSize=10&mcnId={}'
person_detail_url = 'https://xcx.meizhuahuyu.com/douyin/xcx/dyuser/details/{}?token={}&date=1'


class DouMaxMaxSpider(scrapy.Spider):
    name = 'dou_max_max'
    allowed_domains = ['']
    start_urls = ['']

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'LOG_LEVEL': 'INFO',
        # 'LOG_FILE': os.path.join(LOG_DIR, '{}.log'.format(name)),
    }

    def start_requests(self):
        url = mcn_list_url.format(random.choice(tokens), 0)
        yield scrapy.Request(url, headers=get_headers(), meta={'data_count': 0, 'page':0}, dont_filter=True)

    def parse(self, response):
        data_count = response.meta['data_count']
        page = response.meta['page']
        try:
            res_dict = json.loads(response.text)
        except:
            yield response_retry(response, data_log={'url':response.url}, retry_times_max=2)
            return
        if not res_dict.get('result'):
            logging.error('>>>>机构列表页, response is not result, response:{}'.format(res_dict))
            return
        total = res_dict['result']['count']
        data_list = res_dict['result']['items']
        if data_list:
            for data in data_list:
                data_count += 1
                ccpush = {
                    'spider_source:dou_max_max_experts': data['mcnId'],
                }
                item = dict(
                    ccpush=ccpush,
                )
                yield item

            if data_count < total:
                next_url = mcn_list_url.format(random.choice(tokens), page+1)
                yield scrapy.Request(next_url, headers=get_headers(), meta={'data_count': data_count, 'page': page+1}, dont_filter=True)
            else:
                logging.info('----机构抓取完成, page:{}, data_count:{}, total:{}'.format(page, data_count, total))
        else:
            logging.info('----机构抓取完成, page:{}, data_count:{}, total:{}'.format(page, data_count, total))


class DouMaxMaxExpertsSpider(RedisSpider):
    name = 'dou_max_max_experts'
    allowed_domains = ['']
    redis_key = '{}:{}'.format(BOT_NAME, name)

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'LOG_LEVEL': 'INFO',
        # 'LOG_FILE': os.path.join(LOG_DIR, '{}.log'.format(name)),
    }

    def make_request_from_data(self, mcn_id):
        mcn_id = mcn_id.decode()
        detail_url = mcn_detail_url.format(random.choice(tokens), 0, mcn_id)
        return scrapy.Request(detail_url, callback=self.parse_detail, headers=get_headers(), meta={'data_count': 0, 'page': 0, 'mcn_id': mcn_id}, dont_filter=True)

    def parse_detail(self, response):
        data_count = response.meta['data_count']
        page = response.meta['page']
        mcn_id = response.meta['mcn_id']

        try:
            res_dict = json.loads(response.text)
        except:
            yield response_retry(response, data_log={'url': response.url}, retry_times_max=2)
            return
        if not res_dict.get('result'):
            logging.error('>>>>达人列表页, response is not result, response:{}'.format(res_dict))
            if '账号异常' in response.text:
                print('账号异常, 休眠后重试, result:{}'.format(res_dict))
                time.sleep(30)
                if not response.meta.get('try'):
                    yield scrapy.Request(response.url, callback=self.parse_detail, headers=get_headers(), meta={'data_count': data_count, 'page': page, 'mcn_id': mcn_id, 'try': 'try'}, dont_filter=True)
            return
        total = res_dict['result']['count']
        data_list = res_dict['result']['items']
        if data_list:
            mcn = res_dict['result']['mcn']
            for data in data_list:
                data_count += 1
                pass_data = dict(
                    mcn_name=mcn['mcnName'],
                    company_name=mcn['companyName'],
                    tag_name=mcn['tagName'],
                    mcn_desc=mcn['mcnDesc'],
                    user_name=data['douyinName'],
                    fans=data['fansNumber'],
                    digg_count=data['likeNumber'],
                    videos=data['videoNumber'],
                    _id=data['dyuserId'],
                )
                ccpush={
                    'spider_source:kasi_search': json.dumps(pass_data),
                }
                item = dict(dict(
                    _id=data['dyuserId'],
                    mcn=mcn,
                    ccpush=ccpush,
                    save_type='replace',
                ), **data)
                yield item

            if data_count < total:
                next_url = mcn_detail_url.format(random.choice(tokens), page + 1, mcn_id)
                yield scrapy.Request(next_url, callback=self.parse_detail, headers=get_headers(), meta={'data_count': data_count, 'page': page+1, 'mcn_id': mcn_id}, dont_filter=True)
            else:
                logging.info('----达人抓取完成, mcn_namemcn_id:{}, page:{}, data_count:{}, total:{}'.format(mcn_id, page, data_count, total))
        else:
            logging.info('----达人抓取完成, mcn_id:{}, page:{}, data_count:{}, total:{}'.format(mcn_id, page, data_count, total))


class KasiSearchSpider(RedisSpider):
    name = 'kasi_search'
    allowed_domains = []
    redis_key = '{}:{}'.format(BOT_NAME, name)

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'LOG_LEVEL': 'INFO',
    }

    search_url = 'https://api.data.caasdata.com/searchs?keyword={}'
    detail_url = 'https://api.data.caasdata.com/channels/{}/detail_page'
    data_url = 'https://api.data.caasdata.com/channels/{}/ta'

    def __init__(self):
        self.client = MongoClient(MONGO_STR)
        self.collection = self.client[BOT_NAME][self.name]
        logging.info('---db:{}, tables:{}'.format(BOT_NAME, self.name))

    def get_headers(self, key_word=''):
        time_raw = time.time()
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'salt': str(int(time_raw * 1000)),
            'sign': kasi_data_sign(time_raw, key_word),
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }
        return headers

    def make_request_from_data(self, data):
        data = json.loads(data)
        if not self.collection.find_one({'_id': data['_id']}):
            url = self.search_url.format(data['user_name'])
            headers = self.get_headers(data['user_name'])
            return scrapy.Request(url, headers=headers, meta={'pass_data': data}, dont_filter=True)
        else:
            logging.info('---已存在, id:{}'.format(data['_id']))

    def parse(self, response):
        pass_data = response.meta['pass_data']
        res_dict = json.loads(response.text)
        user_data, is_douyin = {}, 0
        for data in res_dict['data']['list']:
            if data['ptitle'] == pass_data['user_name'] and 'douyin.png' in data.get('platform_icon', ''):
                user_data = data
                is_douyin = 1
                break
            elif data['ptitle'] == pass_data['user_name']:
                user_data = data
        if not user_data:
            logging.info('---未搜索到对应作者, user_name:{}, mcn:{}'.format(pass_data['user_name'], pass_data['mcn_name']))
            item=dict(dict(
                is_search=0,
                save_type='replace',
            ), **pass_data)
            yield item
        else:
            logging.info('---搜索到作者, user_name:{}, mcn:{}, is_douyin:{}'.format(pass_data['user_name'], pass_data['mcn_name'], is_douyin))
            item = dict(dict(
                is_search=1,
                is_douyin=is_douyin,
                platform_icon='https://pic.caasdata.com/' + user_data['platform_icon'] if user_data.get('platform_icon') else '',
                kasi_id=user_data['id'],
            ), **pass_data)
            url = self.detail_url.format(user_data['id'])
            headers = dict(dict(
                Authorization='Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FwaS5kYXRhLmNhYXNkYXRhLmNvbS9hdXRoIiwiaWF0IjoxNTY1NjExOTg3LCJleHAiOjE1NjgyMDM5ODcsIm5iZiI6MTU2NTYxMTk4NywianRpIjoieDluckNHdDloZjdFbXpDRCIsInN1YiI6Ijg3NTQ2IiwiTG9naW5Ub2tlbiI6ImFsMFBhOGttWjZtdHMifQ.yNeka_1Os_OP4G1mAAz6KYW_aNHDzeNWrZ2zH28W5RU',
            ), **self.get_headers())
            yield scrapy.Request(url, callback=self.parse_detail, headers=headers, meta={'item': item}, dont_filter=True)

    def parse_detail(self, response):
        item = response.meta['item']
        res_dict = json.loads(response.text)

        data = res_dict['data']

        tags = []
        for key, val in data.items():
            if 'Tags' in key:
                for dd in val.get('data', []):
                    tags.append(dd.get('title', ''))

        if data.get('videoData'):
            video_data=dict(
                videos_kasi=data['videoData']['data']['video_count'],
                videos_per_work=round(int(data['videoData']['data']['video_count']) * 7 / 90, 1),
                low_hot=data['videoData']['data']['hot_video']['low_hot'],
                middle_hot=data['videoData']['data']['hot_video']['middle_hot'],
                high_hot=data['videoData']['data']['hot_video']['high_hot'],
                has_video_data=1,
            )
        else:
            video_data = dict(
                videos_kasi=0,
                videos_per_work=0,
                low_hot=0,
                middle_hot=0,
                high_hot=0,
                has_video_data=0,
            )

        item = dict(dict(
            save_type='replace',
            platform_url=data['url'],
            weibo_url=data.get('weibo', {}).get('data', {}).get('url', '') if data.get('weibo', {}).get('data') else '',
            tags=','.join(tags),
            per_comment_count=int(float(data['comment_average'])),
            per_digg_count=int(float(data['up_average'])),
            per_share_count=int(float(data['share_average'])),
        ), **video_data, **item)
        if item['has_video_data']:
            url = self.data_url.format(item['kasi_id'])
            headers = dict(dict(
                Authorization='Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FwaS5kYXRhLmNhYXNkYXRhLmNvbS9hdXRoIiwiaWF0IjoxNTY1NjExOTg3LCJleHAiOjE1NjgyMDM5ODcsIm5iZiI6MTU2NTYxMTk4NywianRpIjoieDluckNHdDloZjdFbXpDRCIsInN1YiI6Ijg3NTQ2IiwiTG9naW5Ub2tlbiI6ImFsMFBhOGttWjZtdHMifQ.yNeka_1Os_OP4G1mAAz6KYW_aNHDzeNWrZ2zH28W5RU',
            ), **self.get_headers())
            yield scrapy.Request(url, callback=self.parse_data, headers=headers, meta={'item': item}, dont_filter=True)
        else:
            item['age_data'] = {}
            yield item

    def parse_data(self, response):
        item = response.meta['item']
        res_dict = json.loads(response.text)

        age_xdata = res_dict['data']['ta']['data']['age']['xdata']
        age_ydata = res_dict['data']['ta']['data']['age']['ydata']
        temp = {}
        for index in range(len(age_xdata)):
            temp['age_{}'.format(age_xdata[index])] = age_ydata[index]
        item['age_data'] = temp
        yield item





