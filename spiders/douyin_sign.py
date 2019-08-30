import random
import hashlib
import time


def get_headers():
    user_agents = [
        'okhttp/3.8.1',
        'com.ss.android.ugc.aweme/570 (Linux; U; Android 5.1; zh_CN; OPPO R9m; Build/LMY47I; Cronet/58.0.2991.0)'
    ]
    headers = {
        'User-Agent': random.choice(user_agents)
    }
    return headers


def md5_str(data):
    object = hashlib.md5()
    object.update(data.encode('utf8'))
    sign = object.hexdigest()
    return sign


def shuffle(values, poss):
    rst = ''
    for index in poss:
        rst += values[int(index) - 1]
    return rst


def ppp(pMd5, key1, key2):
    rst = ["a", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0",
           "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "e", "1"]
    indexMax = 8
    index = 0
    while True:
        rst[2 * (index + 1)] = pMd5[index]
        rst[2 * index + 3] = key2[index]
        rst[2 * index + 18] = key1[index]
        rst[(2 * index) + 19] = pMd5[index + 24]
        index += 1
        if index == indexMax:
            break

    ascp1 = ''.join(rst).lower()
    as_str = ascp1[0:18]
    cp_str = ascp1[18:]
    return as_str, cp_str


def get_as_cp(timeStrap, urlParams):
    """
    :param timeStrap: int, 当前时间的时间戳(10位)
    :param urlParams: url中的value值(除了加密生成的as,cp),按照key的顺序(顺序，由小到大),拼接成的字符串(抖音app1.6.8以下版本,测试使用1.6.0版本)
    :return:
    """
    paramsMd5 = md5_str(urlParams)
    if timeStrap & 1 != 0:
        paramsMd5 = md5_str(paramsMd5)

    hexTime = hex(timeStrap).upper()[2:]
    aa = shuffle(hexTime, "57218436")  # aes解密出来的
    bb = shuffle(hexTime, "15387264")  # aes解密出来的
    as_str, cp_str = ppp(paramsMd5, aa, bb)
    return as_str, cp_str


def get_douyin_url(user_id=0, max_cursor='0', type='author_video'):
    """
    抖音通过device_id锁定设备,如用同一个device_id刷feed,0.5s休眠,多次请求后会返回“休息一下”的信息
    :param user_id: 用户id
    :param max_cursor:　用于翻页
    :param device_id:　刷feed流时,如果每次device_id都是随机，会导致数据重复，因此同一个device_id请求多次后再切换，在外部控制
    :param keyword:　　通过关键字搜索作者时，传入的参数，可以是作者名称或者作者的抖音id, 搜索接口需要登录才可以使用, 登录后cookie中的
    :param type:　判断是请求什么类型的接口, author_video-作者作品列表页，feed-feed流，author_info-作者信息，author_search-搜索作者接口
    :return:
    """
    ts = int(time.time())
    param_dict = {
        'device_platform': 'android',
        'ts': str(ts),  # feed流请求时， 同一个时间戳只能请求１０次,超过就没有数据
        'aid': '1128',
        'version_code': '160',
        'os_version': '8.0.0',
        'app_name': 'aweme',
        'device_type': random.choice(['OPPO+R9m', 'MI+6']),
        'channel': 'wandoujia',
    }
    if type == 'author_video':
        url_pre = 'https://api-hl.amemv.com/aweme/v1/aweme/post/?'
        param_dict = dict(dict(
            max_cursor=str(max_cursor),
            count='20',
            user_id=str(user_id),
            device_id=str(random.randint(10 ** 5, 10 ** 7)),
        ), **param_dict)
    elif type == 'author_info':
        url_pre = 'https://aweme-eagle-hl.snssdk.com/aweme/v1/user/?'
        param_dict = dict(dict(
            device_id=str(random.randint(10 ** 5, 10 ** 7)),
            user_id=str(user_id)
        ), **param_dict)

    else:
        raise ValueError('>>>>获取url失败，传入get_douyin_url方法的参数type有误，type:{}'.format(type))
    param_dict['rstr'] = 'efc84c17'  # java层写死的,app自身的,与设备无关
    param_str = ''
    ll = sorted(param_dict.items(), key=lambda item: item[0])
    url_middle = []
    for key, val in ll:
        param_str += val
        if key not in ['rstr']:
            url_middle.append('{}={}'.format(key, val))
    param_str = param_str.replace('+', 'a').replace(' ', 'a')
    as_str, cp_str = get_as_cp(ts, param_str)
    url_middle.append('as={}&cp={}'.format(as_str, cp_str))
    url = '{}{}'.format(url_pre, '&'.join(url_middle))
    return url