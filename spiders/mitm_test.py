import redis
import json
import time
import mitmproxy.http
from mitmproxy import ctx
from decrypt_methed import REDIS_SPIDER


class Counter():
    def __init__(self):
        self.r = redis.Redis(**REDIS_SPIDER)

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



addons = [
    Counter()
]
