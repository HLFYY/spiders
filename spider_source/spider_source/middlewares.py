# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import base64
from scrapy import signals
from spider_source.settings import *


class VpsProxyMiddleware(object):
    def process_request(self, request, spider):
        try:
            proxy_dict = get_proxy()
            if proxy_dict:
                if request.url.startswith("http://"):
                    request.meta['proxy'] = proxy_dict['http']  # http代理
                elif request.url.startswith("https://"):
                    request.meta['proxy'] = proxy_dict['https']
                else:
                    logging.error('>>>>url不是http&https, url:{}'.format(request.url))
            else:
                logging.error('>>>>获取代理失败， proxy_dict:{}'.format(proxy_dict))
        except Exception as e:
            logging.error('>>>>请求代理失败, error:{}'.format(e))


class ExceptMiddleware(object):
    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status > 400 and response.status not in [404, 429]:
            error_time = request.meta.get('error_time', 0)
            if error_time < 2:
                request.meta['error_time'] = error_time + 1
                return request
            else:
                logging.error(">>>>响应码大于400, url:{}, status:{}, error_time:{}".format(response.url, response.status, error_time))
        elif response.status >= 400:
            print(request.headers)
            print(response.text)
        return response

    def process_exception(self, request, exception, spider):
        # 出现异常时（超时）使用代理
        if request.url.startswith('http'):
            error_time = request.meta.get('error_time', 0)
            if error_time < 4:
                # logging.info("----出现错误, 更换代理, error_time: {}, url:{}".format(error_time, request.url[60:150]))
                request.meta['error_time'] = error_time + 1
                return request


def proxy_authentica(r, request, spider_name, status_code):
    proxy = r.rpoplpush('proxy_pool', 'proxy_pool')
    proxyUser, proxyPass = proxy.decode('utf8').split('~')
    proxyUser, proxyPass = proxyUser.strip(), proxyPass.strip()
    proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")
    request.meta['proxy'] = "http://http-dyn.abuyun.com:9020"
    request.headers['Proxy-Authorization'] = proxyAuth


class PubliceProxyMiddleware():
    def __init__(self):
        self.r = redis.Redis(**REDIS_PROXY)

    def process_request(self, request, spider):
        # 判断请求是否使用代理，没有代理则添加代理
        if 'http-dyn.abuyun.com' not in str(request.meta.get('proxy')):
            proxy_authentica(self.r, request, spider.name, 0)

    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        if response.status == 429:
            proxy_authentica(self.r, request, spider.name, 1)
            return request
        return response