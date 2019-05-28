import random
from env import *

def loads_data(response, key=''):
    if key:
        return json.loads(response.text)[key]
    else:
        return json.loads(response.text)

def get_headers(type='web'):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': random.choice(APP_USER_AGENT)
    }
    if type == 'web':
        headers['User-Agent'] = random.choice(BROWSER_USER_AGENT)
    return headers


def decrypt_baidu_index_response(keys, encrypt_data):
    """百度指数返回结果解密"""
    w_data = {}
    for index in range(len(keys)//2):
        w_data[keys[index]] = keys[len(keys)//2 + index]

    decrypt_data = ''
    for i in range(len(encrypt_data)):
        decrypt_data += w_data[encrypt_data[i]]
    return decrypt_data


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

"""function stringToHex(str) {
    var val = "";
    for (var i = 0; i < str.length; i++) {
        if (val == "") val = str.charCodeAt(i).toString(16);
        else val += str.charCodeAt(i).toString(16);
    }
    return val;
}
function YunSuoAutoJump() {
    var width = screen.width;
    var height = screen.height;
    var screendate = width + "," + height;
    var curlocation = window.location.href;
    if ( - 1 == curlocation.indexOf("security_verify_")) {
        document.cookie = "srcurl=" + stringToHex(window.location.href) + ";path=/;";
    }
    self.location = "/default.aspx?tabid=226&security_verify_data=" + stringToHex(screendate);
} < /script><script>setTimeout("YunSuoAutoJump()", 50);/"""

def str2token(str_data):
    token = ''
    for val in str_data:
        token += str(hex(ord(val)))
    return token.replace('0x', '')

def china_land(url):
    screen_data = "1333,800"
    cookie = ''
    if "security_verify_" not in url:
        cookie = 'srcurl=' + str2token(url) + ';path=/;'
    url = "http://www.landchina.com/default.aspx?tabid=226&security_verify_data=" + str2token(screen_data)
    return url, cookie

def stringToHex(s):
    val = ""
    for k in s:
        if (val == ""):
            val = str(hex(ord(k)))
        else:
            val += str(hex(ord(k)))
    return val.replace("0x", "")

def get_cookie(url):
    screendate = "1366,768" #  屏幕宽度和高度我们可以设置成固定值．
    curlocation = url  # 当前请求的url
    cookie = "srcurl=" + stringToHex(curlocation) + ";path=/;"
    cookie = {"srcurl": cookie}
    url = url + "&security_verify_data=" + stringToHex(screendate)
    return url, cookie

if __name__ == '__main__':
    # data = decrypt_baidu_index_response("rRP,Gi4XSkAvb1.42,108+95.6-37%", 'SRAXRPSb1bAPSbAAAPS1,irPSbAiGPSRbSAPS,A,APS,bbRPS,ArrPS,SrRPSSASSPSrRRSPSbRS1PSS,,XPSRiSRPSRR,GPSGbR,PSGGAbPSrRRbPSASbSPSSGiiPSS,,bPSrriSPSri1APSSrArPSSAGRPSbSirPSXRGRPSARriPS,bGS')
    # print(data)
    # print(get_sougou_weixin_detail_url('https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6EzDJysI4ql5MPrOUp16838dGRMI7NnPqqmqghgrZjZoAwla_S92HUwwvDqyjOWdzb_UcLpYkX0ABd5cGalMZ82hiRv6K94Zow4jG6WOtmaJceIcIwmExZxIIZrbOZGYWdida8Qgf2vh7OrhA4PNjrWMMdGfWP9xBOPhvugdGMUA52SESmjn9sm4OZCnxixtX&type=1&query=%E4%B8%8A%E6%B5%B7&k=68&h=d'))
    print(china_land('http://www.landchina.com/default.aspx?tabid=226'))
    print(get_cookie('http://www.landchina.com/default.aspx?tabid=226'))
