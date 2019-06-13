import pymongo

from adsl_settings import *

logger = logger(file_name='record_ips')

def record_ips():
    r = redis.Redis(**REDIS_SPIDER)
    client = MongoClient(MONGO_STR)
    collection = client['record']['exists_proxy']
    data = r.smembers('use_ips')
    data =[d.decode() for d in data]
    data.sort()
    save_data = {
        '_id': time.strftime("%Y-%m-%d %H:%M:%S"),
        'ips': data,
        'ip_num': len(data)
    }
    logger.info('---time:{}, ips:{}'.format(save_data['_id'], save_data['ip_num']))
    collection.insert_one(save_data)
    client.close()

def record_proxy_use():
    r = redis.Redis(**REDIS_SPIDER)
    client = MongoClient(MONGO_STR)
    col_total = client['record']['proxy_use_total']
    col = client['record']['proxy_use_current']

    # 获取最近一次统计的代理使用数
    last_data_count = [{}]
    if col_total.find_one():
        last_data_count = list(col_total.find().sort("_id", pymongo.DESCENDING).limit(1))
    last_data_count = last_data_count[0]
    logger.info('--上次统计的代理使用数：{}'.format(last_data_count))
    total_data_counts = {}
    current_data_counts = {}
    keys = r.keys('time_*')
    for key_name in keys:
        key_name = key_name.decode()
        count = r.get(key_name)
        total_data_counts[key_name] = int(count.decode())
        current_data_counts[key_name] = int(count.decode()) - int(last_data_count.get(key_name, 0))

    total_data_counts['_id'] = time.strftime("%Y-%m-%d %H:%M:%S")
    current_data_counts['_id'] = time.strftime("%Y-%m-%d %H:%M:%S")
    logger.info('--当前代理使用数：{}, \n--较上次统计新增量:{}\n'.format(total_data_counts, current_data_counts))
    col.insert_one(current_data_counts)
    col_total.insert_one(total_data_counts)
    client.close()


if __name__ == '__main__':
    record_ips()
    record_proxy_use()