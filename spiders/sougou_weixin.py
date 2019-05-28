from urllib.parse import quote
from public_method import *

list_url = 'https://weixin.sogou.com/weixinwap?query={}&type=1&ie=utf8&_sug_=y&_sug_type_=&s_from=inputå'
# 转义符与字符串映射
str_mapping = {'"': '&quot;', '&': '&amp;', '<': '&lt;', '>': '&gt;', ' ': '&nbsp;', "'": '&#39;', '-': '&ndash;'}

def run(word):
    # 获取搜索页的公众号数据
    url = list_url.format(word)
    response = requests.get(url, headers=get_headers('app'))
    if '此验证码用于确认这些请求是您的正常行为而不是自动程序发出的' in response.content.decode() or '请输入验证码' in response.content.decode():
        print('---被识破为爬虫,要求输入验证码, raw_url:{}, redirect_url:{}'.format(url, response.url))
        return

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

        # 获取公众号主页的真实地址
        time.sleep(1)
        headers = dict(dict(
            Cookie='SNUID=7AAB6EDC4C4EC2FED6A846D64CD87921',
            Referer=quote(url, encoding='utf-8'),
            Host='weixin.sogou.com',
        ), **get_headers())
        res = requests.get(get_sougou_weixin_detail_url(detail_url), headers=headers)
        url_params = re.findall(r"url.*?\+=.*?'(.*?)';", res.content.decode('utf-8'), re.S)
        author_url = ''.join(url_params)
        if not author_url:
            print('---获取真实链接失败, raw_url:{}, redirect_url:{}'.format(get_sougou_weixin_detail_url(detail_url), res.url))
            return
        print(author_url)

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

if __name__ == '__main__':
    run('北京')



