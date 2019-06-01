from decrypt_methed import *

url = 'https://blog.csdn.net/kun1280437633/article/details/80686305'
headers = dict(dict(
    Cookie='acw_sc__v2=5cf10aa41808a0e7a021beb970bdf566e5df2cad',
), **get_headers())
response = requests.get(url, headers=headers)
print(response.text, response.headers)