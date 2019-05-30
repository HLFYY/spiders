from decrypt_methed import *

url = "http://www.landchina.com/default.aspx?tabid=226"
session = requests.session()
res = session.get(url)
print(res.headers)
verify_url, cookie = china_land(url)
print(verify_url, cookie)
res = session.get(verify_url)
print(res.headers)
header = {
    "Host": "www.landchina.com",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
    "Accept": "text/css,*/*;q=0.1",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate",
    "Referer": url,
    "Connection": "keep-alive",
    "Cookies": cookie,
}
response = session.get(url, headers=header)
print(response.request.headers)

