# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：    bloomfilter_redis.py 
   Description :  布隆过滤器结合redis进行过滤
   Author :       fanty
   date：         2018/8/7 
"""

import redis
from hashlib import md5

class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(value.__len__()):
            ret += self.seed * ret + ord(value[i])
        return ((self.cap-1) & ret)


class BloomFilter_Redis(object):
    def __init__(self, redis_set, bit=24, redis_name='bloomfilter'):
        """
        :param REDIS_SET: 连接redis的配置
        :param redis_name:
        """
        self.r = redis.Redis(**redis_set)
        self.bit_size = 1 << bit  # Redis的String类型最大容量为512M
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.hashfunc = []
        self.name = redis_name

        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

    def md5_encrypt(self, str_input):
        m5 = md5()
        m5.update(str_input.encode(encoding='utf8'))
        return m5.hexdigest()

    def isContains(self, str_input):
        str_input = str(str_input)
        if len(str_input) >= 100:
            str_input = self.md5_encrypt(str_input)
        ret = True
        for f in self.hashfunc:
            loc = f.hash(str_input)
            ret = ret & self.r.getbit(self.name, loc)
        return ret

    def insert(self, str_input):
        str_input = str(str_input)
        if len(str_input) >= 100:
            str_input = self.md5_encrypt(str_input)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            self.r.setbit(self.name, loc, 1)
