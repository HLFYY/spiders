import random
import time
import tornado.ioloop
import tornado.web
import redis
import hashlib
from adsl_settings import *

logger = logger(file_name='adsl_server', handel='console')

def get_sign(key):
    sign_raw = MD5(key)
    salt = '46whetf6'
    sign = ''
    for index in range(8):
        sign += sign_raw[index] + salt[index]
    return sign

redis = redis.Redis(**REDIS_SPIDER)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        keys = redis.keys('proxy_*')
        if keys and redis.get(random.choice(keys)):
            key = random.choice(keys)
            ip_port = redis.get(key)
            ip_port = ip_port.decode()
            logger.info('-----back ip:{}'.format(ip_port))
            back_data = {
                'message': 'SUCCESS',
                'proxy': ip_port,
                'proxy_num': len(keys),
            }
            redis.incr('time_{}'.format(key.decode()))
            self.write(json.dumps(back_data, ensure_ascii=False))
        else:
            back_data = {
                'message': 'FALSE',
                'proxy': '',
                'proxy_num': 0,
            }
            logger.info('-----not ip')
            self.write(json.dumps(back_data, ensure_ascii=False))

    def post(self):
        ip = self.get_body_argument('ip', default=None, strip=False)
        port = self.get_body_argument('port', default='3244', strip=False)
        name = self.get_body_argument('name', default=None, strip=False)
        key = self.get_body_argument('key', default=None, strip=False)
        sign = self.get_body_argument('sign', default=None, strip=False)
        logger.info('----get_proxy_ip: ip:{}, port:{}, name:{}, key:{}, sign:{}'.format(ip, port, name, key, sign))
        if sign == get_sign(key) and ip:
            proxy = ip + ':' + port
            redis.set('proxy_'+name, proxy)
            redis.sadd('use_ips', ip)
            response = {
                'message': 'SUCCESS',
                'reason': '',
            }
        elif sign != get_sign(key):
            response = {
                'message': 'FALSE',
                'reason': 'Wrong Token',
            }
        else:
            response = {
                'message': 'FALSE',
                'reason': 'No Client ip',
            }
        self.write(json.dumps(response, ensure_ascii=False))

class MainDelete(tornado.web.RequestHandler):
    def post(self):
        name = self.get_body_argument('name', default=None, strip=False)
        key = self.get_body_argument('key', default=None, strip=False)
        sign = self.get_body_argument('sign', default=None, strip=False)
        logger.info('----del_proxy_ip: name:{}, key:{}, sign:{}'.format(name, key, sign))
        if sign == get_sign(key):
            redis.delete('proxy_' + name)
            response = {
                'message': 'SUCCESS',
                'reason': '',
            }
        else:
            response = {
                'message': 'FALSE',
                'reason': 'Wrong Token',
            }
        self.write(json.dumps(response, ensure_ascii=False))


def make_app():
    return tornado.web.Application([
        (r"/proxy", MainHandler),
        (r"/proxy/delete", MainDelete),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()