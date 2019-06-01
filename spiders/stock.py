from decrypt_methed import *

logger = logger(file_name='stock', type='spider')

def run(code, r=''):
    while True:
        proxies=get_proxy()
        url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd={}5&sty=FDPHKL2B&token=4f1862fc3b5e77c150a2b985b12db0fd&_={}'.format(code, int(time.time()*1000))
        try:
            response = requests.get(url, headers=get_headers(), proxies=proxies, timeout=10)
        except Exception as e:
            logger.info('---request is error, error:{}'.format(e))
            time.sleep(30)
            continue
        if response.text:
            body = re.findall(r'\((.*)\)', response.text, re.S)[0]
            data = json.loads(body)[0].split(',')
            item = dict(
                code=data[1],
                name=data[2],
                today_open=eval(data[3]),
                yestoday_close=eval(data[4]),
                price=eval(data[5]),
                up_count=eval(data[6]),
                up_percent=data[7],
                change_hand=data[8],
                highest=eval(data[9]),
                lowest=eval(data[10]),
            )
            if item['price'] > 1.25 :
                # send_note('price is low or '.format(item['price']))
                logger.info('---, data:{}'.format(item))
            print(item)
            time.sleep(60)

if __name__ == '__main__':
    run('02181')
    # r = redis.Redis(**REDIS_SPIDER)
    # while True:
    #     key, data = r.blpop('spider_stock')

