import redis

redis = redis.Redis()
data = redis.smembers('use_ips')
print('----')