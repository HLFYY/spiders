import json
from multiprocessing import Process, Queue

import redis

from settings.plats_conf import *
from tool.warpper import warning
from copy import copy
from settings.conf import PROCESS_NUMS, TASK_REDIS_KEY, REDIS_SET_URL
import time
import os


class Tasks(object):
    def __init__(self, process_nums=1, type='login'):
        self.process_nums = process_nums
        self.q = Queue()
        self.r_task = redis.Redis(**REDIS_SET_URL)
        if type == 'login':
            self.run_task = self.login_task
        else:
            self.run_task = self.crawl_task

    def run(self, tasks=[]):
        # if self.process_nums < 2:
        #     for task in tasks:
        #         self.run_task(task)
        # else:
        #     for task in tasks:
        #         self.q.put(task)
        #     time.sleep(2)
        #
        #     list_com = list()
        #     for i in range(self.process_nums):
        #         com = Process(target=self.task_distribution, args=(self.q,))
        #         list_com.append(com)
        #     for p in list_com:
        #         p.start()
        while True:
            print('---time:{}, start'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
            key, val = self.r_task.blpop(TASK_REDIS_KEY)
            task = json.loads(val.decode('utf8'))
            print('----time:{}, data:{}, run...'.format(time.strftime("%Y-%m-%d %H:%M:%S"), task))
            self.run_task(task)

    # def task_distribution(self, q):
    #     while True:
    #         if q.empty():
    #             print(os.getpid(), '退出')
    #             break
    #         task = q.get()
    #         self.run_task(task)

    def login_task(self, task):
        plat = task['plat']
        try:
            task = copy(task)
            plat_obj = LOGIN_MAPPING[plat](**task)
            plat_obj.run()
            plat_obj.close()
        except Exception as e:
            warning('plat: {} || login_error || {}'.format(plat, e))

    def crawl_task(self, task):
        plat = task['plat']

        plat_obj = EXTRACT_MAPPING[plat](**task)
        try:
            plat_obj.start_crawl()
        except Exception as e:
            warning('plat: {} || crawl_data_error || {} || reason: {}'.format(plat, task['acc'], e))
        plat_obj.close()


if __name__ == '__main__':
    Tasks().run(PLATS_INFO)
