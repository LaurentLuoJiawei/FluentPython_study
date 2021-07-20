"""
    Des：利用属性描述符构建LineItem
    Date: 2021.06.09
    Author：Laurent Lo
"""
"""
1. 商品具有名称，重量，单价三个属性，
2. 通过计算商品的单价和重量得到总价
"""
class Quality:
    """
    描述符类
    """

    def __init__(self, storage_name):
        self.storage_name = storage_name

    def __set__(self, instance, value):
        if value > 0:
            instance.__dict__[self.storage_name] = value

        else:
            raise ValueError("{!r}'s {!r} must be > 0 ".format(self.storage_name, 'valye'))



"""
1. 将描述符类作为类属性，添加到托管类LineItem中
2. 实例化对象中保存由描述符类处理后的存储属性 obj.__dict__[storage_name]
"""
class LineItem_v4:
    weight = Quality('weight')
    price = Quality('price')

    def __init__(self, des, weight, price):
        self.des = des
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

line = LineItem_v4('cke', 2.0, 10)
print(line.subtotal())

"""
raise ValueError("{} must be set > 0".format(instance.__dict__[name]))
KeyError: 'weight'

"""


# 自动获取储存属性的名称
class Quantity_v2:
    __index = 0
    def __init__(self):
        cls_name = self.__class__.__name__
        index = Quantity_v2.__index
        # 利用描述类属性 index ，为每一个实例赋一个ID，保存在 self.storage_name 中
        fmt = '_{}#{}'.format(cls_name, index)
        print(fmt)
        self.storage_name = fmt
        Quantity_v2.__index +=1


    def __get__(self, instance, owner):
        """
        self 是描述符实例
        :param instance: 托管类实例
        :param owner: 托管类的索引，用于获取类属性
        :return:
        """
        if instance is None:
            """
            未实例化直接访问类属性(cls.weight) 会抛出异常，因此直接返回描述符实例
            """
            return self
        else:
            return getattr(instance, self.storage_name)     # return instance.__dict__[self.storage_name] = item


    def __set__(self, instance, item):
        # 在托管实例中构建字典存储属性， key = 描述实例的ID（price.storage_name），instance.__dict__[self.storage_name] = item
        if item > 0:
            setattr(instance, self.storage_name, item)
        else:
            raise ValueError("value must be > 0")


class LineItem_v5:
    weight = Quantity_v2()      # weight.storage = Quantity_v2#0
    price = Quantity_v2()       # weight.storage = Quantity_v2#1

    def __init__(self, des, weight, price):
        self.des = des
        self.weight = weight        # self.__dict__[weight.storage_name] = weight
        self.price = price


    def subtotal(self):
        return self.weight * self.price

line = LineItem_v5('cke', 2.0, 10)
print(line.subtotal())
print(line.weight, line.price)

print(getattr(line, '_Quantity_v2#0'))
