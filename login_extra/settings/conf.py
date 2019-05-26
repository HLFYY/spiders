from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import json
import os
import requests
from datetime import datetime
import copy
import hashlib
import time
import base64
import random
import urllib3
import re
import platform


LOGIN_PLATS = []
CRAWL_PLATS = []

DIR_ = '/Users/houjie/Desktop/images/'
if not os.path.exists(DIR_):
    os.system('mkdir -p {}'.format(DIR_))

TASK_REDIS_KEY = 'task_queue'

MONGO_SETTING = {
    'host': 'localhost',
    'port': 27017,
    'db': 'cookies',
    'col': 'cookies',
}
REDIS_SET_URL = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 2,
    'password': '',
}
REDIS_SET_FILTER = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 4,
    'password': ''
}
MONGO_STR = "mongodb://{host}:{port}/{db}".format(**MONGO_SETTING)
REDIS_URL = 'redis://:{password}@{host}:{port}?db={db}'.format(**REDIS_SET_URL)

PROCESS_NUMS = 1


USER_AGENT = [
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.125 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
]

PROXY_LIST = [
    'http://user:pass@ip:port',
]

