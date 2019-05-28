import random

import tornado.ioloop
import tornado.web
import redis
import hashlib

def MD5(data_str):
    object = hashlib.md5()
    object.update(data_str.encode('utf-8'))
    return object.hexdigest()

def get_sign(key):
    sign_raw = MD5(key)
    salt = '46whetf6'
    sign = ''
    for index in range(8):
        sign += sign_raw[index] + salt[index]
    return sign

redis = redis.Redis()
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        keys = redis.keys('proxy_*')
        if keys and redis.get(random.choice(keys)):
            data = redis.get(random.choice(keys))
            self.write(data)
        else:
            self.write('NO PROXY')


    def post(self):
        ip = self.get_body_argument('ip', default=None, strip=False)
        port = self.get_body_argument('port', default='8888', strip=False)
        name = self.get_body_argument('name', default=None, strip=False)
        key = self.get_body_argument('key', default=None, strip=False)
        sign = self.get_body_argument('sign', default=None, strip=False)
        print('ip:{}, port:{}, name:{}, key:{}, sign:{}'.format(ip, port, name, key, sign))
        if sign == get_sign(key) and ip:
            proxy = ip + ':' + port
            print('Receive proxy', proxy)
            redis.set('proxy_'+name, proxy)
        elif sign != get_sign(key):
            self.write('Wrong Token')
        elif not ip:
            self.write('No Client ip')

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()