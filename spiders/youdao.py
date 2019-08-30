from .decrypt_methed import *
from urllib import parse

url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
ts = int(time.time() * 1000)
word = 'We will be together forever'
salt, bv, sign = get_youdao_sign(word, ts, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36')
post_data = {
    'i': word,
    'client': 'fanyideskweb',
    'salt': salt,
    'sign': sign,
    'version': '2.1',  # 该参数注释后，返回的结果中，翻译的原文丢失，只有翻译后的数据
    'keyfrom': 'fanyi.web',
    # 'from': 'AUTO',
    # 'to': 'AUTO',
    # 'smartresult': 'dict',
    # 'ts': ts,
    # 'bv': bv,
    # 'doctype': 'json',
    # 'action': 'FY_BY_REALTlME'
}
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'OUTFOX_SEARCH_USER_ID=-664740318@101.95.101.90',
    'Referer': 'http://fanyi.youdao.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
}
post_data = parse.urlencode(post_data)
response = requests.post(url, headers=headers, data=post_data)
res_dict = json.loads()
