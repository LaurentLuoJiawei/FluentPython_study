"""
    Des：重载类的内置方法实现vector
    Date: 2021.06.09
    Author：Laurent Lo
"""
from math import hypot
import array
import reprlib
import numbers
from operator import xor
from functools import reduce
"""
1。接受可迭代参数
2。序列协议，支持切片
"""
class Vector:
    typecode = 'd'
    attrs = 'xyz'
    def __init__(self, components):
        self._components = array.array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __str__(self):
        return str(tuple(self))

    def __repr__(self):
        cls = type(self)
        name  = cls.__name__
        fmt = '{}:({})'
        # content = repr(list(self._components))
        content = reprlib.repr(self._components)
        content = content[content.find('['):-1]
        return fmt.format(name, content)

    @classmethod
    def frombytes(cls, octects):
        typecode = chr(octects[0])
        memv = memoryview(octects[1:]).cast(typecode)
        return cls(memv)        # 支持可迭代参数输入

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        """序列协议
        利用slice 属性
        :param index:
        :return:
        """
        cls = type(self)
        if isinstance(index, slice):        # 长度为1的切片也会创建实例
            return cls(self._components[index])
        elif isinstance(index, numbers.Integral):       # 类型判断时候使用基类
            return self._components[index]
        else:
            msg = '{cls.__name__} indices must be intergers'
            raise TypeError(msg.format(cls=cls))
    def __setattr__(self, key, value):
        cls = type(self)
        if len(key) == 1:       # 处理对实例属性xyz赋值行为的异常
            if key in cls.attrs:
                error = 'readonly attribute {attrs_name!r}'
            elif key.islower():
                error = "can't set attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ''
            if error:
                msg = error.format(cls_name = cls.__name__, attrs_name = key)
                raise  AttributeError(msg)

        super(Vector, self).__setattr__(key, value)         # 除了上述情况，其他时候默认调用超类setattr方法，提供标准行为
    def __hash__(self):

        # hash_list = (hash(c) for c in self._components)     # 构建生成器表达式，惰性计算分量哈希值
        hash_list = map(hash, self._components)     # 构建生成器表达式，惰性计算分量哈希值
        return reduce(xor, hash_list, 0)       # 计算聚合的异或散列值，并设置初始化值为0，用于处理空序列的情况。针对 *= 应设置为1， 对 +、- 应设置为 0

    def __eq__(self, other):
        return len(self) == len(other) and all( a == b for a,b in zip(self, other))
"""
1.通过类的属性访问类的分量
2.类对象可以拆包变成元组（iter）
* 打印类构造方法（repr）
* 类的比较（eq）
* 类的打印（str，format）
* 类的强制类型转换 （bytes, frombytes）
* 类的可散列(hash, @property, eq)
"""

class Vector2D:
    typecode = 'd'      # 设置不同的字节序列编码方法
    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

    def __iter__(self):
        return (i for i in (self.__x, self.__y))

    @property
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y

    def __repr__(self):
        typename = type(self).__name__
        output_fmt = '{}({!r},{!r})'
        return output_fmt.format(typename,*self)

    def __str__(self):
        return str(tuple(self))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __abs__(self):
        return hypot(*self)

    def __bool__(self):
        return bool(abs(self))

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)       # 混合分量的散列值

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(array.array(self.typecode, self)))


    def __format__(self, format_spec:str =''):
        fmt = "<{},{}>"
        if format_spec.endswith('p'):
            print("xxx")
        else:
            components = (format(c, format_spec) for c in self)
            return fmt.format(*components)

    @classmethod
    def frombytes(cls, octes):
        typecode = chr(octes[0])
        memv = memoryview(octes[1:]).cast(typecode)
        return cls(*memv)



def main():
    v1 = Vector2D(3,4)
    print(repr(v1))
    print(v1)
    v1_clone = eval(repr(v1))
    print(v1_clone == v1)
    octes = bytes(v1)
    print(octes)
    print(Vector2D.frombytes(bytes(v1)))
    print(abs(v1))
    print(bool(v1), bool(Vector2D(0,0)))
    print(format(v1, '0.2f'))
    v2 = Vector([1,2,4,5])
    print(v2)
    print(repr(v2))
    print(v2[1:3])

if __name__ == '__main__':
    main()

