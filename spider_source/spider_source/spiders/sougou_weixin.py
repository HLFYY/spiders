# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from spider_source.settings import *
from urllib.parse import quote
from spider_source.lib import *


class SougouWeixinSpider(RedisSpider):
    name = 'weixin_search'
    allowed_domains = []
    redis_key = '{}:{}'.format(BOT_NAME, name)

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        # 'LOG_LEVEL': 'INFO',
        # 'LOG_FILE': os.path.join(LOG_DIR, '{}.log'.format(name)),
    }

    public_search_url_index = 'https://weixin.sogou.com/weixinwap?query={word}&type=1&ie=utf8&_sug_=y&_sug_type_=&s_from=inputå'
    public_search_url = 'https://weixin.sogou.com/weixinwap?page={page}&_rtype=json&query={word}&type=1&ie=utf8&_sug_=y&_sug_type_=&s_from=input&'

    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'weixin.sogou.com',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'X-Requested-With': 'XMLHttpRequest',
    }
    referer = 'https://weixin.sogou.com/weixinwap?query={}&type=1&ie=utf8&_sug_=y&_sug_type_=&s_from=input'

    def make_requests_from_url(self, word):
        url = self.public_search_url_index.format(word=word)
        meta = {'word': word, 'page': 1, 'data_count': 0, 'cookiejar': '{}_{}'.format(word, random.randint(10,100))}
        self.headers['Referer'] = quote(self.referer.format(word), encoding='utf-8')
        return scrapy.Request(url, headers=self.headers, meta=meta, dont_filter=True)

    def parse(self, response):
        print(response.request.headers)
        word = response.meta['word']
        page = response.meta['page']
        data_count = response.meta['data_count']

        if '此验证码用于确认这些请求是您的正常行为而不是自动程序发出的' in response.text or '请输入验证码' in response.text:
            logging.info('---被识破为爬虫,要求输入验证码, url:{}, word:{}, page:{}'.format(response.url, word, page))
            return

        detail_list = []
        if page == 1:
            html = etree.HTML(response.text)
            # 公众号列表
            author_list = html.xpath('//ul[@class="wx-news-list2"]/li')
            if not author_list:
                logging.info('---未匹配到作者信息, url:{}, word:{}'.format(response.url, word))
                return
            for author_data in author_list:
                # weixin_num = author_data.xpath('.//p[@class="gzh-name"]/text()')[0]
                # weixin_name = author_data.xpath('.//p[@class="gzh-tit"]/text()')[0]
                detail_url = author_data.xpath('.//a/@href')[0]
                # print(weixin_name, weixin_num, detail_url)
                detail_list.append(detail_url)
        else:
            try:
                data_dict = json.loads(response.text)
            except:
                if response.url == 'https://weixin.sogou.com/wap':
                    logging.info('----抓取结束，word:{}, page:{}, data_count:{}'.format(word, page, data_count))
                else:
                    logging.error('----loads is wrong, url:{}, word:{}, page:{}'.format(response.url, word, page))
                return
            author_list = data_dict['items']
            for author_data in author_list:
                detail_url = re.findall(r'CDATA\[(/link.*?)\]', author_data, re.S)[0]
                detail_list.append(detail_url)

        for detail_url in detail_list:
            detail_url = get_sougou_weixin_detail_url(detail_url)
            data_count += 1
            # yield {'redis_key': '{}:weixin_author_url'.format(BOT_NAME), "_id": '{}~~{}'.format(detail_url, word)}

        print(page, len(detail_list))

        if page < 10:
            next_url = self.public_search_url.format(page=page, word=word)
            meta = {'word': word, 'page': page+1, 'data_count': data_count, 'cookiejar': response.meta['cookiejar']}
            yield scrapy.Request(next_url, headers=self.headers, meta=meta, dont_filter=True)
        else:
            logging.info('----抓取结束，word:{}, page:{}, data_count:{}'.format(word, page, data_count))

class WeixinAuthorUrlSpider(SougouWeixinSpider):
    name = 'weixin_author_url'
    allowed_domains = []
    redis_key = '{}:{}'.format(BOT_NAME, name)

    def make_requests_from_url(self, data):
        url, word = data.split('~~')
        self.headers['Referer'] = quote(self.referer.format(word), encoding='utf-8')
        self.headers['Cookie'] = 'ABTEST=0|1559373999|v1; SUID=6E93E4743F18960A000000005CF228AF; SUV=006D74F274E4936E5CF228B074049498; SUID=6E93E4743118960A000000005CF228B0; IPLOC=CN3100; JSESSIONID=aaak3ff2bNNVJ5d15kkRw; PHPSESSID=8oa4upc7tbaj9tanfalf9ev226; usid=FCLrGR6-dhukSwC8; SNUID=9EFB86B6C7C24C41321E00EDC7BD4CE3'
        meta = {'word': word, 'raw_url':url, 'cookiejar': '{}_{}'.format(word, random.randint(10,100))}
        return scrapy.Request(url, headers=self.headers, meta=meta, dont_filter=True)

    def parse(self, response):
        print(response.request.headers)
        word = response.meta['word']
        raw_url = response.meta['raw_url']

        url_params = re.findall(r"url.*?\+=.*?'(.*?)';", response.text, re.S)
        author_url = ''.join(url_params)
        if not author_url:
            print('---获取真实链接失败, raw_url:{}, redirect_url:{}'.format(raw_url, response.url))
            return
        print(author_url)