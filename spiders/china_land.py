import uuid

from decrypt_methed import *

def decode_image(src):
    """
    解码图片
    :param src: 图片编码
        eg:
            src="data:image/gif;base64,R0lGODlhMwAxAIAAAAAAAP///
                yH5BAAAAAAALAAAAAAzADEAAAK8jI+pBr0PowytzotTtbm/DTqQ6C3hGX
                ElcraA9jIr66ozVpM3nseUvYP1UEHF0FUUHkNJxhLZfEJNvol06tzwrgd
                LbXsFZYmSMPnHLB+zNJFbq15+SOf50+6rG7lKOjwV1ibGdhHYRVYVJ9Wn
                k2HWtLdIWMSH9lfyODZoZTb4xdnpxQSEF9oyOWIqp6gaI9pI1Qo7BijbF
                ZkoaAtEeiiLeKn72xM7vMZofJy8zJys2UxsCT3kO229LH1tXAAAOw=="

    :return: str 保存到本地的文件名
    """
    # 1、信息提取
    result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", src, re.DOTALL)
    if result:
        ext = result.groupdict().get("ext")
        data = result.groupdict().get("data")

    else:
        raise Exception("Do not parse!")

    # 2、base64解码
    img = base64.urlsafe_b64decode(data)
    print(img)
    # 3、二进制文件保存
    filename = "images/{}.{}".format(uuid.uuid4(), ext)
    with open(filename, "wb") as f:
        f.write(img)

    return filename

url = "http://www.landchina.com/default.aspx?tabid=226"
session = requests.session()
res = session.get(url)
print(res.headers, res.text)
html = etree.HTML(res.text)
image_url = html.xpath('//img[@class="verifyimg"]/@src')[0]
file = decode_image(image_url)
code = YDMHttp().run(file)
print(file, code)
verify_url, cookie = china_land(url, code)
print(verify_url, cookie)
res = session.get(verify_url)
print(res.headers)
header = {
    "Host": "www.landchina.com",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
    "Accept": "text/css,*/*;q=0.1",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "deflate",
    "Referer": url,
    "Connection": "keep-alive",
    "Cookies": cookie,
}
response = session.get(url, headers=header)
print(response.request.headers)
print(response.text)
#
