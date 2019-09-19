from urllib import parse
import js2py
from decrypt_methed import *
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

def jisuan(sell, num, buy, cost):
    money = (sell - buy) * num - cost
    money_per = money / (buy * num)
    return money, money_per


if __name__ == '__main__':
    # url = 'https://mi.gdt.qq.com/gdt_mview.fcg?actual_width=-1&fc=1&datatype=2&actual_height=-2&count=1&adposcount=1&r=0.03468060829692299&template_count=1&ext={"req":{"m1":"855cf0be4f83bd13761ad54ffc7c65f7","m2":"e326b0034ca4ef8cb72aea0fe2b6a8ee","m3":"cb081fa6c1d0d7fdb05396d0c2d4d81b","muidtype":1,"muid":"855cf0be4f83bd13761ad54ffc7c65f7","m9":"jpY655ysTSoO5EUOlVRzL2alW3TXj24daPuCTCfVHZWd4WbdBZrKuwx0y3MYawvTUIYfopGNchSj-Eb34ntFPAE9-j0lgiOTihPE5gmEoSX3S67xDCva9uTM49aNpK4n","placement_type":9,"render_type":3,"conn":1,"carrier":0,"loc_src":5,"support_app_landing_page":1,"c_os":"android","c_osver":"5.1","c_pkgname":"com.songheng.eastnews","c_device":"OPPO R9m","c_devicetype":1,"c_mf":"OPPO","c_ori":0,"c_w":1080,"c_h":1920,"sdkver":"4.63.950","tmpallpt":true,"postype":9,"deep_link_version":1,"c_sdfree":34946129920,"c_market":"7","c_hl":"zh","native_jsver":"1.1.0","scs":"0001dafba243","ast":{"br":"OPPO","de":"R9","fp":"OPPO\/R9m\/R9:5.1\/LMY47I\/1515760704:user\/release-keys","hw":"mt6755","pr":"R9m","sr":"G6BELRFI99999999","is_d":false},"support_video":true,"from_js":0,"sdk_st":"1","wx_api_ver":620954624,"opensdk_ver":620823552,"support_c2s":1,"v":{"ap":0,"rt":1}}}&posid=6020373662477875'
    # headers = {
    #     "User-Agent": "GDTADNetClient-[Dalvik/2.1.0 (Linux; U; Android 5.1; OPPO R9m Build/LMY47I)]",
    #     "Accept-Encoding": "gzip",
    #     "Host": "mi.gdt.qq.com",
    #     "Connection": "Keep-Alive",
    #     "Cookie": "snsuid=73052553150464; qz_gdt=5cqw6xiwaaajhfthl4nq; qz_gdtinner=5cqw6xiwaaajhfthl4nq; gdt_uid=0_1558109546",
    #     "Cookie2": "$Version=1",
    # }
    # response = requests.get(url, headers=headers)
    # print(response.text)
    dd = [
        (25.45, 700, 25.92, 23.18),
        (25.44, 600, 25.92, 17.71),
        (29.25, 400, 29.154, 13.34),
        (2.22, 8000, 2.35, 20.61),
        (7.95, 1800, 8.401, 16.21),
        (19.35, 1000, 18.503, 22.45),
        (11.5, 1600, 11.352, 21.35),
        (6.88, 2200, 6.611, 17.25),
    ]
    for d in dd:
        print(jisuan(*d))
