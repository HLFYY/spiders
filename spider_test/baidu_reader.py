from base import *


def baidu_category():
    url = 'http://appwk.baidu.com/nahome/class/getclass'
    data_json = 'fr=3&pid=1&screen=1920_1080&app_ver=6.0.5.1&optk=*&cid=2&bid=2&from=3_wandjread&opid=wk_na&ydsignature=c4b3b39b7ad0d46c8d51d35aeb208077&Bdi_bear=WIFI&cuid=8366EB6001486C1B925CE09EF6CDA885%7CO&app_ua=OPPOR9m&ua=bd_1080_1920_OPPOR9m_6.0.5.1_5.1&sys_ver=5.1&uid=abd_O_mo_44%3A04%3A44%3A2b%3Afd%3Aeb'
    # data_json = 'fr=3&pid=1&screen=1920_1080&app_ver=6.0.5.1&optk=*&cid=3&bid=2&from=3_wandjread&opid=wk_na&ydsignature=244633ff22ab96ebf8d6b6cfa2639a1d&Bdi_bear=WIFI&cuid=8366EB6001486C1B925CE09EF6CDA885%7CO&app_ua=OPPOR9m&ua=bd_1080_1920_OPPOR9m_6.0.5.1_5.1&sys_ver=5.1&uid=abd_O_mo_44%3A04%3A44%3A2b%3Afd%3Aeb'
    form_data = {param.split('=')[0]: param.split('=')[1] for param in data_json.split('&')}
    response = requests.post(url, headers=get_headers(), data=form_data, verify=False)
    for data in get_data_list(response, 'data')['class_info']:
        for i in range(3):
            print('++' * 10, data['cname'], i+1)
            books_url = 'http://appwk.baidu.com/nahome/class/getlist'
            books_json = 'fr=3&filter_cond=2&pid=1&screen=1920_1080&app_ver=6.0.5.1&optk=*&bid=2&from=3_wandjread&opid=wk_na&ydsignature={}&Bdi_bear=WIFI&cuid=8366EB6001486C1B925CE09EF6CDA885%7CO&app_ua=OPPOR9m&search_type=1&ua=bd_1080_1920_OPPOR9m_6.0.5.1_5.1&pn={}&sys_ver=5.1&uid=abd_O_mo_44%3A04%3A44%3A2b%3Afd%3Aeb&cid2={}'.format(MD5(str(random.randint(1, 100))), i, data['cid'])
            books_form = {param.split('=')[0]: param.split('=')[1] for param in books_json.split('&')}
            time.sleep(1)
            res_book = requests.post(books_url, headers=get_headers(), data=books_form, verify=False)
            for book_data in get_data_list(res_book, 'data')['list_info']:
                # print(book_data['title'])
                detail_url = 'https://appwk.baidu.com/naproxy/combinedbookdetail'
                detail_json = 'fr=3&screen=1920_1080&optk=*&Bdi_bear=WIFI&from_path=normal&doc_id={}&sys_ver=5.1&need_cmt=1&pid=1&app_ver=6.0.5.1&bid=7&from=3_wandjread&cart_id=477797205&opid=wk_na&ydsignature={}&need_relateresource=1&cuid=8366EB6001486C1B925CE09EF6CDA885%7CO&app_ua=OPPOR9m&ua=bd_1080_1920_OPPOR9m_6.0.5.1_5.1&need_catalog=1&uid=abd_O_mo_44%3A04%3A44%3A2b%3Afd%3Aeb&need_recnovel=1'.format(book_data['doc_id'], MD5(str(random.randint(1, 100))))
                detail_form = {param.split('=')[0]: param.split('=')[1] for param in detail_json.split('&')}
                time.sleep(1)
                res_detail = requests.post(detail_url, headers=get_headers(), data=detail_form, verify=False)
                detail_res = get_data_list(res_detail, 'data')
                print(detail_res['docInfo']['title'], detail_res['wangwenInfo']['update_info']['lastchaptername'])
                break


def baidu_rank():
    rank_list = [
        ('女生-人气榜', 3, 3),
        ('男生-人气榜', 3, 2),
        ('女生-热搜榜', 7, 3),
        ('男生-热搜榜', 7, 2),
    ]
    for rank_name, rank_id, channel_id in rank_list:
        for i in range(3):
            print('++' * 10, rank_name, i+1)
            rank_url = 'http://appwk.baidu.com/nahome/rank/ranklist'
            rank_json = 'fr=3&pid=1&screen=1920_1080&app_ver=6.0.5.1&optk=*&bid=2&from=3_wandjread&opid=wk_na&ydsignature={}&Bdi_bear=WIFI&cuid=8366EB6001486C1B925CE09EF6CDA885%7CO&app_ua=OPPOR9m&ua=bd_1080_1920_OPPOR9m_6.0.5.1_5.1&pn={}&sys_ver=5.1&uid=abd_O_mo_44%3A04%3A44%3A2b%3Afd%3Aeb&rank_id={}&category_id={}'.format(MD5(str(random.randint(1, 100))), i+1, rank_id, channel_id)
            rank_form = {param.split('=')[0]: param.split('=')[1] for param in rank_json.split('&')}
            time.sleep(1)
            res_book = requests.post(rank_url, headers=get_headers(), data=rank_form, verify=False)
            for book_data in get_data_list(res_book, 'data'):
                # print(book_data['title'])
                detail_url = 'https://appwk.baidu.com/naproxy/combinedbookdetail'
                detail_json = 'fr=3&screen=1920_1080&optk=*&Bdi_bear=WIFI&from_path=normal&doc_id={}&sys_ver=5.1&need_cmt=1&pid=1&app_ver=6.0.5.1&bid=7&from=3_wandjread&cart_id=477797205&opid=wk_na&ydsignature={}&need_relateresource=1&cuid=8366EB6001486C1B925CE09EF6CDA885%7CO&app_ua=OPPOR9m&ua=bd_1080_1920_OPPOR9m_6.0.5.1_5.1&need_catalog=1&uid=abd_O_mo_44%3A04%3A44%3A2b%3Afd%3Aeb&need_recnovel=1'.format(book_data['doc_id'], MD5(str(random.randint(1, 100))))
                detail_form = {param.split('=')[0]: param.split('=')[1] for param in detail_json.split('&')}
                time.sleep(1)
                res_detail = requests.post(detail_url, headers=get_headers(), data=detail_form, verify=False)
                detail_res = get_data_list(res_detail, 'data')
                print(detail_res['docInfo']['title'], detail_res['wangwenInfo']['update_info']['lastchaptername'])
                break


if __name__ == '__main__':
    # baidu_rank()
    baidu_category()