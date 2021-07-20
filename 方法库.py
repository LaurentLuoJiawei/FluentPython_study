"""

    Des：工具函数总结
    Date: 2021.05.17

"""

# 从有序列表中插入值

# 自定义字典对象

# 自定义方法对象

# 打印检查类的属性列表

# 打印检查方法的参数列表
def func(q,n=2,*args, key=1, **kwargs):
    pass
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
# 函数内省：检查函数内部的函数以及自由变量（闭包）

# 文本规范化与大小写折叠（利用partial进行优化）
import unicodedata
from functools import partial
nfc = partial(unicodedata.normalize, 'NFC')
print(nfc, nfc.func, nfc('sdfsjkf'))
# 字典创建

# filter、map、reduce 的替代方法

# 函数式编程，利用attrgetter和itemgetter 替换lambda 实现对元组元素的获取，对嵌套元组的属性获取

# 审查函数的变量

# 内存检查

# 有限等差数列

# future 模块 线程、进程 调用范式

# HTTP客户端异常处理：分层

# HTTP 请求限流

# 自定义异常类，为异常添加程序结果相关数据；并链接原先异常；当原来异常找不到错误消息，使用所链接异常作为错误消息

# 同时读取和保存远程文件
def load(url, filepath):
    pass

# 判断有效标识符有效

# Json数据类型中嵌套字典和嵌套列表处理，转换成嵌套的自定义类和列表/ 抽象成工厂函数

#

# 动态获取关键字初始化类（利用实例dict 属性）

# 属性表示法

# 动态生成类