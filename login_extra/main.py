import traceback
import time
from tool.process_tasks import Tasks
from tool.warpper import warning
from settings.conf import *
import os
import random
from settings.plats_conf import PLATS_INFO


def crawl_plats_data(num=PROCESS_NUMS):
    # plats = PLATS_INFO
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    # print('\n----{}--{}'.format(now, plats))
    # Tasks(process_nums=num, type='extra').run(plats)
    Tasks(process_nums=num, type='extra').run()


def run_plats_to_login(num=PROCESS_NUMS):
    # plats = PLATS_INFO
    # now = time.strftime("%Y-%m-%d %H:%M:%S")
    # print('\n>>>>{}--{}'.format(now, plats))
    # Tasks(process_nums=num).run(plats)
    Tasks(process_nums=num).run()


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('####------set argv----------####')
        sys.exit()
    try:
        if sys.argv[1] == 'login':
            run_plats_to_login()
            #
            # os.system("kill -9 $(ps -ef|grep chrom|grep -v grep|awk '{print $2}')")
            # os.system("kill -9 $(ps -ef|grep phantomjs|grep -v grep|awk '{print $2}')")
        elif sys.argv[1] == 'extract':
            crawl_plats_data()
        else:
            warning('sys.argv[1] not in [login, extract], invalid argument')
    except:
        content = 'location:{}, error:{}'.format(sys.argv[0], traceback.format_exc())
        warning(content)


