import random


def decrypt_baidu_index_response(key_data, encrypt_data):
    """百度指数返回结果解密"""
    keys = []
    for key in key_data:
        keys.append(key)
    print(keys)
    w_data = {}
    for index in range(len(keys)//2):
        w_data[keys[index]] = keys[len(keys)//2 + index]
    print(w_data)
    encrypt_data_list = []
    for encrypt_d in encrypt_data:
        encrypt_data_list.append(encrypt_d)
    print(encrypt_data_list)
    data_list = []
    for i in range(len(encrypt_data_list)):
        data_list.append(w_data[encrypt_data_list[i]])
    return ''.join(data_list)


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

if __name__ == '__main__':
    # data = decrypt_baidu_index_response("rRP,Gi4XSkAvb1.42,108+95.6-37%", 'SRAXRPSb1bAPSbAAAPS1,irPSbAiGPSRbSAPS,A,APS,bbRPS,ArrPS,SrRPSSASSPSrRRSPSbRS1PSS,,XPSRiSRPSRR,GPSGbR,PSGGAbPSrRRbPSASbSPSSGiiPSS,,bPSrriSPSri1APSSrArPSSAGRPSbSirPSXRGRPSARriPS,bGS')
    # print(data)
    print(get_sougou_weixin_detail_url('https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6EzDJysI4ql5MPrOUp16838dGRMI7NnPqqmqghgrZjZoAwla_S92HUwwvDqyjOWdzb_UcLpYkX0ABd5cGalMZ82hiRv6K94Zow4jG6WOtmaJceIcIwmExZxIIZrbOZGYWdida8Qgf2vh7OrhA4PNjrWMMdGfWP9xBOPhvugdGMUA52SESmjn9sm4OZCnxixtX&type=1&query=%E4%B8%8A%E6%B5%B7&k=68&h=d'))

