import re
import requests
from base_method import *
from urllib import parse
import pandas as pd
import base64
from lxml import etree
from urllib.parse import urljoin

def ss():
    sheet = pd.read_excel(io='米读书库违禁章节列表(连尚书目集)_20190726.xlsx')
    # workbook = xlrd.open_workbook(file_path)
    dicts = dict()
    for tem in sheet.values:
        title = tem[0]
        chapter = tem[2]
        key = '""' + title + '""'
        chapter_id = re.findall(r'\d+', chapter, re.S)
        if chapter_id:
            chapter_id = int(chapter_id[0])
            if key in dicts:
                dicts[key].append(chapter_id)
            else:
                dicts[key] = [chapter_id]
    print(dicts)
    for key, val in dicts.items():
        print({key: val})





if __name__ == '__main__':
    # url = 'https://live.kuaishou.com/profile/linggege'
    # url = 'http://www.gifshow.com/fw/photo/5221079360107510936?cc=share_copylink&#38;fid=1449438575&#38;shareId=50677510281&#38;docId=167&#38;shareType=3&#38;groupName=E_3_180925155713222_G_1&#38;shareToken=XaoTh8ZTFDGU_-z5vZVPiiG01mh&#38;appType=21'
    # response = requests.get(url, headers=get_headers())
    # print(response.url)
    # data_json = re.findall(r'__APOLLO_STATE__=(\{.+?\});', response.text, re.S)[0]
    # print(data_json)


    # url = 'https://haokan.baidu.com/v?vid=12362707288810595703&pd=haokan_share&context=%7B%22cuid%22:%22Ya2va_ufvulvaSahg8-3aYaL2a0_iH8sgi2ga0Pq-i86a28Jga-Q8_uY2ijEP2fHA%22,%22tt%22:1564208447,%22uk%22:%22XN-3xdZFkj0cxblHiuCtIA%22%7D'
    # response = requests.get(url, headers=get_headers())
    # if 'jd6brxns2pk6isyw' in response.text:
    #     print(response.url)

    # url = 'http://www.meipai.com/media/782665249?uid=1694687989&client_id=1089857302&utm_media_id=782665249&utm_source=meipai_share&utm_term=meipai_android&utm_content=test&viewCount=1&shareCount=1&gid=811757107'
    # response = requests.get(url, headers=get_headers(), verify=False)
    # html = etree.HTML(response.text)
    # down_url = html.xpath('//meta[@property="og:video:url"]/@content')
    # name = html.xpath('//h3[@class="detail-name pa"]//text()')
    # print(decrypt_download_url(down_url[0]), name)

    # url = 'https://n.miaopai.com/api/aj_media/info.json?smid=bpynLZqWiLdWLMIcCBVOB8FwsQd5CtiZ&appid=530&_cb=_jsonpjc11111'
    # headers = {
    #     'Host': 'n.miaopai.com',
    #     'Connection': 'keep-alive',
    #     'Sec-Fetch-Mode': 'no-cors',
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    #     'Accept': '*/*',
    #     'Sec-Fetch-Site': 'same-site',
    #     'Referer': 'http://n.miaopai.com/media/bpynLZqWiLdWLMIcCBVOB8FwsQd5CtiZ.htm',
    #     'Accept-Encoding': 'deflate, br'
    # }
    # response = requests.get(url, headers=headers, verify=False)
    # print(response.encoding)
    # print(response.status_code, response.text)

    # url = 'http://v.douyin.com/2DKX2r'
    # response = requests.get(url, headers=get_headers())
    # print(response.text)

    # url = 'https://bobo1.vbbobo.com/channel/share?scid=2017070404252887&bobouid=250557604&shareuid=&mediaType=1'
    # response = requests.get(url, headers=get_headers())
    # print(response.text)

    # url = 'http://www.yidianzixun.com/article/V_026MFRfR'
    # response = requests.get(url, headers=get_headers())
    # print(response.text)

    url = 'https://reflow.huoshan.com/share/load_videos/?offset=0&count=21&user_id=84319803893'
    url = 'https://reflow.huoshan.com/hotsoon/s/P6swlBdw700/'
    url = 'https://like.video/live/share/profile?c=cp&b=79811906&l=zh-Hant&t=1'
    url = 'https://like.video/bg_ci_index.php/live/share/getUserPost?u=1335115789&count=30'
    url = 'https://id.tudou.com/i/UMjkxNzMxMjY4OA==/videos'
    url = 'http://space.bilibili.com/ajax/member/getSubmitVideos?mid=194156269&pagesize=30&tid=0&page=1&keyword=&order=pubdate'
    url = 'https://www.youtube.com/user/GraphStudio1/videos'
    url = 'https://www.instagram.com/p/BwOMCHqFkmM/?utm_source=ig_share_sheet&igshid=1symy8a4qskvc'
    url = 'http://vm.tiktok.com/d1vVWK/'
    url = 'https://www.instagram.com/graphql/query/?query_hash=f2405b236d85e8296cf30347c9f08c2a&variables=%7B%22id%22%3A%227082389313%22%2C%22first%22%3A12%2C%22after%22%3A%22QVFCellrY1JyQ295MkVSTFdrcXlFLUp0ZkdsWkVBZ3ZRX3g3dE5XM256WjdJZVoxLWttRmYxY0FfNXlTbHd2Z2MzakxYdmVJbHkzSUlMLW5fbmVKbTZyZQ%3D%3D%22%7D'



    url = 'https://cache.video.iqiyi.com/jp/dash?tvid=1528582900&bid=500&abid=100&src=02027221010000000000&ut=0&ori=h5&ps=0&messageId=1566027093431&pt=0&lid=&cf=&ct=&locale=zh_cn&k_tag=1&dfp=a0e4e743ca232341d4a3b09ef4eeaad3ad6c7e04f72181234ab0e2a3d221891387&k_ft1=17729624997888&k_uid=1566027093433&qd_v=2&tm=1566027093432&qdy=a&qds=0&vf=3ee1aff661c3ed3acac2d8a231b1d9c4&callback=onSuccess'
    num = 1
    r = redis.Redis(**REDIS_SPIDER)
    # while True:
            # url = 'https://ups.youku.com/ups/get.json?vid=37848326&ccode=050F&client_ip=192.168.1.2&utid=t3tpFWgVYl0CAXTkk24zYLrD&client_ts=1566447529&ckey=119%23Ml8AvYM1MKjvCMMzrywxLkVL6kFjcvGqo%2B%2BXsv0TKOAsiA%2Bg%2BfMK0FCKFeqy4q14k7SnOYwZT4Oljt8GLeAzRBSedFNL6m%2BS4lkGdoHg65kVKUOC9HilSSkfprCMqUCl4YFzFxktgCv1Et8LfHAzLS0HGEF7OYahwGJMIsmbus7scrAi%2BUjKwfxygtW%2FgGhuWis9abqDbpUIJnTwHai1XGTjBE7GxDsumYZo%2BmXW8d8cwDqbeLQda1MhdyX9RZEVM7BwwP%2BDfKfpV60MxB6nqWe%2BF0kAIok4XZk82EGSlpMtKBupbXC5dV1bvxKKK9xarXDYQthqlh85BkKh%2FFOiS4kC7Njz8R0PPYnnF8IiHuKUTS4LnT1K6i7Pqrz6BY9Aiqp7Ob7ZzEeLiBBE8Ou4qw%2FSNLmjz0JJ4xetTox9tU7htBJ%2FzYAcJCcH4CF07pGTi%2FpbChfBBrSOPLAi%2BC2r%2F6G7V4gMvcta1WGw2tUjxYt7%2B2tgH2JT%2BAY1hdFs4hoCt6djpZ1%2BhzRsxRKshOeprjePp46cMzVkxQdcnjAs9llfT1RYSJg8UeaKhISs%2BgSN7nzqzPbgDrM1PxP0zSKbmJOje1dPBO79JUsOtFrN9WPSxO7RrH0UsORAikSoblQMuGTL3lJGjC%3D%3D&site=-1&wintype=interior&p=1&fu=0&vs=1.0&rst=mp4&dq=flv&os=mac&osv=&d=0&bt=pc&aw=w&needbf=1'

            # url = 'https://ups.youku.com/ups/get.json?vid=XNDMxNjc0OTg4MA==&ccode=0505&client_ip=0.0.0.0&client_ts=1566528089&utid=t3tpFWgVYl0CAXTkk24zYLrD&ckey=119%23MlKEZav4MQjXMMMz2MiriuVLT7a5X6uyyx79cfvFOnp8GnndOLZNuqA7n%2B8fOyRc3FNF9UWS4Q9L3dFsUESVNNFG9oAzRr6oQwr89DmLLu%2F8zPfFQssVNrerlBV7zSsU3CI8zUNg4QkLXQULzRwW8smr3V7scrAjn2NJAWI4T%2FY7ZglajU07WV2VG8ms4UTrvri1XGTjBE7GxDsumYZo%2BmXW8d8cwDqbeLQda1MhdyX9RZEVM7BwwPVPbakVR9OfZS6v3ZrjWPaAL6%2BlSPXhRz2fRN%2BJ8Qbr95EepfdcG8lHz8HFrpFR1yZq0uXYKdz078fu0aJKAzkJi6yicgN1lcQYQ7xxPBwt%2FnNYW97tydqn61PUz%2Bxd%2FMyJx7414Z6phCYXqVJAhTCuBezm1Qdf%2BkFCoDNu7DI6uIN4JSJ1vkDjqduvRrggdmKOANZwvcZ0x3EnZXalXAScNBcjL0SDxBfzPLXxKZjPzjIMgAjMMRTZufwRVrJIMeBcKtbBPJJvs9P%2FSPzY%2BO%3D%3D&callback=json65280892720617929'
            # url = 'https://ups.youku.com/ups/get.json?vid=1080272219&ccode=050F&client_ip=192.168.1.1&utid=t3tpFWgVYl0CAXTkk24zYLrD&client_ts=1566528189&ckey=119%23MlKvqut7MJ%2FNDMMz0yxvLhVLXply10Xs0pDbmxZMHsHNOguICU0vizofW%2FT2A6niWtvHOCNp3FNF9UWS4Q9L3oAsRJBONt8LfCqz0SfnqEA8a22hBHMMgMMZR%2BBV9AAYfCDSzRsedF8t9dvFBNTLkc0A8Nj8NCyTg4HQM6ILfXW2WUp0BAkAHoDyuT0Q%2FvxNzKuARM0JvjgWaowfKi%2F4eu8hJlE5JGnXRn0FjAhlJJLY38iaCstisaNzxezswQlqBTXjD1wSccgVBYc6ZHXygvwpWgG3llQw9I3rdYb0%2FIB3WV8%2Bk8DOxPokC%2FI5ml1zixd7H%2F%2FbKQvH3xxLFdwdXfOkxeJCUo4Xz6Yc7sU4ZKBjc8dA7cuiVLLrgjugU7T%2F%2B4KdhR%2BLztRKGIFcKbWaM5rg0cTW%2FcQ8Y9iFA%2B3YFmXJqDK2fxkWi%2FprxOczun7mw8kgeLwKGRE%2BDHGExZpBZ%2FvZGexFs7GxeAmaHziVBI71MVd18pA96KIbvZfSryHsXlzaWX2o4X2PiYizm9ADfdzutxb2bu8v7y%3D%3D&site=-1&wintype=interior&p=1&fu=0&vs=1.0&rst=mp4&dq=flv&os=mac&osv=&d=0&bt=pc&aw=w&needbf=1&callback=youkuPlayer_call_1566528189560&_t=047273382518595963'
            # url = 'https://ups.youku.com/ups/get.json?vid=XOTEwMzA0OTU2&ccode=0505&client_ip=0.0.0.0&client_ts=1566527861&utid=BauXFLJoiBICAWVfZVqBdZeU&ckey=119%23Ml8V8utRM6PNCMMzrMUyjgNWabZKJPomSEMvX79zrPclypd0Iu%2FfcV97oqb8PM9PkG81iLBlIrdGFHA8R2BVNNFGL30Y6Sse3AAL9U%2BS4qFLTqgGRm6WFLH7LFNqlSYk3oX8hmV84pdGwaALR2BWNrc2dGYz4la%2BjewCGUzXIu4QM6ILfXWqlkraTskoYF1IPf3og2Aq1QXbMPmHnXNffqjD3HNH%2Bf%2FD7dFX15EN9L7i3M6MLKa%2BxAQcOaBbsN2%2BBz7gmd%2BDzg1NxrLPaU2T7PIZuTpOkwdR%2B0%2FsxbAcJOg7bfRyW%2Fiylr7J8GQokk99N0ejrtuk1QhHFFvep49t2Ymf9d%2BB4XQskY7STXKQtnYjqwGlhvRYajnqO6%2FdNETkKtRUTekQCfZGyhWUMKXLsmNTWSDVLiRBI76%2BYOfGDVNtWKpCPDCc6ZFGj7SyhJB%2BGDB39H3%2F7p%2BXtUawYKrcbz38AkscbGHZsTUBiz5wtVbg3Ults2qTVEpt4561x7XY6LijQP8uBM75EM%2B4qxlg3ZrebHAYFZVceMvo8c4xyQTxgMzFKO%3D%3D&callback=json65278617600938035'
            # url = 'https://ups.youku.com/ups/get.json?vid=XNDMxNjc0OTg4MA==&ccode=0505&client_ip=0.0.0.0&client_ts=1566542789&utid=T4tqFQhs%2FXQCATtsR2ZiaOPC&ckey=119%23Ml7P2FLeMJPKqMMz0O%2FILuNW4WST1o1kuw6f%2B%2FC3xAb8%2FcifnrqwOHeyqtAONfmd%2FmjIsvbGFoA8R2BVNNFGLe0h4Sse3AAL9U%2BS4qF1O0NMR2VVNEFLqwsWBc6L9yk7f%2F0%2B4lkGM0HhRUttN2es85HWlS0HqyKFSyqOfoD90RcvhIJwys7Fx5qerVVpMrmyyC0VUZbOaowfKi%2F4eu8hJlE5JGnXRnb2Vy2AGsoyopQtNrm4%2FnXX%2FfskGi6sqKV7tFhu02LCil02HmFEbe9ENX98bx8QQc%2BdnXmGKB3wVhqzCEMfg4C0poZWaVc3VbZGcnfEyiNiVfxIWe0coqZexF26hICgyzkO8wE7HcPdC3%2FqthPI2lRFPU%2BGNF0rzrmGm%2FRsCLLP5xsdH%2BPP%2B3uSllh8hG2gEkSrRCzvTpsbnDfI93zWXESeEdZ34AEhXmj01uW58LYxKzgIUK7HmsX6TvFELNOpGvH5IQKnNJhv2JRjdMz8fGpOMUjhBaSMcPnJ1lqfQml8jtk9BD1mnYnS95eKLTO%2F&callback=json65427896610129679'
            # url = 'https://ups.youku.com/ups/get.json?vid=XNDMxNjc0OTg4MA==&ccode=0505&client_ip=0.0.0.0&client_ts=1566542777&utid=Ncx3FUYSXUMCATtsR2Ym3pOq&ckey=119%23Ml8AT71oM6VTXMMz0yuHLkVLXpjx4a%2BnG4ilQdWTxj6q0nIBnBCISGqyf0zR%2FZzZW7qsVyRA3FNF9UWS4Q9L3dARQP%2FONt8LfeAScLSuoDsnz2WzulsZrSmOtgh0NaFLleH7lmBeftAL9U%2Bq44MMIlY84liFy6wJu3HTIUcQM6ILfX7YggRUnGKkvb0kKTVA1wRC5Qg65M0TgjG8aowfKi%2F4eu8hJlE5JGnXRn0FjAhlJJLY38iaCstisaNzxezswQlqBTXjD1wSccgVBYc6Edk0veV4AZC4hSfBbUbmg5fIf9ntcwvisjuMSg0SeMtsov6%2FlR900ZmiEd8WVqgFO4ku79JKyUN2Uxkbyjdqj4QRjslc%2BiRgP44G3qbuwsgknOYHpv8kq%2Bi0EQ5ijrsPDnYJInI8LOXHEIX%2B8bFC0RMiUTvZRx1zNIW6v7GspJ34hDvtGJQ5RbpSc%2FHYFxWH1sFRKRkpdQS6Y74pEyQMs7KtIRF5GrkXZ60eGPNdI6fqgDkcA8Uyo5dpzg4CclE3RzRAYodJpm5uZ0TxIvKKRY1%3D&callback=json65427771800578538'
            # url = r.rpoplpush('tudou_detail_url', 'tudou_detail_url').decode('utf-8').format('XNDMxNjc0OTg4MA==')
            # headers = {
            #     'Referer': 'https://compaign.tudou.com/v/XNDMxNjc0OTg4MA==',
        # 'Sec-Fetch-Mode': 'no-cors',
        # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        #     }
            # response = requests.get(url, headers=headers, verify=False)
            # # print(response.text)
            # if '户端无权播' in response.text:
            #     print(url)
            # num += 1
            # # print('-'*10, num)
            # time.sleep(2)

    # url = 'http://icanhazip.com/'
    # local_ip = requests.get(url).text
    # time_now = int(time.time())
    # license = 'test12404'
    # secret = 'e76094b51c'
    # sign = MD5('{}{}{}'.format(license, time_now, secret))
    # url_proxy = 'http://47.244.246.48/obtain?license={}&time={}&sign={}&cnt=1'.format(license, time_now, sign)
    # url_white = 'http://47.244.246.48/whitelist/list?license={}&time={}&sign={}'.format(license, time_now, sign)
    # url_add_white = 'http://47.244.246.48/whitelist/add?license={}&time={}&sign={}&ip={}'.format(license, time_now, sign, local_ip)
    # # print(url_add_white, url_proxy, url_white)
    # response = requests.get(url_proxy)
    # print(response.status_code, response.text)
    # proxy_list = json.loads(response.text)['proxies']
    # ip_port = random.choice(proxy_list)
    # proxy = {
    #     'http': 'http://{}'.format(ip_port),
    #     'https': 'https://{}'.format(ip_port),
    # }
    # print(proxy)
    # url = 'http://vm.tiktok.com/d1vVWK/'
    # response = requests.get(url, headers=get_headers(), proxies=proxy)
    # print(response.text)
    # # url = 'http://icanhazip.com/'
    # local_ip = requests.get(url, proxies=proxy).text
    # print(local_ip)

    # url = 'https://share.rightpaddle.com/api/h5/get_video_info/'
    # url = 'http://share.ippzone.com/ppapi/post/detail'
    # headers = {
    #     # 'accept': 'application/json',
    #     # 'accept-encoding': 'gzip, deflate, br',
    #     # 'accept-language': 'zh-CN,zh;q=0.9',
    #     # 'content-length': '29',
    #     # 'content-type': 'application/json',
    #     # 'cookie': 'UM_distinctid=16c89a04115940-0189aeb6d6e71c-38607701-13c680-16c89a04116a26; CNZZDATA1277106093=92713123-1565674219-%7C1565864299',
    #     # 'origin': 'https://share.rightpaddle.com',
    #     # 'referer': 'https://share.rightpaddle.com/share_storebrand/?vid=2576007023732723969&vname=langua&vapp=3804&abid=223_ad_tt_3762_0_test_FILTER,167_live_show_3694_default_FILTER,253_recom_fresh_layer_similar_default&pcid=huawei&cid=2576007023732723969&impressionid=78D5DF1C-2507-43BE-AAF0-86B2226A06CF&nickname=&uid=&udid=0dd3d21f-02a6-3da0-8624-efe81bb82b32&user_icon=https%3A%2F%2Ficdn.rightpaddle.net%2Fuser_icon%2Fanonymous%2Fdefault_avatar_unlogined_new.png&ab=default&brand=v82',
    #     # 'sec-fetch-mode': 'cors',
    #     # 'sec-fetch-site': 'same-origin',
    #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    # }
    # form_data = {"vid":"2579753222151344450"}
    # form_data = {"pid":87170997}
    # response = requests.post(url, data=json.dumps(form_data), headers=headers)
    # print(response.text)
    print('---')
    url = "http://mobads.baidu.com/cpro/ui/mads.php"

    querystring = {
        "code2": "myPY5R4KQDkfQD7fHzkDHausp1dWUvY8Tvq8uv9-UhT8uy71IA4-ILnhmgfqnBuM5iuk5ymknvfkmvmYgvPsTBuWTLPGujdBnjGBrjCvP1Cvn1Cvn1CkngkiHMIiRR4FwLICmhchIZFhIZ0qTvwog168P10vPiuv5y78uZFEpywhuyNbg168rjDsr7tYQWD8n10hpyYqFhkL5HcknzuduA-b5iuhugfqfR4RiikPRdPfQ7uFwDN5QD4PHY3_i7wPHakjHD-ji1FyiRw7Hzu9UhwzUv-bgv-b5ymzuhc4mhD1nhuBn1DvP1nhUA6qnHmsFMP8uMFEUHYsniuVmynqrAnlnvDluHnlPhflPvmlPHRhmgKspyfquWD1uj7WuWfhmgKGUhuE5yV2Qyu3TadgXj9ZRv33fdP_mYqHIYCVNM6dy7KLmYwaXDdcwg91myPVTY9DUWNmiAkWgYFLHR97IvPRiZ9sTbFLPidyXjNmRZIWwDF3HR97Xj9gmgIWivu_mvNyXW9cfgIWNDF3HyucUgPcfv3dyD9_mdqaIYdcwgIWND93iMFaIL0VNM6dy7KLmYwjUAPnHL91uy7LmYIhUAP-NMC3iD7LT79jXMPBwhd1iDF8PN9cUAPxfMIPiduLT1IZXZKzfMIpQNu3PN9fIvPDfvkWHDq3TdP9IvPZuhV1yDq_T7KcILPDwvk1NdPVTY9fu19BfLIWiDqLHHIKXDdDfL91PdF_ih-9n--HyydpfvuoTAdwn-GQNv9FHdGoUYP7nAPRfLC3yDNlTvujILPmRZC3mb73IhN-Fh6qPj6sFhP15iuL5HmYnau8UL0qFhFzujdKUhwzUv-bFh-9ujYkP1DLrH6vrHD3Piu1I1Yknj6sFMPbm1YVnHbzrisdPWR_QHD4nWb_PHmdFhq1IWYdQWD8niu85HDhIA7B5H0hTLIG5HDhmhwz5HczFh7sIjYsFMKxIhNz5H68P10vPiuzug7xpyfqn1RznHnYuhDkPvnYPynLuH0YmynLmhR4PW6LnjNbuhRhpyd-pHY1PH6zn1bsPHRzrj6kP1DhTvN15HDdPWm4P1bLn1T1rjbhUMfqUMN_U7tsFMPC5HD4nW0hIvbqmWKBrjmLPWnvn1Dkg1mYxAcsmW6vP1m1PWnsnNtvPZkBnAc3PWTvn1m1njFxPWNtmWKBrjmLPWnvn10sg1mdxAcsmW6vP1m1PWnsndtvPiusThqb5yu-uyfhmg0qnauWpyfqFMP85Hndrjc1rH0dPHc3rjDLniu8ugfqnH0sFhq15y78uZFEpyfhmgKGujYvPjfvnW03FhPdpyfqfYPKPjfsPH9AnRF7rjbLPYNDrjDkPjnYnRFAfRRzfHItHzuYTjdKHdPfcAq8cD99Uyd-Tb9-myfhuAN85Hn8nauWpA-b5y4dUAshmWDdPWm4P1bLn1Tvnjcqnifb",
        "b1566979737602": "1"}

    payload = ""
    headers = {
        'cache-control': "no-cache",
        'Postman-Token': "294743b6-c25a-4103-9aca-fce44ba704a5"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    print(response.content.decode('utf-8'))
