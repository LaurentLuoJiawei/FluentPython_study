"""
    Des：python数据模型测试
    Date: 2021.05.17
"""

import collections

# nametuples 构建只有少量属性但没有方法的对象 -> 数据库条目
Card = collections.namedtuple('Card', ['rank', 'suit'])
class FrenchDeck:
    ranks = [str(n) for n in range(2,11)] + list('JQKA')
    suits = 'spade diamonds clubs hearts'.split()
    def __init__(self):
        self._card = [Card(rank,suit) for rank in self.ranks for suit in self.suits]

    def __len__(self):
        return len(self._card)

    def __getitem__(self, pos):
        # 若getitem 的处理对象为list，则可对类进行index, slice, iter, reverse 操作
        return self._card[pos]

    def __contains__(self, item):
        return item in self._card

deck = FrenchDeck()

# 随机抽取
from random import choice
print(len(deck))
for i in range(3):
    print(choice(deck))


# 切片抽取 将重构getitem方法，将列表操作交给了self._card
print(deck[:3])

# 重载__contains__
print( Card(rank='11', suit='hearts') in deck)

# 给花色suit 赋值进行排序
suit_values = dict(spade=3, hearts=2, diamonds=1, clubs=0)
def spade_high(card: Card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    res = rank_value * len(suit_values) + suit_values[card.suit]
    print(card, rank_value, res)
    return res
# sorted 函数的key 是根据迭代序列中的元素中的某一个值进行排序的。
# spade_high 根据每一个card的 rank和suit计算得到这个card的值，然后进行排序
for i in sorted(deck, key=spade_high):
    print(i)

"""模拟数值类型
1.实现二维计算 加减
2.模计算
3.* 标量计算
"""

from math import hypot

class Vector:
    def __init__(self, x, y):
        self._x = x
        self._y = y
    def __getitem__(self, item):
        return self._x, self._y

    def __repr__(self):
        # 打印实例
        return 'Vecotr(%r, %r)' % (self._x, self._y)

    def __abs__(self):
        return hypot(self._x, self._y)

    def __bool__(self):
        # 如果模为0，则false
        return bool(abs(self))

    def __add__(self, vector):
        x = self._x + vector._x
        y = self._y + vector._y
        return (Vector(x,y))

    def __mul__(self, scalar):
        x = self._x * scalar
        y = self._y * scalar
        return Vector(x,y)

v1 = Vector(3,1)
v2 = Vector(6,8)
print(v1+v2)
print(v1*4)
print(v1)


"""序列构成的数组
"""
# 列表推导
a = 'sbgndsab'
b = [i for i in a if i < 'k']
print(b)
# 使用filter 和 map
c = list(filter(lambda c:c<'k', a))  # 如果要对a的元素进行单独操作，可以在filter 中嵌套 filter(lambda c, condition(c), map(func, a))
print(c == b)

# 利用列表推导实现笛卡尔积：列表中包含可迭代类型元素构成的tuple
sizes = ['s','m','l','xl']
colors = ['red', 'blue', 'green']
dikaer = [(size, color) for size in sizes for color in colors]
print(dikaer)

# 生成器表达
for shirt in ('%s/%s' % (size,color) for size in sizes for color in colors):
    print(shirt)

# slice 构建切片对象
sample = 'sku   coke   $11'
sku = slice(0,3)
name = slice(6,10)
price = slice(13,None)
print(sample[sku], sample[name], sample[price])

# 多维数组切片
import numpy as np
a = np.ones([2,3,4])
print(a)
b = a[...,2]
print(b.shape)

# * + 操作序列
a = [' '] *3
print(a)
b = [[' ']*3]
print(len(b))
c = [[' ']*3] *3
print(c)
c[0][1] = '2'
print(c)
# 三个引用指向同一个列表

d = [['']*3 for i in range(3)]
print(d)
d[0][1] = 3
print(d) #构建三个对象，单独赋值操作

# 使用bisect快速查找列表元素中值插入的位置
import bisect
# 成绩查询
def grade(score, breakpoint= [60,70,80,90], grades= ['E','D','C', 'B', 'A']):
    pos = bisect.bisect_right(breakpoint, score)
    return grades[pos]
print([grade(i) for i in [40,61,60,51,70,1,90,80]])

# 对有序对象进行多次插入
size = 7
import random
my_list = []
for i in range(size):
    item = random.randrange(size*3)
    bisect.insort_left(my_list,item)
    print(my_list)

# 浮点型数组的创建、存入文件和读取
from array import array
from random import random
import time
# floats = array('d', (random() for i in range(10**7)))       # 构建生成器表达式建立双精度浮点数组，类型码'd'
# print(floats[-1])
# t1 = time.time()
# fp = open('', 'wb')
# floats.tofile(fp)       # 直接写入文件
# fp.close()
# print(f"1000万浮点数，写入文件用时：{time.time() - t1}", )
# t1 = time.time()
# with open('', 'w') as f:
#     f.writelines(floats)
# print(f"1000万浮点数以文本形式写入，写入文件用时：{time.time() - t1}", )
#
# t1 = time.time()
# fp = open('','rb')      # 读取1000万个浮点数
# print(f"1000万浮点数，读取文件用时：{time.time() - t1}", )
# with open('', 'rb') as f:
#     data = f.readlines()
# print(f"1000万浮点数以文本形式读取，读取文件用时：{time.time() - t1}", )

# floats.byteswap()
# print(floats[-1])

# 内存视图
numbers = array('h', [-2, -1, 0, 1, 2])
memv = memoryview(numbers)
print(memv)
print(memv[1])
memvoct = memv.cast('B')
print(memvoct.tolist())

# numpy ndarry 的操作
import numpy as np
a = np.arange(12)
print(a)

# dequeue
from collections import deque
dq = deque(range(10), maxlen=10)
print(dq)
for i in range(1,3):
    dq.rotate(i)
    print(dq)

dq.append(11)
print(dq)
dq.append(15)
print(dq)
dq.appendleft(13)
print(dq)
dq.extendleft([20,19,-1])
print(dq)


"""
Section 3
"""
# 字典的构造方式
d = dict(a=1, b=2)
d = {'a':1, 'b':2}
d = dict(zip(['a','b'],[1,2]))
# 字典推导
a = [(11,'china'),(12,'usa')]
b = {num: country for num, country in a}
print(b)
# 直接使用defaultdict，利用default_factory 实现没有键值返回默认值
from collections import defaultdict
# defaultdict.setdefault('key', []).append()
# 继承userdict 构建自定义字典类，设置默认值
from collections import UserDict
"""自定义字典类
1.当key不是字符串时，转换成string再进行索引。
2.当字典没有字符串key，raise keyerror
3.构建字典get方法为调用getitem
4.重载contains方法，对非字符串的key转换成字符串后再进行判断  
"""
class my_class(UserDict):
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __setitem__(self, key, value):
        # 将所有key都提前在赋值的时候转换成字符串
        self.data[str(key)] = value


    def __contains__(self, key):
        return str(key) in self.data.keys()

# 不可变映射类型
from types import MappingProxyType
d = {1:'A'}
d_proxy = MappingProxyType(d) # dproxy 是不可修改的
# d_proxy[2] = 'B'    # d_proxy 的修改只能通过 对d进行修改
d.update({2:'B'})
print(d_proxy)

# 集合推导
from unicodedata import name

# 集合与可迭代对象的操作
a = {1,2,34}
b = {1:'222', 2:'435'}
c = dict(d='sf', k='sdf')
d = a.union(b,c)
print(d)            # {1, 2, 34, 'k', 'd'}
print(type(d))      # <class 'set'>

# 比较字典和set 在键值查找的速度的

"""
1）
构建长度为 1000、1W、10W浮点数的列表 haystack_list
构建键值数量为1000、1W、10W的浮点数字典 haystack_dict
构建元素数量为1000、1W、10W的浮点数集合 haystack_set

2）
随机生成包含1000个浮点数的数组needles

3）
计算在列表中查找相同元素的时间
计算在字典中查找相同元素的时间
计算在集合中查找相同元素的时间

4）
利用集合的比较运算计算查找相同元素的时间

"""
needles = array('d',(random() for i in range(10**3)))
needles_set = set(needles)
def build_hs(num):
    haystack = array('d', (random() for i in range(10**num)))
    hs_list = haystack.tolist()
    hs_dict = {i:' ' for i in haystack}
    hs_set = {i for i in haystack}
    assert isinstance(hs_list, list) and isinstance(hs_dict, dict) and isinstance(hs_set, set)
    return hs_list, hs_dict, hs_set

def count_found(needles, haystack):
    founder = 0
    for i in needles:
        if i in haystack:
            founder += 1
    return founder
def union_found(needles, set):
    found = len(needles & set)
    return found

# 1k 找 1k的时间对比
def get_time(needles, num):
    hs_list, hs_dict, hs_set = build_hs(num)
    time_cost = {}
    t1 = time.time()
    count_found(needles,hs_list)
    time_cost['list'] = time.time() - t1

    t3 = time.time()
    count_found(needles,hs_dict)
    time_cost['dict'] = time.time() - t3

    t5 = time.time()
    count_found(needles,hs_set)
    time_cost['set'] = time.time() - t5

    t7 = time.time()
    union_found(needles_set, hs_set)
    time_cost['union_set'] = time.time() - t7
    print(f"在{10**num}大小的列表中花费时间{time_cost['list']}, "
          f"字典中花费时间{time_cost['dict']}，"
          f"集合遍历查找花费时间{time_cost['set']}，"
          f"集合合并查找花费时间{time_cost['union_set']}")
    print(f'列表/字典：{time_cost["list"]/ time_cost["dict"]}, '
          f'列表/集合 {time_cost["list"]/ time_cost["set"]}, '
          f'字典/集合 {time_cost["dict"]/ time_cost["set"]}, '
          f'遍历/合并{time_cost["set"]/ time_cost["union_set"]}')
    return time_cost

# t1 = get_time(needles, 3)
# t2 = get_time(needles, 4)
# t3 = get_time(needles, 5)
# print(f'列表的查找之间增长系数为{t2["list"] /t1["list"]}, {t3["list"]/ t2["list"]}')
# print(f'字典的查找之间增长系数为{t2["dict"] /t1["dict"]}, {t3["dict"]/ t2["dict"]}')
# print(f'集合的查找之间增长系数为{t2["set"] /t1["set"]}, {t3["set"]/ t2["set"]}')
# print(f'集合的合并操作的增长系数{t2["union_set"]/ t1["union_set"]}, {t3["union_set"]/ t2["union_set"]}')
"""
在1000大小
    列表中花费时间0.010886192321777344, 
    字典中花费时间6.413459777832031e-05，
    集合遍历查找花费时间6.699562072753906e-05，
    集合合并查找花费时间3.409385681152344e-05
    列表/字典：169.73977695167287, 
    列表/集合 162.49110320284697, 
    字典/集合 0.9572953736654805, 
    遍历/合并1.965034965034965

在10000大小
    列表中花费时间0.10844278335571289, 
    字典中花费时间0.000125885009765625，
    集合遍历查找花费时间0.0001442432403564453，
    集合合并查找花费时间4.00543212890625e-05
    列表/字典：861.4431818181819, 
    列表/集合 751.8049586776859, 
    字典/集合 0.8727272727272727, 
    遍历/合并3.6011904761904763

在100000大小
    列表中花费时间1.131382942199707,
    字典中花费时间0.0002880096435546875，
    集合遍历查找花费时间0.00020313262939453125，
    集合合并查找花费时间4.696846008300781e-05
    列表/字典：3928.281456953642, 
    列表/集合 5569.6760563380285, 
    字典/集合 1.4178403755868545, 
    遍历/合并4.324873096446701
    列表的查找之间增长系数为9.961, 10.432994314509214
    字典的查找之间增长系数为1.962825278810409, 2.287878787878788
    集合的查找之间增长系数为2.1530249110320283, 1.4082644628099175
    集合的合并操作的增长系数1.1748251748251748, 1.1726190476190477

"""
# todo 集合合并操作的原因




"""
Section 5
"""
# bytes 对象
a = 'caf¥e'
b = bytes(a, encoding='utf-8')
print(len(a),b, len(b), id(b[:2]))     #5 b'caf\xc2\xa5e' 6 人民币符号无法用ascii 码表示因此使用十六进制转义序列
d = bytearray(b)
print(d[:2], id(d[:2]))     # id(c[:2]) == id(d[:2])

c = memoryview(b)
print(c[:2], id(c[:2]))     #
print(f"b:{id(b)}, c:{id(c)}, d:{id(d)}")
# memoryview 转换成二进制的内存共享

# 缓冲类对象创建bytes 与bytesarry对象的复制操作


# encode编码
cafe = bytes('casge', encoding='utf-8')
print(cafe)
# unicode 规范函数
from unicodedata import normalize
def nfc_equal(str1, str2):
    return normalize('NFC', str1) == normalize('NFD', str2)

# 大小写折叠函数
def fold_equal(str1:str, str2:str):
    return str.casefold(str1) == str.casefold(str2)

# 去除变音符号
import unicodedata
def shace_marks(str1):
    # 将字符串中的组合符号进行拆分，
    norm_txt = normalize('NFD', str1)
    shaved = ''.join(c for c in norm_txt if unicodedata.combining(c))
    return shaved

# 去除属于不是拉丁字母的组合符号
import string
def shave_marks_latin(str2):
    norm_text = normalize('NFD', str2)
    is_latin = False
    shaved_text = []
    for c in norm_text:
        if is_latin and unicodedata.combining(c):
            continue
        shaved_text.append(c)
        if not unicodedata.combining(c):
            is_latin = c in string.ascii_letters
    shaved_text = ''.join(shaved_text)
    return normalize('NFC',shaved_text)

"""
Section 5
"""
# 利用map、filter 完成函数的阶乘
def fact(n):
    return 1 if n<2 else n*fact(n-1)

# 使用列表推到和生成器推到替代 map和filter
res_map = list(map(fact, range(1,5)))
res_map_list = (fact(i) for i in range(1,5))
res_filter = list(map(fact, filter(lambda x:x>4, range(10))))
res_filter_list = (fact(i) for i in range(10) if i >4 )

# 使用sum 替代reduce
from functools import reduce
from operator import add
res_reduce = reduce(add, range(10))
res_reduct_sum = sum(range(10))
print(res_reduce, res_reduct_sum)

# 实现可调用对象
"""
BingoCage 类可以使用任何可迭代的对象构建，并且会在内部存储一个随机顺序排列的列表，调用实例取出一个元素
"""
import random
class BingoCage():
    def __init__(self, iter_obj):
        if hasattr(iter_obj, '__iter__'):
            self._item = list(iter_obj)
            random.shuffle(self._item)
    def catch(self):
        try:
            return self._item.pop()
        except IndexError:
            raise LookupError("类元素列表为空")
    def __call__(self):
        return self.catch()
test = BingoCage([1,2,4,5])
print(test())
# test = BingoCage(())
# print(test())

# 函数内省
# print(dir(fact))
# 比较两个对象的属性
print(set(dir(BingoCage)) - set(dir(fact)))     #{'__weakref__', 'catch'}

def func(q,n=2,*args, key=1, **kwargs):
    pass

func(10,2,'sdf','dfs', key=1, sfd='sf')
# 函数参数打印
from inspect import signature
sig = signature(func)
print('sig:',str(sig))        # 打印参数
for name, param in sig.parameters.items():      #打印参数类型、名称、默认值
    print(param.kind,':',name,':',param.default)
"""
sig: (q, n=2, *args, key=1, **kwargs)
POSITIONAL_OR_KEYWORD : q : <class 'inspect._empty'>
POSITIONAL_OR_KEYWORD : n : 2
VAR_POSITIONAL : args : <class 'inspect._empty'>
KEYWORD_ONLY : key : 1
VAR_KEYWORD : kwargs : <class 'inspect._empty'>
"""


# 使用reduce函数和一个匿名函数计算阶乘
from functools import reduce
def multi(a,b):
    return a*b
res = reduce(multi, range(1,10))        # 自定义乘法函数，利用reduct实现阶乘
res = reduce(lambda x,y: x*y, range(1,10))      # 利用reduct 和 匿名函数计算阶乘
from operator import mul
res = reduce(mul, range(1,10))      # 利用可用于函数式编程的方法实现

# 函数式编程，利用attrgetter和itemgetter 替换lambda 实现对元组元素的获取，对嵌套元组的属性获取
from operator import attrgetter, itemgetter
samples = [('ksk','**&','112'),('sdfas','%$#&','1231'),('kkk','**&','111')]
selector = itemgetter(0,1)
for case in sorted(samples,key=itemgetter(2)):
    print(selector(case))

from collections import namedtuple
samples = [('tokoy','JP',('10','20')),('DC','US',('15','11')),('NYC','US', ('001','10'))]
city = namedtuple('city','name contry index')
index = namedtuple('index','x y')
name_citys = [city(name, contry, index(x,y)) for name, contry, (x,y) in samples]
selector = attrgetter('name','index')
for city in sorted(name_citys, key = itemgetter(0)):
    print(selector(city))

# 冻结参数
from functools import partial
nfc = partial(normalize,'NFC')

# 检查模块中所有成员对象是否是方法
from inspect import getmembers
from inspect import isfunction
# import function_list
function_list = []
funcs = [func for func in getmembers(function_list, isfunction)]        # 从function_list模块中选择所有是函数方法的对象


"""
Section 7
"""
# 闭包
def make_avg():
    series = []
    def avg(new_value):
        series.append(new_value)
        total = sum(series)
        return total/ len(series)
    return avg

# code 属性保存局部变量和自由变量信息
"""
make_avg.__code__.co_varnames       # 内部函数变量审查
make_avg.__code__.co_freevars       # 返回定义函数时的自由变量的绑定
make_avg.__closure__                # 返回cell 对象
make_avg.__closure__[0].cell_contents   #保存自由变量中的值
"""
# clock 装饰器
def clock(func):
    def clocker(*args):
        t1 = time.perf_counter()
        res = func(*args)
        t2 = time.perf_counter() 
        name = func.__name__
        arg_str = ",".join([repr(arg) for arg in args])
        print("[%0.8fs] %s( %s ) -> %r" % (t2-t1, name , arg_str, res))
        return res
    return clocker
@clock
def snooze(seconds):
    time.sleep(seconds)

@clock
def factorial(n):
    return 1 if n<2 else n*factorial(n-1)

print("*"*20, 'Calling snooze(.123)')
snooze(.123)
print("*"*20, 'Calling factorial(6)')
print("6! = ", factorial(6))

# 单分派泛函数
"""
通过分派函数，实现对不同数据类型的处理
"""
from functools import singledispatch
from collections import abc
from typing import Text, MutableMapping, Sequence
import html
import numbers

@singledispatch
def htmlize(obj):
    content = html.escape(obj)
    return "<pre> {} </pre>".format(content)

@htmlize.register(Text)
def _(text):
    content = html.escape(text).replace('\n','</br>\n')
    return "<p>{0}<\p>".format(content)

@htmlize.register(numbers.Integral)
def _(n):
    """转换成十进制和十六进制"""
    return "<pre>{0} (0x{0:x})</pre>"

# @htmlize.register(Sequence)
# @htmlize.register(MutableMapping)
# def _(seq):
#     inner = "</i>\n</i>".join([html.escape(item) for item in seq])
#     return "<ul>\n<li>" + inner + "</li>\n</ul>"

# 浅复制
"""
对嵌套列表做浅复制
"""
l1 = [3, [66, 55, 44], (7, 8, 9)]
l2 = list(l1)
print(l1 is l2)
print(l2 == l2)
l1.append(100)
l1[1].remove(55)
print("l1", l1)
print("l2", l2)
l2[1] += [33, 22]
l2[2] += (10,11)
print("l1",l1)
print("l2",l2)
"""浅复制
l1 [3, [66, 44], (7, 8, 9), 100]    #
l2 [3, [66, 44], (7, 8, 9)]
l1 [3, [66, 44, 33, 22], (7, 8, 9), 100]    # 删除l2中的55也被删除，因为l2 索引的list 与 l1 相同
l2 [3, [66, 44, 33, 22], (7, 8, 9, 10, 11)]     # 对于tuple 的增量赋值，等于重新创建了一个新的tuple 并将引用存到了l2[-1]，对l1没有影响
"""


# 对任意对象做深复制和浅复制
"""bus乘客在途中上下车

"""
import copy
class Bus:
    def __init__(self, passenger=None):
        if passenger is None:
            self.passenger = []
        else:
            self.passenger = list(passenger)

    def pick(self, name):
        self.passenger.append(name)

    def drop(self, name):
        self.passenger.remove(name)
bs1 = Bus(['1','2','3','4'])
bs2 = copy.copy(bs1)
bs3 = copy.deepcopy(bs2)
bs1.drop('2')
print(bs2.passenger, bs3.passenger, id(bs1.passenger), id(bs2.passenger))

"""使用可变类型作为参数默认值
"""
class WrongBus(Bus):
    def __init__(self, passenger=[]):
        self.passenger = passenger

p = ['1','3','4']
wrongbus1 = WrongBus()
wrongbus1.pick('6')
print(wrongbus1.passenger)
wrongbus2 = WrongBus()
wrongbus2.pick('19')
print(wrongbus2.passenger)        #['6', '19']
"""
# bus1 与bus 2 在初始化时，使用了默认值
导致两个bus 的 passenger 引用了同一个list，self.passenger 成为了passenger->list 的别名

"""

"""
section 9
"""

# 使用reduce 实现累计异或
def iter_xor():
    n = 0
    for i in range(6):
        n ^= i
    return n

from functools import reduce
def lamb_xor():
    return reduce(lambda x,y : x^y, range(6))

from operator import xor
def operator_xor():
    return reduce(xor, range(6))

"""
section 11
"""
# 调用collection模块内置类型的方法， 解决普通内置类型（dict，list，str）的方法委托问题（内置类型方法不调用子类化覆盖方法）

from collections import UserDict, UserList, UserString

class DoubltDict(UserDict):
    def __setitem__(self, key, value):
        super(DoubltDict, self).__setitem__(key, [value]*2)

dd = DoubltDict(one=2)
print(dd)

# 多重继承：菱形问题
class A:
    def ping(self):
        print("APing")

class B(A):
    def pong(self):
        print("BPong")
class C(A):
    def pong(self):
        print("CPong")

class D(B,C):       #继承定义顺序决定了方法解析顺序，先B再C
    def ping(self):
        A.ping(self)
        print("DPing")
    def pingpong(self):
        self.ping()
        super().ping()
        self.pong()
        super().pong()
        C.ping(self)
# print(D.__mro__)
d = D()
print(d.pong())         # BPong  D中没有实现pong 方法，根据mro 的解析顺序显示，调用了父类B的pong方法
print(d.ping())         # APing  显式调用超类A，
print(d.pingpong())

"""
APing   运行D类ping 方法
DPing
APing   super 委托超类A的ping方法
BPong   按解析顺序运行B的pong 方法
BPong   super 委托超类B运行pong方法
APing   显式将ping方法委托给C进行调用（忽略mro 方法解析顺序）
"""
import io
# 打印类的方法解析顺序
def print_mor(cls):
    print( ",".join([c.__name__ for c in cls.__mro__]))
print_mor(bool)     # bool,int,object
print_mor(numbers.Integral)     # Integral,Rational,Real,Complex,Number,object
# base结尾的为抽象基类，open函数返回对象属于这些类型
print_mor(io.BytesIO)       # BytesIO,_BufferedIOBase,_IOBase,object
print_mor(io.TextIOWrapper)         # TextIOWrapper,_TextIOBase,_IOBase,object

"""
section 13
"""
import abc
import random
from typing import Sequence
class Tombola(abc.ABC):
    @abc.abstractmethod
    def load(self):
        """
        将元素放入容器
        :return:
        """

    @abc.abstractmethod
    def pick(self):
        """
        从容器中随机取出一个元素，返回选中元素
        :return:
        """

    def loaded(self):
        pass

    def inspect(self):
        if self.loaded():
            return sorted(self)

class Bingo(Tombola):
    def __init__(self, components):
        self._components = list(components)
        self._ran = random.shuffle

    def __iter__(self):
        return iter(self._components)

    def load(self, items):
        self._components.extend(items)
        self._ran(self._components)

    def pick(self):
        try:
            return self._components.pop()
        except IndexError:
            raise LookupError("pick from empty Bingocage")

    def __call__(self):
        return self.pick()

    def loaded(self):
        return bool(self._components)

    def __str__(self):
        return str(tuple(self._components))



a = Bingo(['a','b','c'])
print(a)
a.load(('u','z'))
print(a)
print(a.pick())
print(a)
print(len(a.inspect()))

class AddableBingo(Bingo):
    def __add__(self, other):
        if isinstance(other, Tombola):
            return AddableBingo(self.inspect() + other.inspect())
        else:
            return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, Tombola):
            items = other.inspect()
        else:
            try:
                items = iter(other)
            except TypeError:
                self_cls = type(self).__name__
                msg = "right operand in += must be {!r} or an iterable"
                raise TypeError(msg.format(self_cls))
        self.load(items)
        return self

ad = AddableBingo(('c','v','k'))
ac = AddableBingo(('1','5','0'))
print(ad.inspect())
test1 = ['1','2','4']
test2 = ('s','2',2)
ad_org = ad
print(id(ad_org))
ae = ad + ac            # 实现同类型相加
print(ae ,id(ae))       # 生成新对象
ad += test1             # 实现对可迭代元素的增量赋值
print(ad,id(ad))        # 就地相加，地址不变

"""
section 14
"""

# 可迭代对象

# 迭代器

# 生成器对象

# 生成器表达式：for 循环时 定义体才会真正执行

"""等差数列生成器
等差数列中，数字类型与start 或者 step 一致，利用强制类型转换
"""
class ArithmeticProgression:
    def __init__(self, start, step, stop=None):
        self.start = start
        self.step = step
        self.stop = stop

    # def __iter__(self):
    #     return (i for i in range(self.start, self.stop, self.step))

    def __iter__(self):
        result = type(self.start + self.step)(self.start)
        forever = self.stop is None
        index = 0
        while forever or result < self.stop:
            yield result
            index += 1
            result = self.start + self.step* index

from fractions import Fraction
from decimal import Decimal
ap1 = ArithmeticProgression(0, 2, 5)
ap2 = ArithmeticProgression(0, .1, .4)        # 浮点数累计可能有致错风险
ap3 = ArithmeticProgression(0, 1/3, 1)
ap4 = ArithmeticProgression(0,Fraction(2,7),2)
ap5 = ArithmeticProgression(0, Decimal('.5'), .7)
# print(list(ap1), list(ap2), list(ap3), list(ap4) , list(ap5))
# print(type(1+.5))
# print(type(Decimal('.2')+1))
# print(type(Fraction(1,3)+0))

# 构建生成器方法
def ariprog_gen(begin, step, stop=None):
    index = 0
    forever = stop is None
    result = type(begin + step)(begin)
    while result < stop or forever:
        yield result
        index += 1
        result = begin + step*index
for i in ariprog_gen(0, Fraction(1,12), 1/2):
    print(i)

# 引入iterools 模块
import itertools

def ariprog_gen_v2(begin, step, stop=None):
    first = type(begin + step)(begin)
    gen = itertools.count(first, step)          # 保证等差数列的类型与begin 或 step 一致
    if stop is not None:
        ap_gen = itertools.takewhile(lambda x: x < stop, gen)
    return ap_gen

"""
senction 17 
"""


"""复用不定长的平均数方法
实现客户端、委派生成器、子生成器模式
"""

def average_v1():
    # 利用闭包实现不定长列表求平均
    total = 0
    turn = 0
    def avg(item):
        nonlocal total, turn
        total += item
        turn += 1
        return total/turn
    return avg

# a = average_v1()

Reuslt = namedtuple('Result',"turn avg")
def average_v2():
    # 构建子生成器
    total = 0
    turn = 0
    avg = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        turn += 1
        avg = total / turn
    return Reuslt(turn, avg)

def grouper(results, key):
    # 构建生成器委派器协程
    while True:
        results[key] = yield from average_v2()

def report(data):
    """
    打印结果
    :param data:
    :return:
    """
    fmt = "total: {} , key {}, average: {:.2f}"
    return  (fmt.format(v[0], k, v[1]) for k,v in data.items())


def client(data):
    """构建客户端
    对数据的平均统计
    :return:
    """
    results = {}        #创建空字典用于协议结果传递
    for key, values in data.items():
        group = grouper(results, key)
        next(group)         # 协程预激
        for value in values:
            group.send(value)
        group.send(None)
    print(results)
    return report(results)


samples = {
    "girls;kg":[1,2,4,5],
    "girls:height":[1.1,1.2,1.4,1.5]
}

# a = client(samples)
# print(list(a))

"""
section 17
"""

# THreadPoolExecutor
from time import sleep, strftime
from concurrent import futures

def display(*args):
    # print(strftime("%H:%M:%s"))
    print(strftime("[%H:%M:%S]"),end=' ')
    print(*args)

def loiter(n):
    msg = "{} loiter ({}) : doing noting for {} s..."
    display(msg.format('\t'*n, n, n))
    sleep(n)
    msg = "{} loiter ({}) ：done"
    display(msg.format('\t'*n, n))
    return n*10

def run():
    display("Script staring")
    # executor = futures.ProcessPoolExecutor(max_workers=4)
    executor = futures.ThreadPoolExecutor(max_workers=3)
    res = executor.map(loiter, range(5))
    display("result:", res)     # result: <generator object _chain_from_iterable_of_lists at 0x7fd024b3e990>
    display("play individual result")
    for i, r in enumerate(res):
        msg = "index : {}, result: {}"
        display(msg.format(i,r))
    display("Script end...")


# run()
"""
[23:07:28] Script staring
[23:07:28]  loiter (0) : doing noting for 0 s...
[23:07:28]  loiter (0) ：done
[23:07:28] 	 loiter (1) : doing noting for 1 s...
[23:07:28] 		 loiter (2) : doing noting for 2 s...
[23:07:28] result: <generator object Executor.map.<locals>.result_iterator at 0x7fae63360a40>
[23:07:28] play individual result
[23:07:28] index : 0, result: 0
[23:07:28] 			 loiter (3) : doing noting for 3 s...
[23:07:29] 	 loiter (1) ：done
[23:07:29] 				 loiter (4) : doing noting for 4 s...
[23:07:29] index : 1, result: 10
[23:07:30] 		 loiter (2) ：done
[23:07:30] index : 2, result: 20
[23:07:31] 			 loiter (3) ：done
[23:07:31] index : 3, result: 30
[23:07:33] 				 loiter (4) ：done
[23:07:33] index : 4, result: 40
[23:07:33] Script end...
"""

"""
sec 19 
"""
from collections import abc

# 将jso对象转换成能FrozenJSON对象
"""
处理Json数据格式中，嵌套字典和嵌套列表
FronzonJSON 对象
1. 保存整体json数据到实例属性中
2. 利用key在实例查找时候，调用类方法即时对json结果进行实例化
"""
from collections import abc
from urllib.request import urlopen
import os
import json
import keyword


class FrozenJSON():
    def __init__(self, data):
        # 修改与属性名冲突的key
        self._data = {}
        for key, value in data.items():
            if keyword.iskeyword(key):
                key  += '_'
            self._data[key] = value


    def __getattr__(self, item):
        if hasattr(self._data, item):
            # key 调用
            return getattr(self._data, item)
        else:
            # 当key 不存在时，获取item对应的元素
            return FrozenJSON.build(self._data[item])

    @classmethod
    def build(cls, obj):
        if isinstance(cls, abc.MutableMapping):
            # 处理字典
            return cls(obj)
        elif isinstance(cls, abc.MutableSequence):
            # 处理list嵌套字典
            return [cls.build(i) for i in obj]
        else:
            return obj

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
res_json = load()
res = FrozenJSON(res_json)
print(res.Schedule.keys())
for k, v in res.Schedule.items():
    msg ="{} : {}".format(len(k), k)
    print(msg)

"""
利用new 方法替换类方法
"""

class FrozenJSON_v2():
    """
    利用new 类方法实现build 类方法
    """
    def __new__(cls, arg):
        if isinstance(arg, abc.MutableMapping):
            return super().__new__(cls)     # 返回实例
        elif isinstance(arg, abc.MutableSequence):
            return [cls(i) for i in arg]        # 返回嵌套实例的list
        else:
            return arg      # 不返回实例

    def __init__(self, data):
        # 修改与属性名冲突的key
        self._data = {}
        for key, value in data.items():
            if keyword.iskeyword(key):
                key  += '_'
            self._data[key] = value


    def __getattr__(self, item):
        if hasattr(self._data, item):
            # key 调用
            return getattr(self._data, item)
        else:
            # 当key 不存在时，获取item对应的元素
            return FrozenJSON.build(self._data[item])

# res_json = load()
# res = FrozenJSON_v2(res_json)
# print(res.Schedule.keys())
# for k, v in res.Schedule.items():
#     msg ="{} : {}".format(len(k), k)
#     print(msg)


"""
sction 21
"""
from itertools import product