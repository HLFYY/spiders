# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from spider_source.bloomfilter_redis import BloomFilter_Redis
from spider_source.settings import *


class SpiderSourcePipeline(object):
    def open_spider(self, spider):
        name = spider.name
        self.bot_name = BOT_NAME

        if spider.name in []:
            name = ''

        size = BLOOM_PARAM.get(name, [24])[0]
        self.bf_redis = BloomFilter_Redis(REDIS_FILTER, bit=size, redis_name='{}:{}:{}'.format(self.bot_name, name, 'blm'))
        self.r = redis.Redis(**REDIS_SPIDER)
        self.client = MongoClient(MONGO_STR)
        self.collection = self.client[self.bot_name][name]

        logging.info('---redis_bloom:{}, size:{}'.format('{}:{}:{}'.format(self.bot_name, name, 'blm'), size))

    def push_redis_key(self, item, spider):
        if 'ccpush' in item and isinstance(item['ccpush'], dict):
            for key, value in item['ccpush'].items():
                self.r.rpush(key, value)
        else:
            self.r.rpush(BOT_NAME + ":" + spider.name + ":push", item['_id'])

    def process_item(self, item, spider):
        if '_id' in item:
            item['_id'] = str(item['_id'])
        item['crawl_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
        item['cctime'] = int(time.time())

        if item.get('save_type') == 'insert':
            exists = self.collection.find_one({'_id': item['_id']})
            if not exists:
                self.collection.insert(item)
                self.push_redis_key(item, spider)

        elif item.get('save_type') == 'update':
            if self.collection.find_one({'_id': item['_id']}):
                self.collection.update_one({'_id': item['_id']}, {'$set': item})
                self.push_redis_key(item, spider)

        elif item.get('save_type') == 'replace':
            self.collection.replace_one({'_id': item['_id']}, item, True)
            self.push_redis_key(item, spider)

        else:
            self.push_redis_key(item, spider)

        return item

    def close_spider(self, spider):
        self.client.close()
