"""
    Des：构建LineItem
    Date: 2021.06.09
    Author：Laurent Lo
"""
"""
1. 商品具有名称，重量，单价三个属性，
2. 通过计算商品的单价和重量得到总价
"""
class LineItem_v1:
    def __init__(self, des, weight, price):
        self.des = des
        self.weight = weight
        self.price = price

    def subtital(self):
        return self.weight * self.price

# v2 中增加对数量和价格的非负限制
class LineItem_v2:
    def __init__(self, des, weight, price):
        self.des = des
        self.weight = weight
        self.price = price

    # 利用特性实现读值和设值
    def get_weight(self):
        return self.__weight

    @property   # 设置类属性的值读取方法
    def weight(self):
        return self.__weight

    @weight.setter      # 设置类属性的值设置方法
    def weight(self, value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError("value must be > 0")

# line = LineItem_v2('cke', -2.0, 10)
# ValueError: value must be > 0

class Foo:
    """
    特性文档验证
    """
    @property
    def des(self):
        """
        这是一个类的特性文档，
        :return:
        """
        return self.__dict__['des']

    # 类似于java 的属性注入
    @des.setter
    def des(self, value):
        self.__dict__['des'] = value

    def __delattr__(self, item):
        if hasattr(self, item):
            self.__dict__.pop(item)
        else:
            raise

print(Foo.__doc__)      # 存储了类的特性中的文档内容，用于说明操作方法
t1 = set(Foo.__dict__)
del Foo.des

print(set.difference(t1,set(Foo.__dict__)))


