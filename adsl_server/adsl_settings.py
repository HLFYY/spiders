import os
import sys
envplat_dir = os.path.dirname(os.path.realpath(__file__)).split("spiders")[0]
sys.path.append(envplat_dir + "spiders")
# from base_settings import *
from base_method import *
from log_setting import logger

