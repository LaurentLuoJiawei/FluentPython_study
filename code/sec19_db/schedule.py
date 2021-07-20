"""
    Des：利用shelve模块调整json数据源的数据结构
    Date: 2021.06.09
    Author：Laurent Lo
"""
"""
1. db 的in 运算符可以查看 db类实例的keys
2. db getitem 返回 record实例
3. record 的实例提供动态属性名访问
"""

import shelve
import json
from urllib.request import urlopen
from collections import abc
import keyword
import os

DB_NAME = './schedule_db'
test_key = 'conference.115'

db = shelve.open(DB_NAME)

def load():
    url = 'http://www.oreilly.com/pub/sc/osconfeed'
    filepath = './osconfeed.json'
    if not os.path.exists(filepath):
        msg = "download from {} to {}".format(url, filepath)
        print(msg)
        with urlopen(url) as remote, open(filepath,'wb') as local:
            local.write(remote.read())

    with open(filepath) as f:
        return json.load(f)

def load_db(db):
    raw_data = load()
    for key, value in raw_data['Schedule'].items():
        name = key[:-1]         # events -> event
        rec_list = value
        for rec in rec_list:
            fmt = '{}.{}'.format(name, rec['serial'])
            rec['serial'] = fmt
            db[fmt] = Record(**rec)




class Record:
    def __init__(self, **kwargs):
        # for k, v in kwargs.items():
        #     if keyword.iskeyword(k):
        #         k += '_'
        #     self.__dict__.update({k:v})
        self.__dict__.update(kwargs)



if __name__ == '__main__':
    db = shelve.open(DB_NAME)
    if test_key not in db:
        load_db(db)
    res = db['event.33451']
    print(res.speakers, res.description)
    db.close()