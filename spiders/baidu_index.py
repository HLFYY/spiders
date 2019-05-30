from decrypt_methed import *

# 日期格式：2019-02-24， area:默认全国（0）
data_url = 'http://index.baidu.com/api/SearchApi/index?area=0&word={keyword}&startDate={startdate}&endDate={enddate}'

def run(params):
    r_task = redis.Redis(**REDIS_SPIDER)
    val = r_task.get('baidu_BDUSS')
    url = data_url.format(**params)
    # BDUSS替换成自己登陆后的值
    headers = dict(dict(
        Cookie='BDUSS={}'.format(val.decode()),
        Host='index.baidu.com',
        Referer='http://index.baidu.com/v2/main/index.html',
    ))
    response = requests.get(url, headers=headers, proxies=get_proxy())
    if 'not login' in response.text:
        print('----未登录, response:{}'.format(response.text))
        return
    elif 'bad request' in response.text:
        print('----请示失败，可能关键词{}未被收录'.format(params.get('keyword')))
        return
    data = loads_data(response, key='data')

    # 获取解密的key
    time.sleep(1)
    uniqid = data['uniqid']
    uniqid_url = 'https://index.baidu.com/Interface/api/ptbk?uniqid={}'.format(uniqid)
    response = requests.get(uniqid_url, headers=headers, proxies=get_proxy())
    key_data = loads_data(response, 'data')

    # 解密数据
    userIndexes = data['userIndexes']
    for userIndexe in userIndexes:
        print(userIndexe)
        for key, val in userIndexe.items():
            if isinstance(val, dict):
                decrypt_data = decrypt_baidu_index_response(key_data, val['data'])
                userIndexe[key]['data'] = decrypt_data
        print(userIndexe)

if __name__ == '__main__':
    params = {
        'startdate': '20190424',
        'enddate': '20190524',
        'keyword': '华为',
    }
    run(params)

