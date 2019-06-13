from adsl_settings import *


def record_ips():
    r = redis.Redis()
    client = MongoClient(MONGO_STR)
    collection = client['record']['exists_proxy']
    data = redis.smembers('use_ips')
    print(data)

if __name__ == '__main__':
    record_ips()