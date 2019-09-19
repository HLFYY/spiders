from base import *


def dejian_category():
    # url = 'https://dj.palmestore.com/zybk/api/categoryNew/category?timestamp=1568632944685&usr=i2184309278&sign=A6lBcKsbj%2Bq2K9OSa%2BXyh52lUGcn%2FkrzT0WlESUTsA4i1543G8%2BwTyhDprR0JGHeN7IJmbvXtzIa3luaFBIfRuPqai0G2Chhgvn1OkcJXuWLZ3b8mN5e8F0iqY4pzV51Tazwq5UxZ95%2FeK9DMEDpGYUr2QGRLLWVLiP7qJGj1CY%3D&pluginVersion=79&a0=null&pk=MF0001&today=0&zyeid=8882fb29765446dba3ff677e0b41e3a1&usr=i2184309278&rgt=7&p1=VoVRBOjCfgEDAFntLM%2Fye7BT&pc=10&p2=124009&p3=17101856&p4=501656&p5=19&p6=&p7=__624047014896077&p9=2&p12=&p16=OPPO+R9m&p21=3&p22=5.1&p25=17101856&p26=22'
    # response = requests.get(url, headers=get_headers(), verify=False)
    # print(response.text)
    # for data in get_data_list(response, 'body')['categoryList']:
    #     if data['name'] in ['男频', '女频']:
    #         for group_data in data['groups'][0]['items']:
    #             print(group_data['id'], group_data['name'])
    #             books_url = 'https://dj.palmestore.com/zybk/api/categoryNew/index?timestamp=1568634222060&usr=i2184309278&categoryId=804&sign=jB3ywXEltq%2Fba3z12qSraYQYenTMptApidSdzq13N6KAosvVBJK46kgB0e43eOeMp%2BA2i%2BGKhJcRZ%2BElE7HuttXv0Oj%2FwgVv8i5Fpz%2BYsrIBD3bUvEOa2%2BKjFSASE0i9vhG3Xyh8chhjD8L0pIyC3RuJO%2BZvJVModWPiT9CBYUs%3D&page=1&pageSize=15&hasFilterInfo=1&categoryType=women&resourcesId=6&pluginVersion=79&a0=null&pk=null&today=0&zyeid=8882fb29765446dba3ff677e0b41e3a1&usr=i2184309278&rgt=7&p1=VoVRBOjCfgEDAFntLM%2Fye7BT&pc=10&p2=124009&p3=17101856&p4=501656&p5=19&p6=&p7=__624047014896077&p9=2&p12=&p16=OPPO+R9m&p21=3&p22=5.1&p25=17101856&p26=22'
    sign_list = [
        ('都市', 1568701822479, 745, 'man',
         'tjG+XEH48ZV/vKwzAmqaqx+0iP6fSdO/C8p4nmNKQDcE952wucNnPKEtyclfOSLXlsNsNR4YDPHH5/qqe7FVSyltSu14Usly1X3qnFiAPSFjCVrQKaod/klitrxceYaNB4P2aMYVM66Q+gga18lDwuJSQ7SCY4FEoF+AQp2CU7c='),
        ('游戏', 1568701975807, 752, 'man',
         'MbvY08N6/lebrSFgSsP7WglIqslN6SbacSPdVDP268cpAT6kruEqhK05qWQWjjuELd3gdFQgKaTipWucfqQcBOzS+0MMRwkS3u2m6nnxrkn/0BmIsUA3bregYXnMn0dJkgO71DYMU8dOdF/CkBfOYwLFhsHRzlLMa1ig+RcP4QE='),
        ('玄幻', 1568702231726, 744, 'man', 'Av5n8nKYS2jSG9imIvKQwPpNRiHXWU4+HmPb4d3XwwwBwb4JHpZiljmue16zlwpxkSTKGg2JYh9RTIA58eLTBxIMEAMTKejkTnR+PFUBnPBFb7h6Hxxn+qDBwzJZzpaDqIOmKNAiNZc9D3/7xzbBbdHr8AJAhY0tfmnSvTIKxjQ='),
        ('仙侠', 1568702285326, 747, 'man', 'QfT7V0h4J0mQsOL98dbDxskiJpKL8LBybhMJj8oRoNeK88ZmMM9oBQl3aHyXScKVyfffLLmrh261Pzzsz/+D9ioPR5/VvnPDxeLD7akeGDPpKtw0bWey2f5nAKu+7/ckIFOmK+uQHkarPu+ctepdJx+UO0I1Q73pTYu/Ny8rw5s=')
    ]
    for category, timestamp, categoryId, channel, sign in sign_list:
        for i in range(3):
            books_url = 'https://dj.palmestore.com/zybk/api/categoryNew/index?timestamp={}&usr=i2184309278&categoryId={}&sign={}&page={}&pageSize=15&hasFilterInfo=1&categoryType={}&resourcesId=6&pluginVersion=79&a0=null&pk=null&today=0&zyeid=8882fb29765446dba3ff677e0b41e3a1&usr=i2184309278&rgt=7&p1=VoVRBOjCfgEDAFntLM%2Fye7BT&pc=10&p2=124009&p3=17101856&p4=501656&p5=19&p6=&p7=__624047014896077&p9=2&p12=&p16=OPPO+R9m&p21=3&p22=5.1&p25=17101856&p26=22'.format(timestamp, categoryId, sign, i+1, channel)
            res_books = requests.get(books_url, headers=get_headers(), verify=False)
            # print(json.loads(res_books.text))
            print('=='*10, category, i+1)
            for data in get_data_list(res_books, 'body')['sectionModule']['section']['books']:
                # print(data['name'])
                time.sleep(1)
                detail_url = 'https://dj.palmestore.com/zybk/api/detail/index?bid={}&pluginVersion=10.0&zyeid=8882fb29765446dba3ff677e0b41e3a1&usr=i2184309278&rgt=7&p1=VoVRBOjCfgEDAFntLM%2Fye7BT&pc=10&p2=124009&p3=17101856&p4=501656&p5=19&p6=&p7=__624047014896077&p9=2&p12=&p16=OPPO+R9m&p21=3&p22=5.1&p25=17101856&p26=22'.format(data['id'])
                res_detail = requests.get(detail_url, headers=get_headers(), verify=False)
                data = get_data_list(res_detail, 'body')
                print(data['bookInfo']['bookName'], data['bookInfo']['lastChapterTime'], data['chaperInfo']['chapterName'])
                break
            time.sleep(1)

def dejian_rank():
    rank_list = [
        ('女生-热读榜', 34552),
        ('男生-热读榜', 34566),
        ('男生-好评榜', 34567),
    ]
    for rank_name, rank_id in rank_list:
        for i in range(3):
            url = 'https://dj.palmestore.com/zybk/api/rank/books?pageSize=20&currentPage={}&sectionId={}&type=normal&style=NEW-STYLE0&freqKey=MF0004&plug=79&pluginVersion=79&a0=null&pk=null&today=1&zyeid=8882fb29765446dba3ff677e0b41e3a1&usr=i2184309278&rgt=7&p1=VoVRBOjCfgEDAFntLM%2Fye7BT&pc=10&p2=124009&p3=17101856&p4=501656&p5=19&p6=&p7=__624047014896077&p9=2&p12=&p16=OPPO+R9m&p21=3&p22=5.1&p25=17101856&p26=22'.format(i+1, rank_id)
            response = requests.get(url, headers=get_headers(), verify=False)
            # print(json.loads(res_books.text))
            print('=='*10, rank_name, i+1)
            for data in get_data_list(response, 'body'):
                # print(data['name'])
                time.sleep(1)
                detail_url = 'https://dj.palmestore.com/zybk/api/detail/index?bid={}&pluginVersion=10.0&zyeid=8882fb29765446dba3ff677e0b41e3a1&usr=i2184309278&rgt=7&p1=VoVRBOjCfgEDAFntLM%2Fye7BT&pc=10&p2=124009&p3=17101856&p4=501656&p5=19&p6=&p7=__624047014896077&p9=2&p12=&p16=OPPO+R9m&p21=3&p22=5.1&p25=17101856&p26=22'.format(data['id'])
                res_detail = requests.get(detail_url, headers=get_headers(), verify=False)
                data = get_data_list(res_detail, 'body')
                print(data['bookInfo']['bookName'], data['bookInfo']['lastChapterTime'], data['chaperInfo']['chapterName'])
                break
            time.sleep(1)

if __name__ == '__main__':
    dejian_category()
    # dejian_rank()