from tool.warpper import warning
from settings.conf import *
import json
from tool.warpper import post_data_to_nsq, read_ad_cookies
from datetime import datetime


class ExtractData(object):
    def __init__(self, first_page=1, channel_category_id=None, channel_id=None, agent_id=None, plat='', acc=''):
        self.first_page = first_page
        self.plat = plat
        self.acc = acc
        self.total_nums = 0
        self.headers = {}
        self.time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.ad_data = {}
        self.ad_data = {self.plat: []}

        self.channel_category_id = channel_category_id
        self.channel_id = channel_id
        self.agent_id = agent_id
        try:
            assert channel_category_id and channel_id and agent_id, 'classes->extract_data->__init__: channel_id'
        except Exception as e:
            warning(e)
            raise e

    def start_crawl(self):
        """
            流程
        """
        self.set_headers(self.get_cookie())
        data = self.get_next_page_data(self.first_page)
        if not data:
            warning('plat: {}|| classes->extract_data->start_crawl || miss start_crawl_data'.format(self.plat))
            return
        data = json.loads(data, encoding='utf-8')
        self.total_nums = self.get_total_nums(data)
        self.parse(data, self.first_page, self.headers)
        self.deal_end()

    def parse(self, json_data, page, headers):
        info_data = self.get_info_data(json_data)
        if not info_data:
            return

        for item in info_data:
            op = self.extract_item(item)
            self.total_nums -= 1
            if self.total_nums <= 0:
                return
            if str(op) == '0':
                return
            elif str(op) == '1':
                continue
            else:
                pass
        time.sleep(0.8)
        page += 1
        data = self.get_next_page_data(page)
        data = json.loads(data, encoding='utf-8')
        self.parse(data, page, headers)

    def deal_end(self):
        print('-------', self.ad_data)

    def extract_item(self, item):
        """
            解析item数据(放回可以是字符串的 continue, break, return)
        """

    def get_next_page_data(self, page):
        url, form_data = self.get_request_url(page)
        return self.get_data(url, self.headers) if not form_data else self.get_data(url, self.headers, data=form_data)

    def get_request_url(self, page):
        """
            组装请求每页的 url 和formdata
        """
        url = None
        form_data = None
        return url, form_data

    def get_info_data(self, json_data):
        """
            items_list
        """
        return []

    def set_headers(self, cookie):
        """
            设置请求头
        """
        headers = {
            'User-Agent': random.choice(USER_AGENT),
            'Cookie': cookie,
        }
        self.headers = headers

    def get_cookie(self):
        """
            获取cookie
        """
        cookie_list = read_ad_cookies(self.acc, self.plat)
        cookie = ''
        for cookie_dict in cookie_list:
            cookie += '{}={}; '.format(cookie_dict['name'], cookie_dict['value'])
        return cookie

    def get_data(self, url, headers, timeout=30, data=None):
        try:
            proxy = self.get_proxy()
            res = requests.get(url, headers=headers, verify=False, timeout=timeout, proxies=proxy) if not data \
                else requests.post(url, headers=headers, verify=False, data=data, timeout=timeout, proxies=proxy)

            if res.status_code != 200:
                raise Exception('proxy error')
        except:
            try:
                res = requests.get(url, headers=headers, verify=False, timeout=timeout) if not data \
                    else requests.post(url, headers=headers, verify=False, timeout=timeout, data=data)
            except Exception as e:
                warning('访问报错 plat: {} || {}'.format(self.plat, e))
                return False
        return res.text

    def get_proxy(self):
        proxy = random.choice(PROXY_LIST)
        return {
            'http': '{}'.format(proxy),
            'https': '{}'.format(proxy),
        }

    def get_total_nums(self, data):
        """
            获取items总数
        """
        return 0

    def close(self):
        pass

    def extract_first(self, el, xpath, type_=None):
        if not type_:
            return str(el.xpath(xpath)[0]).strip() if el.xpath(xpath) else el.xpath(xpath)
        return type_(str(el.xpath(xpath)[0]).strip()) if el.xpath(xpath) else el.xpath(xpath)

    def append_data(self, name, consumption, view, click, activation=0):
        self.ad_data[self.plat].append(dict(
            name=name,
            consumption=self.transform(consumption, float),
            view=self.transform(view),
            click=self.transform(click),
            activation=self.transform(activation),
            account=self.acc,

            channel_category_id=self.channel_category_id,
            channel_id=self.channel_id,
            agent_id=self.agent_id,
        ))

    def transform(self, data, type_=int):
        data = data if data else 0
        data = 0 if '-' in str(data) else data
        data = str(data).replace(',', '') if ',' in str(data) else data
        return type_(data)

