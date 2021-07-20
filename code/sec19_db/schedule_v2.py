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
import inspect
from collections import abc
import keyword
import os

DB_NAME = './schedule_v2_db'
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
    for key, rec_list in raw_data['Schedule'].items():
        name = key[:-1]         # events -> event
        cls_name = name.capitalize()
        cls = globals().get(cls_name, DbRecord)
        if inspect.isclass(cls) and issubclass(cls, DbRecord):
            factory = cls
        else:
            factory = DbRecord      # event.venue 返回 DbRecord 类

        for rec in rec_list:
            key = '{}.{}'.format(name, rec['serial'])
            rec['serial'] = key
            db[key] = factory(**rec)        # 使用factory 构建存储在数据库中的对象




class Record:
    def __init__(self, **kwargs):       # 实例动态属性构建和访问
        self.__dict__.update(kwargs)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.__dict__ == other.__dict__
        return NotImplemented

class DbRecord(Record):
    __db = None

    @classmethod
    def fetch(cls, key):
        db = cls.__db
        try:
            return db[key]
        except TypeError:
            if db is None:
                msg = "databases not set; call '{}.set_db(my_db)' "
                raise MissingDatabaseError(msg.format(cls.__name__))
            else:
                raise   # 抛出其他异常

    @staticmethod
    def set_db(db):
        DbRecord.__db = db

    @staticmethod
    def get_db():
        return DbRecord.__db        # 确保继承后的子类仍返回类数据库的引用
    def __repr__(self):
        if hasattr(self, 'serial'):
            cls_name = self.__class__.__name__
            return ' <{} serial = {!r}>'.format(cls_name, self.serial)
        else:
            return super().__repr__()

class Event(DbRecord):
    """
    1. DbRecord 类通过serial number 返回event 类实例
    2. Event 类实例的固定格式打印 repr
    3. Event 具有venue 属性 返回 DbRecord 实例及 venue serial
    4. Event 具有speakers 属性，存储speker serial 和 speaker name
    """
    @property
    def venue(self):
        key = 'venue.{}'.format(self.venue_serial)
        return self.__class__.fetch(key)

    @property
    def speakers(self):
        if not hasattr(self, '_speaker_objs'):
            spkr_serials = self.__dict__['speakers']
            fetch = self.__class__.fetch
            self._speaker_objs = [fetch('speaker.{}'.format(key)) for key in spkr_serials]
        return self._speaker_objs

    def __repr__(self):
        if hasattr(self, 'name'):       # speaker_obj 和 event 都有名称
            cls_name = self.__class__.__name__
            return '<{} {!r}>'.format(cls_name, self.name)

        else:
            return super.__repr__()

class MissingDatabaseError(RuntimeError):
    """
    需要数据库但没有指定数据库时抛出
    """

if __name__ == '__main__':
    db = shelve.open(DB_NAME)
    if test_key not in db:
        load_db(db)
    DbRecord.set_db(db)
    event = DbRecord.fetch('event.33463')
    print(event)
    print(event.venue)
    print(event.venue.name)
    for spkr in event.speakers:
        fmt = '{} : {}'
        print(fmt.format(spkr.serial, spkr.name))
    db.close()