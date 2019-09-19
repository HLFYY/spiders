import base64
import json
import random
import re
import time

import requests
from decrypt_methed import get_headers
from lxml import etree
from urllib.parse import quote, urlsplit

words = [
        '#推文超话#',
        '#推文总结#',
        '#强推文#',
        '#bl推文#',
        '#言情推文#',
        '#每日推文#',
        '#灵异文#',
        '#推文#',
        '#推文少女#',
        '#推文bl#',
        '#甜宠文推荐#',
        '#推文bg#',
        '#推文bl肉#',
        '#推文日记#',
        '#推文扫文每日盘点#',
        '#推文君安利时间#'
    ]

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': 'SUB=_2A25wdkwnDeRhGeBH4lAU9SvKyjyIHXVTAjrvrDV8PUNbmtAKLUXfkW9NQYln30D5jgv6ItWpLNqXLZMBcykcgnsP',
        # 'Cookie': 'SUB=_2A25wdjyeDeRhGeFO6lQQ8irNwz6IHXVTAilWrDV8PUNbmtAKLXKkkW9NQZOqdEIPgQM-XQo71IJx4BVx8u6D1qpJ',
        'Cookie': 'SUB=',

    # 'Host': 's.weibo.com',
        # 'Referer': 'https://s.weibo.com/weibo?q=%23%E6%8E%A8%E6%96%87%E8%B6%85%E8%AF%9D%23&Refer=weibo_weibo',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    }

def weibo_theme(word):
    # url = 'https://s.weibo.com/hot?q={}&xsort=hot&suball=1&tw=hotweibo&Refer=weibo_hot&page=2'.format(quote(word, 'utf-8'))
    url = 'https://s.weibo.com/weibo?q={}&Refer=hot_weibo&page=2'.format(quote(word, 'utf-8'))
    response = requests.get(url, headers=headers)
    # print(response.text)
    print('=='*10, word)
    html = etree.HTML(response.text)
    data_list = html.xpath('//div[@id="pl_feedlist_index"]//div[@class="card"]')
    for data in data_list:
        content = data.xpath('.//div[@class="content"]/p[@class="txt"][last()]//text()')
        print(''.join(content).strip().replace('收起全文d', ''))
    time.sleep(1)

def weibo_author(url):
    # headers['Host'] = 'www.weibo.com'
    response = requests.get(url, headers=headers)
    print(response.text)
    html = etree.HTML(response.text)
    is_login = html.xpath('//div[@class="m-hint"]/a[@action-type="login"]/text()')
    if is_login and '立即登录' in is_login[0]:
        print(is_login)
    else:
        print('====')
    # for data in response.headers.get('Set-Cookie').split(';'):
    #     if 'SUB=' in data:
    #         _, sub_data = data.split('=')
    # print(sub_data)
    # data_dict = json.loads(re.findall(r'\((\{.*?\})\)', response.text, re.S)[0])
    # html_data = data_dict['html']
    #
    # if html_data:
    #     html_data = etree.HTML(html_data)
    #     data_list = html_data.xpath('//div[@action-type="feed_list_item"]')
    #     for data in data_list:
    #         content = data.xpath('.//div[@node-type="feed_list_content"]//text()')
    #         content = ''.join(content).strip()
    #         print(content)


if __name__ == '__main__':
    # for word in words:
    #     weibo_theme(word)
    # weibo_author('https://www.weibo.com/u/5032972504?profile_ftype=1&is_all=1')
    # weibo_author('https://www.weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=2&pagebar=0&pl_name=Pl_Official_MyProfileFeed__20&id=1005055032972504&script_uri=/u/5032972504&feed_type=0&pre_page=2&domain_op=100505&__rnd=1567741223142')
    # weibo_author('https://www.weibo.com/bookreview?pids=Pl_Official_MyProfileFeed__27&is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=2&ajaxpagelet=1&ajaxpagelet_v6=1&__ref=/bookreview?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=1#feedtop&_t=FM_156818546619432')
    # weibo_author('https://login.sina.com.cn/visitor/visitor?a=crossdomain&cb=return_back&s=_2AkMqJDC8f8NxqwJRmPAVz2zqZIhzyQDEieKceMFnJRMxHRl-yT83qhwJtRB6AaQeU5VrcuGF5hYfWTBZ-5LA2YI0GQ_-&sp=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhrSe8zw4h7K0yTQVfSyKgo&from=weibo&_rand=0.9912247784610713')
    weibo_author('https://s.weibo.com/hot?q=%23bl%E6%8E%A8%E6%96%87%23&xsort=hot&suball=1&tw=hotweibo&Refer=realtime_hot')