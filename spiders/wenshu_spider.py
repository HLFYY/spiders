from string import ascii_lowercase
from urllib import parse
from .decrypt_methed import *
import execjs


def get_wenshu_vl5x(vjkl5):
    with open('code_js/wenshu_vl5x.js', 'r') as f:
        js_data = f.read()
    js_data = js_data.replace('572f1d93ff9d70a801561801e7baf21e53ec2f65', vjkl5)
    context = execjs.compile(js_data)
    sign = context.call("getKey")
    print(sign)
    return sign

def random_str(count):
    str_data = ascii_lowercase + '0123456789'
    return ''.join([random.choice(str_data) for _ in range(count)])

def request_list_data(vjkl5):
    url = 'http://wenshu.court.gov.cn/List/ListContent'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '237',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '_gscu_2116842793=58355596svcohx13; vjkl5={}; _gscs_2116842793=65258175o07y5692|pv:1'.format(vjkl5),
        'Host': 'wenshu.court.gov.cn',
        'Origin': 'http://wenshu.court.gov.cn',
        'Referer': 'http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    vl5x = get_wenshu_vl5x(vjkl5)
    for i in range(1, 10):
        data = {
            'Param': '案件类型:行政案件',
            'Index': str(i),
            'Page': '10',
            'Order': '法院层级',
            'Direction': 'asc',
            'vl5x': vl5x,
            # 'number': 'wens',
            'number': '0.13318365043432667',
            'guid': '{}-{}-{}-{}'.format(random_str(8), random_str(4), random_str(8), random_str(12)),
        }
        response = requests.post(url, data=parse.urlencode(data), headers=headers)
        data_dict = json.loads(json.loads(response.text))
        print(data_dict)
        for data in data_dict:
            if data.get('案件名称'):
                print(data.get('案件名称'))
        print('==='*10)
        time.sleep(1)


if __name__ == '__main__':
    url = 'http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1+AJLX++案件类型:刑事案件'
    headers = dict(dict(
        # Cookie='_gscu_2116842793=65332249qwerl17'
    ), **get_headers())
    # response = requests.get(url, headers=headers)
    # set_cookie = response.headers.get('Set-Cookie', '')
    # vjkl5 = re.findall(r'vjkl5=([^;]+)', set_cookie, re.S)[0]
    # print(vjkl5)
    # vjkl5 = "4820193fffe70d201a518e279c26fe673f4e7052"
    # '7d91393ff0e715b019f1831b865b91a7b61cc25a'
    # 'd19393ffd7709c01fb1846ed824cf997be0ab64b'
    # 'c9b9bf8793ffd7705f01d41801f6942d7c44c987'
    request_list_data('61b7093f4771eb015e189447ce3b43cbc9ef559')