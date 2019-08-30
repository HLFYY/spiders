import json
import time
import re
from string import ascii_lowercase
import requests


fontscn_h57yip2q = {
    '\\uabcf':'4',
    '\\uaced':'3',
    '\\uaedd':'8',
    '\\uaede':'0',
    '\\uafcd':'6',
    '\\ubdaa':'5',
    '\\ubdcd':'1',
    '\\ubfad':'9',
    '\\uccda':'2',
    '\\ucfbe':'7',
}
fontscn_3jqwe90k = {
    '\\uaacb':'4',
    '\\uabcd':'3',
    '\\uacdd':'0',
    '\\uaefb':'8',
    '\\uafbc':'6',
    '\\ubbca':'1',
    '\\ubdca':'5',
    '\\ubfee':'9',
    '\\uccac':'2',
    '\\ucfba':'7',
}
fontscn_yuh4hy4p = {
    '\\uaabd':'5',
    '\\uaadd':'0',
    '\\uacde':'9',
    '\\uadaa':'2',
    '\\uadac':'1',
    '\\uadcb':'7',
    '\\uaeed':'8',
    '\\ubebb':'3',
    '\\ucbdc':'6',
    '\\ucccf':'4',
}
fontscn_qw2f1m1o = {
    '\\uabcb':'4',
    '\\uaccd':'3',
    '\\uacda':'0',
    '\\uaeff':'8',
    '\\uafbb':'6',
    '\\ubdca':'1',
    '\\ubdcc':'5',
    '\\ubfef':'9',
    '\\uccaa':'2',
    '\\ucfba':'7',
}
fontscn_yx77i032 = {
    '\\uabce':'4',
    '\\uaccd':'6',
    '\\uaeda':'8',
    '\\uaefe':'0',
    '\\uafed':'3',
    '\\ubaaa':'5',
    '\\ubddd':'1',
    '\\ubfad':'2',
    '\\ubfae':'9',
    '\\uc44f':'7',
}


def get_num(s):
    new_s = (list(map(lambda x: x.encode('unicode_escape'), s)))
    result = ''
    ignore_key = ascii_lowercase + ascii_lowercase.upper() + '0123456789' + '.'
    for i in new_s:
        i = i.decode()
        if i in ignore_key:
            result += i
        else:
            for fontsc_data in [fontscn_3jqwe90k, fontscn_h57yip2q, fontscn_qw2f1m1o, fontscn_yuh4hy4p, fontscn_yx77i032]:
                if i in fontsc_data:
                    i = fontsc_data[i]
                    break
            result += i
    return result



if __name__ == '__main__':
    print(get_num('곭w'))

