from urllib import parse
import js2py
from .decrypt_methed import *
import js2py
from urllib.parse import quote
import execjs


def haoduo_app():
    with open('csdn.js') as f:
        js = f.read()
    import execjs
    now = time.time()
    context = execjs.compile(js)
    res = context.call("cmd5x", '/jp/dash?tvid=11878510309&bid=500&abid=100&src=02027221010000000000&ut=0&ori=h5&ps=0&messageId=1559650754970&pt=0&lid=&cf=&ct=&locale=zh_cn&k_tag=1&dfp=a038afc5a7d37744f493c2030b915b91eb7b2265f33215877881bd2887b108a886&k_ft1=17729624997888&k_uid=1559650754971&qd_v=1&qdy=a&qds=0&tm=1559650754971&callback=onSuccess')
    print(res)
    print(time.time() - now)


def remove_error():
    import os
    import re

    paths = ["/Users/houjie/Desktop/110_15287796ed5d3b544b025a580300a2be/res/layout/",
             "/Users/houjie/Desktop/110_15287796ed5d3b544b025a580300a2be/res/layout-v22/",
             "/Users/houjie/Desktop/110_15287796ed5d3b544b025a580300a2be/res/layout-v21/",
             # "/Users/houjie/Desktop/110_15287796ed5d3b544b025a580300a2be/res/layout-v26/",
             # "/Users/houjie/Desktop/110_15287796ed5d3b544b025a580300a2be/res/animator-v21/",
             "/Users/houjie/Desktop/110_15287796ed5d3b544b025a580300a2be/res/color/",
             "/Users/houjie/Desktop/110_15287796ed5d3b544b025a580300a2be/res/menu/",
             ]
    for path in paths:
        files = os.listdir(path)
        for tem in files:
            # if tem == "a1.xml":
            try:
                with open(path + tem, 'rb')as f:
                    content = f.read().decode()
                    # ress = re.findall(r'sina:.*?night=".*?"', content, flags=re.IGNORECASE)
                    # re.sub(b'sina:.*?Night=".*?"', b'', content, count=-1, flags=re.IGNORECASE)
                    # for res in ress:
                    #   content = content.replace(res, '')
                    ress = re.findall(r'app:.{0,32}=".*?"', content, flags=re.IGNORECASE)
                    for res in ress:
                        # print(res,tem)
                        content = content.replace(res, '')
                    ress = re.findall(r'fresco:.{0,29}=".*?"', content, flags=re.IGNORECASE)
                    for res in ress:
                        # print(res,tem)
                        content = content.replace(res, '')
                    ress = re.findall(r'android:keyboardNavigationCluster="true"', content, flags=re.IGNORECASE)
                    for res in ress:
                        # print(res,tem)
                        content = content.replace(res, '')
                    ress = re.findall(r'submit:.{0,20}=".*?"', content, flags=re.IGNORECASE)
                    for res in ress:
                        # print(res,tem)
                        content = content.replace(res, '')
                    ress = re.findall(r'video:.{0,20}=".*?"', content, flags=re.IGNORECASE)
                    for res in ress:
                        # print(res,tem)
                        content = content.replace(res, '')
                    ress = re.findall(r'sina[a-zA-Z.]*?:.*?=".*?"', content, flags=re.IGNORECASE)
                    for res in ress:
                        # print(res,tem)
                        content = content.replace(res, '')
                    ress = re.findall(r'style="\?attr/.{0,40}?"', content, flags=re.IGNORECASE)
                    for res in ress:
                        # print(res,tem)
                        content = content.replace(res, '')
                with open(path + tem, 'wb')as f:
                    f.write(content.encode())
            except:
                print(path + tem)

def wordsToBytes(str_data):
    i = 0
    t = []
    while i < len(str_data)*32:
        print(i >> 5)
        t.append(str_data[i >> 5] >> 24 - i % 32 & 255)
        i += 8
    return t


def bytesToWords(str_data):
    t, n, r = [0]*(len(str_data) // 4 if len(str_data) % 4 == 0 else len(str_data) // 4 + 1), 0, 0
    while n < len(str_data):
        # print(n, r >> 5, str_data[n] << 24 - r % 32)
        t[r >> 5] = t[r >> 5] | str_data[n] << 24 - r % 32
        n += 1
        r += 8
    return t

def stringtobyte(str_data):
    t = []
    for i in str_data:
        t.append(255 & ord(i))
    return t

def ff(e, t, n, r, o, i, a):
    s = e + (t & n | ~t & r) + (o >> 0) + a
    return (s << i | s >> 32 - i) + t

def gg(e, t, n, r, o, i, a):
    s = e + (t & r | n & ~r) + (o >> 0) + a
    return (s << i | s >> 32 - i) + t

def hh(e, t, n, r, o, i, a):
    s = e + (t ^ n ^ r) + (o >> 0) + a
    return (s << i | s >> 32 - i) + t

def ii(e, t, n, r, o, i, a):
    s = e + (n ^ (t | ~r)) + (o >> 0) + a
    return (s << i | s >> 32 - i) + t


def get_sign(str_data):
    e = stringtobyte(str_data)
    n = bytesToWords(e)
    u = 8 * len(e)
    c = 1732584193
    f = -271733879
    l = -1732584194
    d = 271733878
    for p in range(len(n)):
        n[p] = 16711935 & (n[p] << 8 | n[p] >> 24) | 4278255360 & (n[p] << 24 | n[p] >> 8)
    print(n)
    n[u >> 5] = n[u >> 5] | 128 << -u % 32
    dd = 14 + (u + 64 >> 9 << 4)
    n += [0]*(dd-len(n)+1)
    n[dd] = u
    print(len(n), n)
    p = 0
    while p < len(n):
        y = c
        w = f
        b = l
        xx = d
        c = c + y >> 0
        f = f + w >> 0
        l = l + b >> 0
        d = d + xx >> 0
        p += 16
    print(c, f, l ,d)

# or (var n = r.bytesToWords(e), u = 8 * e.length, c = 1732584193, f = -271733879, l = -1732584194, d = 271733878, p = 0; p < n.length; p++)
#                 n[p] = 16711935 & (n[p] << 8 | n[p] >>> 24) | 4278255360 & (n[p] << 24 | n[p] >>> 8);
#             n[u >>> 5] |= 128 << u % 32,
#             n[14 + (u + 64 >>> 9 << 4)] = u;
#             var h = s._ff
#               , v = s._gg
#               , m = s._hh
#               , g = s._ii;
#             for (p = 0; p < n.length; p += 16) {
#                 var y = c
#                   , w = f
#                   , b = l
#                   , _ = d;
# f = g(f = g(f = g(f = g(f = m(f = m(f = m(f = m(f = v(f = v(f = v(f = v(f = h(f = h(f = h(f = h(f, l = h(l, d = h(d, c = h(c, f, l, d, n[p + 0], 7, -680876936), f, l, n[p + 1], 12, -389564586), c, f, n[p + 2], 17, 606105819), d, c, n[p + 3], 22, -1044525330), l = h(l, d = h(d, c = h(c, f, l, d, n[p + 4], 7, -176418897), f, l, n[p + 5], 12, 1200080426), c, f, n[p + 6], 17, -1473231341), d, c, n[p + 7], 22, -45705983), l = h(l, d = h(d, c = h(c, f, l, d, n[p + 8], 7, 1770035416), f, l, n[p + 9], 12, -1958414417), c, f, n[p + 10], 17, -42063), d, c, n[p + 11], 22, -1990404162), l = h(l, d = h(d, c = h(c, f, l, d, n[p + 12], 7, 1804603682), f, l, n[p + 13], 12, -40341101), c, f, n[p + 14], 17, -1502002290), d, c, n[p + 15], 22, 1236535329), l = v(l, d = v(d, c = v(c, f, l, d, n[p + 1], 5, -165796510), f, l, n[p + 6], 9, -1069501632), c, f, n[p + 11], 14, 643717713), d, c, n[p + 0], 20, -373897302), l = v(l, d = v(d, c = v(c, f, l, d, n[p + 5], 5, -701558691), f, l, n[p + 10], 9, 38016083), c, f, n[p + 15], 14, -660478335), d, c, n[p + 4], 20, -405537848), l = v(l, d = v(d, c = v(c, f, l, d, n[p + 9], 5, 568446438), f, l, n[p + 14], 9, -1019803690), c, f, n[p + 3], 14, -187363961), d, c, n[p + 8], 20, 1163531501), l = v(l, d = v(d, c = v(c, f, l, d, n[p + 13], 5, -1444681467), f, l, n[p + 2], 9, -51403784), c, f, n[p + 7], 14, 1735328473), d, c, n[p + 12], 20, -1926607734), l = m(l, d = m(d, c = m(c, f, l, d, n[p + 5], 4, -378558), f, l, n[p + 8], 11, -2022574463), c, f, n[p + 11], 16, 1839030562), d, c, n[p + 14], 23, -35309556), l = m(l, d = m(d, c = m(c, f, l, d, n[p + 1], 4, -1530992060), f, l, n[p + 4], 11, 1272893353), c, f, n[p + 7], 16, -155497632), d, c, n[p + 10], 23, -1094730640), l = m(l, d = m(d, c = m(c, f, l, d, n[p + 13], 4, 681279174), f, l, n[p + 0], 11, -358537222), c, f, n[p + 3], 16, -722521979), d, c, n[p + 6], 23, 76029189), l = m(l, d = m(d, c = m(c, f, l, d, n[p + 9], 4, -640364487), f, l, n[p + 12], 11, -421815835), c, f, n[p + 15], 16, 530742520), d, c, n[p + 2], 23, -995338651), l = g(l, d = g(d, c = g(c, f, l, d, n[p + 0], 6, -198630844), f, l, n[p + 7], 10, 1126891415), c, f, n[p + 14], 15, -1416354905), d, c, n[p + 5], 21, -57434055), l = g(l, d = g(d, c = g(c, f, l, d, n[p + 12], 6, 1700485571), f, l, n[p + 3], 10, -1894986606), c, f, n[p + 10], 15, -1051523), d, c, n[p + 1], 21, -2054922799), l = g(l, d = g(d, c = g(c, f, l, d, n[p + 8], 6, 1873313359), f, l, n[p + 15], 10, -30611744), c, f, n[p + 6], 15, -1560198380), d, c, n[p + 13], 21, 1309151649), l = g(l, d = g(d, c = g(c, f, l, d, n[p + 4], 6, -145523070), f, l, n[p + 11], 10, -1120210379), c, f, n[p + 2], 15, 718787259), d, c, n[p + 9], 21, -343485551),
#                 c = c + y >>> 0,
#                 f = f + w >>> 0,
#                 l = l + b >>> 0,
#                 d = d + _ >>> 0
#             }
#             return r.endian([c, f, l, d])


if __name__ == '__main__':
    remove_error()
    # headers = {
    #     'User-Agent': "official.f1.3.3.1.3b0d4e4.20190723161254",
    #     "host": "readfree.zhulang.com",
    #     "common": "8QbovhpKVfI2KLGcILfqtUYvUrlEi1B7/5Dc7HcVHGuO/8Ww",
    #     "accept": "application/json",
    #     "channel": "f_oppo",
    #     "X-Version": "3b0d4e4",
    #     "version-code": "190717",
    #     "umd": '2e',
    #     "X-Token": "Opcyfss+uZm+xQpJRPiJHKWyptHh3K53jmUstXoONiqnB+Y+V8n7FqbWrohjNZ8tkGBmmRb5KyGMfzkzHlAXEmhvxnOJq7fp8z7eOM3fss+g09CERJscW8Y7hcH/TkWwAgapjzXlFrPEWTwH",
    #     "package": "com.wifi.reader.free",
    #     "X-Validate": "7221b587ca876508a2c031e50d0555ad"
    # }
    #
    #
    # def get_book_data(book_text):
    #     # book_text = "O0YNA1zq/PFQ+0Yl3ddmM82sJqIdrbthcMTe0GenXMEfqdXLzeZd2Sb+4tJzRW7LbE/ocvz66CrxpGNS"
    #     url = "http://test-liaowang-app.qttcs3.cn/netty/sendToAll"
    #     payload = "{\"param\": \" %s \",\"flag\": 1,\"TAG\": \"3\"}" % book_text
    #     headers = {
    #         'Content-Type': "application/json",
    #         'User-Agent': "PostmanRuntime/7.15.2",
    #         'Accept': "*/*",
    #         'Cache-Control': "no-cache",
    #         'Host': "test-liaowang-app.qttcs3.cn",
    #         'Accept-Encoding': "gzip, deflate",
    #         'Content-Length': "13071",
    #         'Connection': "keep-alive",
    #         'cache-control': "no-cache"
    #     }
    #
    #     response = requests.request("POST", url, data=payload, headers=headers)
    #     print(response.status_code)
    #     return response.text
    #
    #
    # list_url = "http://readfree.zhulang.com/v1/cate"
    #
    # url = "http://readfree.zhulang.com/v1/book?q=&offset=200&limit=100&cate1=6&cate2=-1&cate3=0&finish=-1&provider=-1&author=-1&word_count=-1&vip=-1&sort=&update=-1"
    #
    # req = requests.get(url, headers=headers)
    # print(req.text)  # 获取加密后的数据
    # text = get_book_data(req.text)  # 调用小刘接口解密数据
    # if text == "":
    #     pass
    # else:
    #     print(text)

