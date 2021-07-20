"""
    Des：拆分描述符类，验证LineItem 不同的属性
    Date: 2021.07.03
    Author：Laurent Lo
"""

import abc

# 构建基类
class AutoStorage:
    """
    管理托管实例中的储存属性
    """
    __counter = 0
    def __init__(self):
        cls = self.__class__
        cls_name = cls.__name__
        index = cls.__counter
        fmt = "_{}#{}".format(cls_name, index)
        self.storage_name = fmt
        cls.__counter +=1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)



class Validated(AutoStorage):
    def __set__(self, instance, value):
        value = self.validate(value)
        setattr(instance,self.storage_name, value)

    @abc.abstractmethod
    def validate(self, value):
        """return validated value or raise error"""

class Quantity(Validated):
    def validate(self, value):
        if value < 0:
            raise ValueError("value must be > 0")
        else:
            return value

class NoneBlank(Validated):
    def validate(self, value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError("value can not be empty or blank")
        else:
            return value


class LineItem_v5:
    des = NoneBlank()
    weight = Quantity()      # weight.storage = Quantity_v2#0
    price = Quantity()       # weight.storage = Quantity_v2#1

    def __init__(self, des, weight, price):
        self.des = des
        self.weight = weight        # self.__dict__[weight.storage_name] = weight
        self.price = price


    def subtotal(self):
        return self.weight * self.price

line = LineItem_v5('cke', 2.0, 10)
print(line.subtotal())
print(line.weight, line.price)

print(getattr(line, '_Quantity#1'), getattr(line,'_NoneBlank#0'))
