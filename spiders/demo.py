from decrypt_methed import *
import js2py

def haoduo_app():
    with open('csdn.js') as f:
        js = f.read()
    import execjs
    now = time.time()
    context = execjs.compile(js)
    res = context.call("cmd5x", '/jp/dash?tvid=11878510309&bid=500&abid=100&src=02027221010000000000&ut=0&ori=h5&ps=0&messageId=1559650754970&pt=0&lid=&cf=&ct=&locale=zh_cn&k_tag=1&dfp=a038afc5a7d37744f493c2030b915b91eb7b2265f33215877881bd2887b108a886&k_ft1=17729624997888&k_uid=1559650754971&qd_v=1&qdy=a&qds=0&tm=1559650754971&callback=onSuccess')
    print(res)
    print(time.time()-now)

def remove_error():
    import os
    import re

    paths = ["/Users/houjie/Desktop/code/xinlangxinwen_260/res/layout/",
             "/Users/houjie/Desktop/code/xinlangxinwen_260/res/layout-v17/",
             "/Users/houjie/Desktop/code/xinlangxinwen_260/res/layout-v21/",
             "/Users/houjie/Desktop/code/xinlangxinwen_260/res/layout-v26/",
             "/Users/houjie/Desktop/code/xinlangxinwen_260/res/animator-v21/",
             "/Users/houjie/Desktop/code/xinlangxinwen_260/res/color/",
             ]
    for path in paths:
        files = os.listdir(path)
        for tem in files:
            # if tem == "a1.xml":
            with open(path + tem, 'rb')as f:
                content = f.read().decode()
                # ress = re.findall(r'sina:.*?night=".*?"', content, flags=re.IGNORECASE)
                # re.sub(b'sina:.*?Night=".*?"', b'', content, count=-1, flags=re.IGNORECASE)
                # for res in ress:
                #   content = content.replace(res, '')
                ress = re.findall(r'app:.{0,28}=".*?"', content, flags=re.IGNORECASE)
                for res in ress:
                    # print(res,tem)
                    content = content.replace(res, '')
                ress = re.findall(r'fresco:.{0,29}=".*?"', content, flags=re.IGNORECASE)
                for res in ress:
                    # print(res,tem)
                    content = content.replace(res, '')
                ress = re.findall(r'android:keyboardNavigationCluster="true"', content, flags=re.IGNORECASE)
                for res in ress:
                    # print(res,tem)
                    content = content.replace(res, '')
                ress = re.findall(r'submit:.{0,20}=".*?"', content, flags=re.IGNORECASE)
                for res in ress:
                    # print(res,tem)
                    content = content.replace(res, '')
                ress = re.findall(r'video:.{0,20}=".*?"', content, flags=re.IGNORECASE)
                for res in ress:
                    # print(res,tem)
                    content = content.replace(res, '')
                ress = re.findall(r'sina[a-zA-Z.]*?:.*?=".*?"', content, flags=re.IGNORECASE)
                for res in ress:
                    # print(res,tem)
                    content = content.replace(res, '')
            with open(path + tem, 'wb')as f:
                f.write(content.encode())


if __name__ == '__main__':
    remove_error()

