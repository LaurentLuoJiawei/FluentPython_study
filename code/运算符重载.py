"""
    Des：python数据模型测试
    Date: 2021.05.17
"""
import array
import math
class Vector:
    typecode = 'd'
    def __init__(self, components):
        self._components = array.array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __len__(self):
        return len(self._components)

    def __str__(self):
        return str(tuple(self))

    def __eq__(self, other):
        # 引入notimplemented 异常用于类型检查
        if isinstance(other, Vector):
            return True if len(self) == len(other) and all(x == y for x in self for y in other) else False
        else:
            raise NotImplemented        # 调用后备机制尝试 other.eq(self)
        # return True if len(self) == len(other) and all(x == y for x in self for y in other) else False

    # 一元运算符对应的特殊方法
    def __pos__(self):
        return Vector(self)

    def __neg__(self):
        return Vector(-x for x in self)

    def __abs__(self):
        return math.sqrt(sum( i*i for i in self))

    """
    安全重载标量加法
    1。实现长度不同的向量相加
    2。实现非向量可迭代对象相加
    """
    def __add__(self, other):
        pass

    # 后备机制
    def __radd__(self, other):
        pass
    # 就地方法
    def __iadd__(self, other):
        pass
    """
    安全重载标量乘法
    1. 实现向量与标量乘法
    2. 实现多种标量数据类型的乘法
    """

    # 重载点积运算符号@
    def __matmul__(self, other):
        pass

    def __rmatmul__(self, other):
        pass



# 安全重载 + 向量加法运算符

#