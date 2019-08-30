from pymongo import MongoClient
import pandas as pd
from spider_source.settings import MONGO_STR, BOT_NAME


def data2excel():
    client = MongoClient(MONGO_STR)
    collection = client[BOT_NAME]['kasi_search']
    datas = collection.find()
    result_list = []
    for data in datas:
        people = dict(
            机构名称=data['mcn_name'],
            行业标签=data['tag_name'],
            机构简介=data['mcn_desc'],
            账号名称=data['user_name'],
            粉丝数=data['fans'],
            获赞数=data['digg_count'],
            作品数=data['videos'],
            is_search=data.get('is_search', 0),
            is_douyin=data.get('is_douyin', 0),
            平台标识链接=data.get('platform_icon', ''),
            平台链接=data.get('platform_url', ''),
            微博链接=data.get('weibo_url', ''),
            用户标签=data.get('tags', ''),
            集均评论数=data.get('per_comment_count', ''),
            集均点赞数=data.get('per_digg_count', ''),
            集均分享数=data.get('per_share_count', ''),
            发布视频=data.get('videos_kasi', ''),
            视频发布频率=data.get('videos_per_work', ''),
            大爆款视频=data.get('high_hot', ''),
            中爆款视频=data.get('middle_hot', ''),
            小爆款视频=data.get('low_hot', ''),
        )
        for key,val in data.get('age_data', {}).items():
            people[key.replace('age_', '')] = val
        result_list.append(people)

    df = pd.DataFrame(result_list, dtype='str')
    df.to_excel('{}.xls'.format('MCN'), index=0, encoding='gbk')

def get_data():
    client = MongoClient(MONGO_STR)
    collection = client[BOT_NAME]['kasi_search']
    datas = collection.find()
    result_list = {}
    keys = ['机构名称', '行业标签', '机构简介', '账号名称', '粉丝数', '获赞数', '作品数', 'is_search', 'is_douyin', '平台标识链接', '平台链接', '微博链接', '用户标签', '集均评论数', '集均点赞数', '集均分享数', '发布视频', '视频发布频率', '大爆款视频', '中爆款视频', '小爆款视频', '6-17', '18-24', '25-30', '31-35', '36-40', '40+']
    for key in keys:
        result_list[key] = []
    for data in datas:
        people = dict(
            机构名称=data['mcn_name'],
            行业标签=data['tag_name'],
            机构简介=data['mcn_desc'],
            账号名称=data['user_name'],
            粉丝数=data['fans'],
            获赞数=data['digg_count'],
            作品数=data['videos'],
            is_search=data.get('is_search', 0),
            is_douyin=data.get('is_douyin', 0),
            平台标识链接=data.get('platform_icon', ''),
            平台链接=data.get('platform_url', ''),
            微博链接=data.get('weibo_url', ''),
            用户标签=data.get('tags', ''),
            集均评论数=data.get('per_comment_count', ''),
            集均点赞数=data.get('per_digg_count', ''),
            集均分享数=data.get('per_share_count', ''),
            发布视频=data.get('videos_kasi', ''),
            视频发布频率=data.get('videos_per_work', ''),
            大爆款视频=data.get('high_hot', ''),
            中爆款视频=data.get('middle_hot', ''),
            小爆款视频=data.get('low_hot', ''),
        )
        for key, val in data.get('age_data', {}).items():
            people[key.replace('age_', '')] = val
        for key, val in result_list.items():
            result_list[key].append(people.get(key, ''))
        # temp = []
        # for key in keys:
        #     temp.append(str(people.get(key, '')))
        # print(temp)
        # ', '.join(temp)
        # result_list.append(', '.join(temp))
    All = []
    for data, val in result_list.items():
        df = pd.DataFrame({data: val})
        All.append(df)

    writer = pd.ExcelWriter('test.xlsx')

    for dd in All:
        print(keys[All.index(dd)], All.index(dd))
        dd.to_excel(writer, sheet_name=keys[All.index(dd)], startcol=All.index(dd), index=False)

if __name__ == '__main__':
    # get_data()
    # data2excel()
    print(len(['机构名称', '行业标签', '机构简介', '账号名称', '粉丝数', '获赞数', '作品数', 'is_search', 'is_douyin', '平台标识链接', '平台链接', '微博链接', '用户标签', '集均评论数', '集均点赞数', '集均分享数', '发布视频', '视频发布频率', '大爆款视频', '中爆款视频', '小爆款视频', '6-17', '18-24', '25-30', '31-35', '36-40', '40+']))


