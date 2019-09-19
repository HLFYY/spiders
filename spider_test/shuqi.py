from base import *


def shuqi_category():
    for channel in ['male', 'female']:
        url = 'https://walden1.shuqireader.com/andapi/rankv2/class?_={}'.format(int(time.time()*1000))
        form_data = {
            'timestamp': str(int(time.time()*1000)),
            'category_key': channel,
            'sign': MD5(str(random.randint(1,100)))
        }
        time.sleep(1)
        response = requests.post(url, data=form_data, headers=get_headers(), verify=False)
        for data in get_data_list(response, 'data')[channel]['groupList']:
            category, short_name = data['relatedName'], data['showName']
            # print(data)
            for i in range(3):
                print('++'*10, short_name, i)
                if channel == 'male':
                    category = '其他小说' if category == '耽美小说' else category
                    books_url = 'https://read.xiaoshuo1-sm.com/novel/i.php?do=is_caterank&topClass=502&filterMigu=1&p=1&page={}&userId=1504639959&firstCate={}&sort=updateTime&_={}'.format(i+1, category, int(time.time()*1000))
                else:
                    books_url = 'https://read.xiaoshuo1-sm.com/novel/i.php?do=is_caterank&topClass=502&filterMigu=1&p=1&page={}&userId=1504639959&secondCate={}&sort=updateTime&_={}'.format(i+1, category, int(time.time()*1000))
                time.sleep(1)
                res_books = requests.get(books_url, headers=get_headers())
                for data in get_data_list(res_books, 'data'):
                    print(data)
                    detail_url = 'http://content.shuqireader.com/andapi/book/info/?_={}'.format(int(time.time()*1000))
                    detail_form = {
                        'bookId': data['bookid'],
                        'user_id': '1504639959',
                        'timestamp': str(int(time.time()*1000)),
                        'sign': '850eb5c203072ffd809f2727f72305ae',
                        'channel': '1077',
                        'version': '10.9.2.90',
                        'ver': '190904',
                        'linkMiguServer': '0'
                    }
                    res_detail = requests.post(detail_url, data=detail_form, headers=get_headers(), verify=False)
                    detail_data = get_data_list(res_detail, 'data')
                    print(detail_data)
                    # print(detail_data['bookName'], detail_data['lastChapter']['chapterName'])
                    tk = base64.b64encode((str(data['bookid']) + '417ac59e9f').encode()).decode()
                    cp_url = 'http://bookapi.shuqiapi.com/?bamp=sqbq&session=&userId=1504639959&bid={}&tk={}&sn=1568601841745589&imei=862021032478011&_={}'.format(data['bookid'], tk, int(time.time()*1000))
                    res_cp = requests.get(cp_url, headers=get_headers())
                    print(res_cp.text)


def shuqi_rank():
    for channel in ['男生', '女生']:
        url = 'https://read.xiaoshuo1-sm.com/novel/i.php?do=is_rank_home&p=1&userId=1504639959&appVer=10.9.2.90&interest={}&ver=190904&_=1568722453219'.format(channel)
        # url = 'https://read.xiaoshuo1-sm.com/novel/i.php?do=is_rank_home&p=1&userId=1504639959&appVer=10.9.2.90&interest=女生&ver=190904&_=1568722530743'
        res = requests.get(url, headers=get_headers())
        for data in get_data_list(res, 'data'):
            for i in range(3):
                rank_url = 'https://read.xiaoshuo1-sm.com/novel/i.php?channelId=&interest={}&p=1&size=10&page={}&rank=&status=0&type={}&userId=1504639959&do=is_rank_list&_=1568722695663'.format(channel, i+1, data['type'])
                res_rank = requests.get(rank_url, headers=get_headers())
                print("++"*10, channel, data['title'])
                for rank_data in get_data_list(res_rank, 'data'):
                    print(rank_data)
                    break
                time.sleep(1)


if __name__ == '__main__':
    # shuqi_category()
    # shuqi_rank()
    detail_url = 'http://content.shuqireader.com/andapi/book/info/?_={}'.format(int(time.time() * 1000))
    detail_form = {
        'bookId': '7740251',
        'user_id': '1604639959',
        'timestamp': '1568720120933',
        'sign': '187927ad37965c8149a7ac779b883ce9',
        'channel': '1177',
        'version': '20.9.2.90',
        'ver': '190904',
        'linkMiguServer': '0'
    }
    res_detail = requests.post(detail_url, data=detail_form, headers=get_headers(), verify=False)
    detail_data = get_data_list(res_detail, 'data')
    print(res_detail.text)
    # dd = {
    #     'bookId': '7740251',
    #     'user_id': '1504639959',
    #     'timestamp': '1568720120933',
    # }
    # xx = ''
    # for key, val in dd.items():
    #     xx += '{}{}'.format(key, val)
    # print(xx)
    # print(MD5('bookId=7740251&timestamp=1568720120933&user_id=1504639959'))
