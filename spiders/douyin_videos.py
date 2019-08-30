import time
import json
import requests
from douyin_sign import get_douyin_url, get_headers


def get_author_info(user_id):
    url = get_douyin_url(type='author_info', user_id=user_id)
    response = requests.get(url, headers=get_headers())
    user_data = json.loads(response.text)['user']
    item=dict(
        user_name=user_data['nickname'],
        user_id=user_data['unique_id'],
        fans=user_data['follower_count'],
        digg_count=user_data['total_favorited'],
        video_count=user_data['aweme_count'],
    )
    return item


def get_author_videos(user_id, max_cursor='', start_time=''):
    start_time = start_time if start_time else int(time.time())-3600*24*180
    total = 0
    while True:
        author_url = get_douyin_url(user_id=user_id, max_cursor=max_cursor)
        response = requests.get(author_url, headers=get_headers())
        res_dict = json.loads(response.text)
        data_list = res_dict['aweme_list']
        has_more = res_dict['has_more']
        num = 0
        for data in data_list:
            total += 1
            if start_time <= int(data['create_time']):
                item = dict(
                    title=data['desc'],
                    update_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data['create_time']))),
                    digg_count=data['statistics']['digg_count'],
                    comment_count=data['statistics']['comment_count'],
                )
                yield item
                num += 1
        print(has_more, num)
        if has_more and num:
            max_cursor = res_dict['max_cursor']
            time.sleep(0.4)
        else:
            print('视频数：{}'.format(total))
            break


if __name__ == '__main__':
    author_data = get_author_info('00QqxG2E')
    print(author_data)

    for data in get_author_videos('60424463447'):
        print(data)