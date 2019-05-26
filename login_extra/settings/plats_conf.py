from classes.example.baitong_extract import BaiduExtract
from classes.baidu.baidu_login import BaiduLogin


PLATS_INFO = [
    dict(
        acc='',
        pwd='',
        plat='',
        driver='c'
    ),
]


LOGIN_MAPPING = {
    'baidu': BaiduLogin,
}


EXTRACT_MAPPING = {
    'baidu': BaiduExtract,
}


PLAT_ID_DRIVER_MAPPING = {
    'baidu': [38, 'c'],
}

GDT_MAPPING = {
    '3431283291': '7055871',
}

SMSEN_MAPPING = {
    'znteccc': '25704241',
}

