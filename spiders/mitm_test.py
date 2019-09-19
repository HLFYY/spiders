import redis
import json
import time
import mitmproxy.http
from decrypt_methed import REDIS_SPIDER, MONGO_STR
# from pymongo import MongoClient



class Counter():
    def __init__(self):
        self.r = redis.Redis(**REDIS_SPIDER)
        # self.client = MongoClient(**MONGO_STR)
        # self.col = self.client['feed']['weili']
        self.set_ = set()

    def request(self, flow: mitmproxy.http.HTTPFlow):
        if 'https://xcx.meizhuahuyu.com/douyin/xcx/mcn' in flow.request.url:
            print(flow.request.url)
            headers = flow.request.headers
            dicts = {}
            for key, val in headers.items():
                # print(data, type(data))
                # if key in ['d1', 'd2', 'd3', 'd4', 'd5']:
                dicts[key] = val
            print(time.strftime("%Y-%m-%d %H:%M:%S"), dicts)
            self.r.set('dou_max_max:headers', json.dumps(dicts))

    def response(self, flow: mitmproxy.http.HTTPFlow):
        if '_gscu_2116842793' in flow.response.headers.get('Set-Cookie', ''):
            print(flow.request.url)
            print(flow.request.headers)
        if 'List/List?sorttype' in flow.request.url:
            # print(flow.response.text)
            print(flow.response.headers.get('Set-Cookie'))
        if 'https://pc.weilitoutiao.net/peacock/api/zhwnl/v4/headline?' in flow.request.url:
            data_list = json.loads(flow.response.text)['data']['list']
            for data in data_list:
                if '网赚' in data['title'] or '赚钱' in data['title'] or '快来' in data['title']:
                    print(data['title'], data['share_link'])
                    self.r.rpush('weili_ad', 'title:{}, url:{}'.format(data['title'], data['share_link']))
                # if 'post_id' in data:
                #     # if data['post_id'] not in self.set_:
                #     #     self.set_.add(data['post_id'])
                #     #     print(data['title'], data['share_link'])
                #     if '网赚' in data['title'] or '赚钱' in data['title'] or '快来' in data['title']:
                #         print(data['title'], data['share_link'])
                #         self.r.rpush('weili_ad', 'title:{}, url:{}'.format(data['title'], data['share_link']))
                # else:
                #     print(data)
        if 'api.weibo.cn/2/searchall' in flow.request.url or 'api.weibo.cn/2/statuses/unread_friends_timeline' in flow.request.url:
            print('==='*10)
            print(flow.request.url)
            print(flow.request.get_text())
            print(flow.request.headers.get('user-agent'))
            print('==='*10)





addons = [
    Counter()
]
