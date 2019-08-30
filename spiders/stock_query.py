from decrypt_methed import *
import pandas as pd


def percent(start, end):
    start, end = float(start), float(end)
    num = float(format((end - start) / start, '.4f'))
    return '%.2f%%' % (num * 100)


url_1 = 'https://suggest3.sinajs.cn/suggest/type=&key={}&name=suggestdata_1566398624177'
url_2 = 'https://hq.sinajs.cn/?_=0.782942645967817&list={}'
url_3 = 'https://finance.sina.com.cn/realstock/company/{}/nc.shtml'

# names = ['立讯精密', '穗恒运A', '依顿电子', '京能电力', '江南水务', '氯碱化工', '中国国贸', '平高电气', '皇马科技', '新天然气', '陕西黑猫', '民和股份', '基蛋生物', '海翔药业', '温氏股份']
# names = ['三安光电', '宁夏建材', '多氟多', '华银电力', '平煤股份', '天邦股份', '正邦科技', '分众传媒', '浙商证券', '中材国际', '祥和实业', '皖天然气', '惠发食品', '中材科技', '九牧王', '贵研铂业', '国药股份', '珠江啤酒', '天士力', '北辰实业', '中国巨石', '金牌厨柜', '中光学', '康恩贝', '中海油服', '诚意药业', '科大讯飞']
# names = ['旺能环境', '仁和药业', '万润股份', '老板电器', '石基信息', '恒生电子', '洋河股份', '浙江美大', '立讯精密', '歌尔股份', '巨化股份', '万科A', '圣邦股份', '信维通信', '中国人寿']
names = ['万向德农', '双汇发展', '旺能环境', '仁和药业', '老板电器', '洋河股份', '立讯精密', '歌尔股份']
# names = ['中信证券', '中国人寿', '东北证券', '华能水电', '华远地产', '金', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
while True:
    print('--开始, time:{}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
    data_list = []
    for name in names:
        time.sleep(0.4)
        res_1 = requests.get(url_1.format(name), headers=get_headers(), timeout=10)
        try:
            code = re.findall(r'"(.*?)";', res_1.text, re.S)[0].split(',')[3]
        except:
            print(name)
            continue
        res_2 = requests.get(url_2.format(code), headers=get_headers(), timeout=10)
        data = re.findall(r'"(.*?)";', res_2.text, re.S)[0].split(',')
        # res_3 = requests.get(url_3.format(code), headers=get_headers(), timeout=10)
        # price_5 = re.findall(r'price_5_ago = (\d+.?\d*)', res_3.text, re.S)[0]
        # price_10 = re.findall(r'price_10_ago = (\d+.?\d*)', res_3.text, re.S)[0]
        # price_20 = re.findall(r'price_20_ago = (\d+.?\d*)', res_3.text, re.S)[0]
        # price_60 = re.findall(r'price_60_ago = (\d+.?\d*)', res_3.text, re.S)[0]
        item=dict(
            名称=name,
            代码=re.findall(r'\d+', code, re.S)[0],
            股价=data[3],
            昨收=data[2],
            今开=data[1],
            开幅=percent(data[2], data[1]),
            涨幅=percent(data[2], data[3]),
            涨值='%.2f' % (float(data[3]) - float(data[2])),
            最高=data[4],
            最低=data[5],
            # price_5=price_5,
            # price_5=percent(price_5, data[3]),
            # price_10=price_10,
            # price_10=percent(price_10, data[3]),
            # price_20=price_20,
            # price_20=percent(price_20, data[3]),
            # price_60=price_60,
            # price_60=percent(price_60, data[3]),
            # 振幅=data[],
            # 换手率=data[],
            # 市净率=data[],
            # 市盈率=data[],
            成交量='%.2f' % (int(data[8]) / 10**6) + '万手',
            成交额='%.2f' % (float(data[9]) / 10**8) + '亿元',
            # 总市值=data[],
            # 总股本=data[],
            # 流通值=data[],
            # 流通股=data[],
            时间=data[30] + " " + data[31],
        )
        data_list.append(item)
        up_percent= eval(re.findall(r'-?\d+.?\d*', item['涨幅'], re.S)[0])
        if up_percent> 2.5 or up_percent < -2.5:
            print('-'*10, name, up_percent, '-'*10)
    # df = pd.DataFrame(data_list, dtype='str')
    # df.to_excel('/Users/houjie/Desktop/股票_{}_{}.xls'.format(names[1], item['时间'][:10]), index=0, encoding='gbk')
    time.sleep(60)
