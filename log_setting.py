# coding:utf-8
import os
import logging
import logging.config
from base_settings import SPIDER_LOG_DIR, SERVER_LOG_DIR, ONLINE

# 给过滤器使用的判断
class RequireDebugTrue(logging.Filter):
    # 实现filter方法
    def filter(self, record):
        return ONLINE


LOGGING = {
    # 基本设置
    'version': 1,  # 日志级别
    'disable_existing_loggers': False,  # 是否禁用现有的记录器

    # 日志格式集合
    'formatters': {
        # 标准输出格式
        'standard': {
            # [具体时间][线程名:线程ID][日志名字:日志级别名称(日志级别ID)] [输出的模块:输出的函数]:日志内容
            # 'format': '[%(asctime)s][%(threadName)s:%(thread)d][%(name)s:%(levelname)s(%(lineno)d)]\n[%(module)s:%(funcName)s]:%(message)s'
            'format': '%(asctime)s [%(name)s] %(levelname)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },

    # # 过滤器
    # 'filters': {
    #     'require_debug_true': {
    #         '()': RequireDebugTrue,
    #     }
    # },

    # 处理器集合
    'handlers': {
        # 输出到控制台
        'console': {
            'level': 'DEBUG',  # 输出信息的最低级别
            'class': 'logging.StreamHandler',
            'formatter': 'standard',  # 使用standard格式
            # 'filters': ['require_debug_true', ],  # 仅当 DEBUG = True 该处理器才生效
        },
        # 输出到文件
        'log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(SERVER_LOG_DIR, 'default.log'),  # 输出位置
            'maxBytes': 1024 * 1024 * 50,  # 文件大小
            'backupCount': 5,  # 备份份数
            'encoding': 'utf8',  # 文件编码
        },
    },

    # 日志管理器集合
    'loggers': {
        # 管理器
        'root': {
            'handlers': ['log', 'console'],
            'level': 'DEBUG',
            'propagate': False,  # 是否传递给父记录器
        },
    }
}

def logger(file_name=None, level=None, type='server', handel=None):
    dir = SERVER_LOG_DIR if type == 'server' else SPIDER_LOG_DIR
    if file_name:
        LOGGING['handlers']['log']['filename'] = os.path.join(dir, '{}.log'.format(file_name))
    if level:
        LOGGING['loggers']['root']['level'] = level
    if handel and handel in ['log', 'console']:
        LOGGING['loggers']['root']['handlers'] = ['{}'.format(handel)]
    # 加载前面的标准配置
    logging.config.dictConfig(LOGGING)
    # 获取loggers其中的一个日志管理器
    logger = logging.getLogger("root")
    return logger
