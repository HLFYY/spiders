import os
import sys
import execjs
envplat_dir = os.path.dirname(os.path.realpath(__file__)).split("spiders")[0]
sys.path.append(envplat_dir + "spiders")
from base_method import *

def get_data_list(response, key):
    return json.loads(response.text)[key]