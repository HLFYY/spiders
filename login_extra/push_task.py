import redis

from settings.conf import *

def push_login_data():
    r_task = redis.Redis(**REDIS_SPIDER_URL)
    push_data =dict(
        acc='',
        pwd='',
        plat='baidu',
        driver='c'
    )
    r_task.rpush(TASK_REDIS_KEY, json.dumps(push_data, ensure_ascii=False))

if __name__ == '__main__':
    push_login_data()