from urllib.parse import quote
from decrypt_methed import *

list_url_index = 'https://weixin.sogou.com/weixinwap?query={}&type=1&ie=utf8&_sug_=y&_sug_type_=&s_from=inputå'
list_url = 'https://weixin.sogou.com/weixinwap?page={}&_rtype=json&query={}&type=1&ie=utf8&_sug_=y&_sug_type_=&s_from=input&'
# 转义符与字符串映射
str_mapping = {'"': '&quot;', '&': '&amp;', '<': '&lt;', '>': '&gt;', ' ': '&nbsp;', "'": '&#39;', '-': '&ndash;'}

def run(word):
    user_agent = random.choice(APP_USER_AGENT)
    pg = 1
    url = list_url_index.format(word)
    cookie = ''
    while True:
        print('==='*20)
        print(url)
        print('==='*20)
        pg += 1
        # 获取搜索页的公众号数据
        referer = 'https://weixin.sogou.com/weixinwap?query={}&type=1&ie=utf8&_sug_=y&_sug_type_=&s_from=input'.format(word)
        headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            # 'Cookie': 'ABTEST=0|1559373999|v1; SUID=6E93E4743F18960A000000005CF228AF; SUV=006D74F274E4936E5CF228B074049498; SUID=6E93E4743118960A000000005CF228B0; IPLOC=CN3100; JSESSIONID=aaak3ff2bNNVJ5d15kkRw; PHPSESSID=8oa4upc7tbaj9tanfalf9ev226; usid=FCLrGR6-dhukSwC8; SNUID=9EFB86B6C7C24C41321E00EDC7BD4CE3',
            'Cookie': cookie,
            'Host': 'weixin.sogou.com',
            'Referer': quote(referer, encoding='utf-8'),
            # 'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'User-Agent': user_agent,
            'X-Requested-With': 'XMLHttpRequest',
        }
        response = requests.get(url, headers=headers, proxies=get_proxy())
        if '此验证码用于确认这些请求是您的正常行为而不是自动程序发出的' in response.content.decode() or '请输入验证码' in response.content.decode():
            print('---被识破为爬虫,要求输入验证码, raw_url:{}, redirect_url:{}'.format(url, response.url))
            return
        if not cookie:
            cookie = response.headers['Set-Cookie']
        # return

        detail_list = []
        if pg != 2:
            try:
                data_dict = json.loads(response.text)
            except:
                if response.url == 'https://weixin.sogou.com/wap':
                    print('----抓取结束，pg:{}'.format(pg))
                else:
                    print('----error, url:{}'.format(response.url))
                return
            author_list = data_dict['items']
            for author_data in author_list:
                # print(author_data)
                detail_url = re.findall(r'CDATA\[(/link.*?)\]', author_data, re.S)[0]
                # print(detail_url)
                detail_list.append(detail_url)
        else:
            html = etree.HTML(response.text)
            # 公众号列表
            author_list = html.xpath('//ul[@class="wx-news-list2"]/li')
            if not author_list:
                print('---未匹配到作者信息, url:{}, response:{}'.format(url, response.content.decode()))
                return
            for author_data in author_list:
                weixin_num = author_data.xpath('.//p[@class="gzh-name"]/text()')[0]
                weixin_name = author_data.xpath('.//p[@class="gzh-tit"]/text()')[0]
                detail_url = author_data.xpath('.//a/@href')[0]
                print(weixin_name, weixin_num, detail_url)
                detail_list.append(detail_url)

        for detail_url in detail_list:
            # 获取公众号主页的真实地址
            time.sleep(1)
            headers['Cookie'] = 'ABTEST=0|1559373999|v1; SUID=6E93E4743F18960A000000005CF228AF; SUV=006D74F274E4936E5CF228B074049498; SUID=6E93E4743118960A000000005CF228B0; IPLOC=CN3100; JSESSIONID=aaak3ff2bNNVJ5d15kkRw; PHPSESSID=8oa4upc7tbaj9tanfalf9ev226; usid=FCLrGR6-dhukSwC8; SNUID=9EFB86B6C7C24C41321E00EDC7BD4CE3'
            res = requests.get(get_sougou_weixin_detail_url(detail_url), headers=headers, proxies=get_proxy())
            url_params = re.findall(r"url.*?\+=.*?'(.*?)';", res.content.decode('utf-8'), re.S)
            author_url = ''.join(url_params)
            if not author_url:
                print('---获取真实链接失败, raw_url:{}, redirect_url:{}'.format(get_sougou_weixin_detail_url(detail_url), res.url))
                break
            print(pg, detail_list.index(detail_url), author_url)
            continue

            # 获取公众号最新的文章
            time.sleep(1)
            response = requests.get(author_url, headers=get_headers())
            if '请输入验证码' in response.content.decode():
                print('---被识破为爬虫,要求输入验证码, raw_url:{}, redirect_url:{}'.format(url, response.url))
                return
            # 文章列表
            article_list = json.loads(re.findall(r'msgList.*?(\{.*?\});', response.content.decode('utf-8'), re.S)[0])['list']
            for article_data in article_list:
                print(article_data['app_msg_ext_info']['title'])
                content_url = article_data['app_msg_ext_info']['content_url']
                content_url = content_url if content_url.startswith('http') else 'https://mp.weixin.qq.com' + content_url
                # 获取的详情页链接中，&字符被转义为&amp;，需进行字符串替换后可正常请求数据
                for str_data, val in str_mapping.items():
                    content_url = content_url.replace(val, str_data)
                print(content_url)

                # 获取文章xiangqing
                time.sleep(1)
                res = requests.get(content_url, headers=get_headers())
                content_html = etree.HTML(res.content.decode())
                title = content_html.xpath('//h2/text()')
                print(title)
                # print(response.content.decode())
                # 提取

        url = list_url.format(pg, word)

if __name__ == '__main__':
    run('北京')
