import requests
import json
from lxml import etree
import time

from public_method import get_sougou_weixin_detail_url

url = 'https://weixin.sogou.com/weixinwap?query=北京&type=1&ie=utf8&_sug_=y&_sug_type_=&s_from=inputå'

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'X-Requested-With': 'XMLHttpRequest',
}
session = requests.Session()
response = session.get(url, headers=headers)
time.sleep(1)
html = etree.HTML(response.text)

data_list = html.xpath('//ul[@class="wx-news-list2"]/li')
for data in data_list:
    weixin_num = data.xpath('.//p[@class="gzh-name"]/text()')[0]
    weixin_name = data.xpath('.//p[@class="gzh-tit"]/text()')[0]
    detail_url = data.xpath('.//a/@href')[0]
    print(weixin_name, weixin_num, detail_url)
    time.sleep(2)
    headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
'Cookie': 'SNUID=7AAB6EDC4C4EC2FED6A846D64CD87921',
'Host': 'weixin.sogou.com',
'Referer': 'https://weixin.sogou.com/weixinwap?query=%E4%B8%8A%E6%B5%B7&type=1&ie=utf8&_sug_=y&_sug_type_=&s_from=input',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
    }
    res = requests.get(get_sougou_weixin_detail_url(detail_url), headers=headers)
    print(res.content.decode())
    time.sleep(3)



