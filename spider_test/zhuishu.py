from base import *


def zhui_category():
    url = 'http://b01.zhuishushenqi.com/v2/category/statics?packageName=com.ushaqi.zhuishushenqi.adfree&hasTag=true'
    response = requests.get(url, headers=get_headers(), verify=False)
    for key, val in get_data_list(response, 'category').items():
        if key in ['male']:
            for data_2 in val:
                print('=='*10, key, data_2['name'])
                cate_tag = data_2['alias']
                time.sleep(1)
                books_url= 'http://b01.zhuishushenqi.com/category/fuzzy-search?alias={}&packageName=com.ushaqi.zhuishushenqi.adfree&sort=1&price=1&start=0&limit=30'.format(cate_tag)
                res_books = requests.get(books_url, headers=get_headers(), verify=False)
                # for i in range(100):
                #     books_url = 'http://b01.zhuishushenqi.com/category/fuzzy-search?alias={}&packageName=com.ushaqi.zhuishushenqi.adfree&sort=1&price=1&start={}&limit=30'.format(cate_tag, i*30)
                #     res_books = requests.get(books_url, headers=get_headers(), verify=False)
                #     print(i+1, get_data_list(res_books, 'books')[0]['title'], '+++', get_data_list(res_books, 'books')[1]['title'])
                #     time.sleep(1)
                for book_data in get_data_list(res_books, 'books'):
                    print(book_data['title'])
                    book_id = book_data['_id']
                    time.sleep(1)
                    detail_url = 'https://bookapi01.zhuishushenqi.com/book/{}?t=0&useNewCat=true&packageName=com.ushaqi.zhuishushenqi.adfree'.format(book_id)
                    res_detail = requests.get(detail_url, headers=get_headers(), verify=False)
                    print(res_detail.text)
                    title, date = get_data_list(res_detail, 'title'), get_data_list(res_detail, 'updated')
                    print(title, date, get_data_list(res_detail, 'lastChapter'))


def zhuishu_rank():
    for id in ['cb5696d03d5f4616989a11897f7d96e9', 'e72b146305e74fff9a6fe1cbeedd3601']:
        url = 'https://b.zhuishushenqi.com/category/rankinfo?ajax=ajax&size=100&st=1&node={}&token=&type=main_free&packageName=com.ushaqi.zhuishushenqi.adfree'.format(id)
        response = requests.get(url, headers=get_headers(), verify=False)
        node = get_data_list(response, 'node')['title']
        print('++'*10, node, len(get_data_list(response, 'book')))
        for book_data in get_data_list(response, 'book')[:2]:
            print(book_data['title'])
            detail_url = 'https://bookapi01.zhuishushenqi.com/book/{}?t=0&useNewCat=true&packageName=com.ushaqi.zhuishushenqi.adfree'.format(
                book_data['_id'])
            time.sleep(1)
            res_detail = requests.get(detail_url, headers=get_headers(), verify=False)
            title, date = get_data_list(res_detail, 'title'), get_data_list(res_detail, 'updated')
            print(title, date, get_data_list(res_detail, 'lastChapter'))



if __name__ == '__main__':
    zhui_category()
    # zhuishu_rank()