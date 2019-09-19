from base import *

# 排行榜数据列表页接口（分类下的书籍列表和排行榜下的书籍列表）请求，response中没有bookList字段时，可视为该排行榜抓取完成

# 分类下的书籍列表页请求, headers中不携带qimei参数，请求的数据和抓包的不同,带上则一样，且该参数可随意修改后几位数字
headers = {
'qimei': '864394550382488',
'User-Agent': 'okhttp/3.6.0',
}

# 书籍详情页请求，headers中需携带下面的参数，少了或者改动则无法获取数据，需要验证这些参数的时效性
detail_headers = {
    'qrem': '1',
    'qrtm': '1568606547',
    'qrsy': '535646A24BE1DCD107A270E582333A88',
    'c_version': 'qqreader_7.0.8.0888_android',
    'User-Agent': 'okhttp/3.6.0'
}

def qq_category():
    # 男生
    # url = 'https://androidtgw.reader.qq.com/v7_0_8/queryOperation?categoryFlag=1'
    url = 'https://androidtgw.reader.qq.com/v7_0_8/queryOperation?categoryFlag=2'
    response = requests.get(url, headers=get_headers(), verify=False)
    print(response.text)
    # for data in get_data_list(response, 'boyCategoryList'):
    for data in get_data_list(response, 'girlCategoryList'):
        name, cate_id = data['categoryName'], data['actionId']
        time.sleep(1)
        book_list_url = 'http://rec.reader.qq.com/v7_0_8/listDispatch?actionTag=,-1,-1,-1,-1,101&actionId={}&action=categoryV3&pagestamp={}'.format(
            cate_id, 1)
        res_books = requests.get(book_list_url, headers=headers, verify=False)
        # for i in range(100):
        #     book_list_url = 'http://rec.reader.qq.com/v7_0_8/listDispatch?actionTag=,-1,-1,-1,-1,101&actionId={}&action=categoryV3&pagestamp={}'.format(
        #         cate_id, i + 1)
        #     res_books = requests.get(book_list_url, headers=headers, verify=False)
        #     try:
        #         book_list = get_data_list(res_books, 'bookList')
        #     except:
        #         print(res_books.text)
        #     print(len(book_list), i+1, book_list[0]['title'], book_list[1]['title'])
        #     time.sleep(1)
        for book_data in get_data_list(res_books, 'bookList'):
            title, book_id = book_data['title'], book_data['bid']
            book_url = 'https://androidtgw.reader.qq.com/v7_0_8/nativepage/book/detail?bid={}&pagestamp=1&alg=70.5.43&origin={}&dataType=cate_id&data_type=0&fromPage=&qmk=1,6,9'.format(book_id, cate_id)
            res_book_detail = requests.get(book_url, headers=detail_headers, verify=False)
            chapinfo = get_data_list(res_book_detail, 'chapinfo')
            info = get_data_list(res_book_detail, 'introinfo')
            print(info['book']['title'], info['book']['copyrightinfo'], chapinfo['lastcname'])
            time.sleep(1)
        print('=='*20)
        # break


def qq_rank():
    # url = 'https://commontgw.reader.qq.com/v7_0_8/queryOperation?pagestamp=1&rankFlag=1'
    url = 'https://commontgw.reader.qq.com/v7_0_8/queryOperation?pagestamp=1&rankFlag=2'
    response = requests.get(url, headers=get_headers(), verify=False)
    print(response.text)
    # for data in get_data_list(response, 'boyCategoryList'):
    for data in get_data_list(response, 'rank'):
        rank_name, rank_id, rank_tag = data['title'], data['actionId'], data['actionTag']
        print('--'*3, rank_name, rank_tag)
        rank_url = 'https://commontgw.reader.qq.com/v7_0_8/listDispatch?action=rank&actionTag={}&actionId={}&pagestamp={}&plan=1'.format(
            rank_tag, rank_id, 1)
        res_books = requests.get(rank_url, headers=get_headers(), verify=False)
        book_list = get_data_list(res_books, 'bookList')
        # 排行榜接口请求，response中没有bookList字段时，可视为该排行榜抓取完成
        # for i in range(100):
        #     rank_url = 'https://commontgw.reader.qq.com/v7_0_8/listDispatch?action=rank&actionTag={}&actionId={}&pagestamp={}&plan=1'.format(rank_tag, rank_id, i+1)
        #     res_books = requests.get(rank_url, headers=get_headers(), verify=False)
        #     try:
        #         book_list = get_data_list(res_books, 'bookList')
        #     except:
        #         print(res_books.text)
        #     print(len(book_list), i+1, book_list[0]['title'])
        #     time.sleep(1)
        for book_data in book_list:
            title, book_id = book_data['title'], book_data['bid']
            book_url = 'https://androidtgw.reader.qq.com/v7_0_8/nativepage/book/detail?bid={}&pagestamp=1&alg=70.5.43&origin={}&dataType=cate_id&data_type=0&fromPage=&qmk=1,6,9'.format(
                book_id, rank_id)
            res_book_detail = requests.get(book_url, headers=detail_headers, verify=False)
            chapinfo = get_data_list(res_book_detail, 'chapinfo')
            info = get_data_list(res_book_detail, 'introinfo')
            print(info['book']['title'], info['book']['copyrightinfo'], chapinfo['lastcname'])
            time.sleep(1)
        print('==' * 20)


if __name__ == '__main__':
    qq_category()
    # qq_rank()
    # url = 'https://androidtgw.reader.qq.com/v7_0_8/nativepage/book/detail?bid=25847364&pagestamp=1&alg=70.5.43&origin=30013&dataType=cate_id&data_type=0&fromPage=&qmk=1,6,9'
    #
    # res_book_detail = requests.get(url, headers=headers, verify=False)
    # print(res_book_detail.text)