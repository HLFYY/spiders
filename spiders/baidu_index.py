import time

import requests
import json

from public_method import decrypt_baidu_index_response

url = 'https://index.baidu.com/Interface/Newwordgraph/getIndex?region=0&startdate=20190518&enddate=20190524&wordlist[0]=华为'
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'BDUSS=dqQkJuSVF-bEJWNU1pUGs3Y1B5Mm5ONGt2SHc5M3BqcFA5elFmN1lETFdZaEJkSUFBQUFBJCQAAAAAAAAAAAEAAAD2DidIuu693ExGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANbV6FzW1ehcSz',
    'Host': 'index.baidu.com',
    'Referer': 'https://index.baidu.com/baidu-index-mobile/index.html?',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'X-Requested-With': 'XMLHttpRequest',
}
response = requests.get(url, headers=headers)
time.sleep(1)
print(response.text)
res_dict = json.loads(response.text)
data = res_dict['data']
print(data)
uniqid = res_dict['uniqid']
uniqid_url = 'https://index.baidu.com/Interface/api/ptbk?uniqid={}'.format(uniqid)
response = requests.get(uniqid_url, headers=headers)
print(response.text)
key_data = json.loads(response.text)['data']
_all = data[0]['index'][0]['_all']
decrypt_data = decrypt_baidu_index_response(key_data, _all)
print(_all, decrypt_data)
'ZDW3BFux.t8iRl%58%.32,741+096-'
