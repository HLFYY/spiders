
from string import ascii_lowercase
import random

def get_sougou_weixin_detail_url(url):
    '''搜狗微信，列表页获取的url进行处理，返回真实url'''
    url = url if url.startswith('http') else 'https://weixin.sogou.com' + url
    k_data = random.randint(1, 100)
    h_data = url.index('url=')
    c_data = url.index('&k=') if '&k=' in url else -1
    print(k_data, h_data, c_data)

    if h_data != -1 and c_data == -1:
        h_data = url[h_data+ 30 + k_data:h_data+ 31 + k_data]
        return url + '&k=' + str(k_data) + '&h=' + str(h_data)
    else:
        return url


def random_str(count):
    str_data = ascii_lowercase + '0123456789'
    return ''.join([random.choice(str_data) for _ in range(count)])