"""
    Des：构建LineItem
    Date: 2021.06.09
    Author：Laurent Lo
"""
"""
1. 商品具有名称，重量，单价三个属性，
2. 通过计算商品的单价和重量得到总价
"""
def prop_factory(name):

    def get_pro(instance):
        return instance.__dict__[name]

    def set_pro(instance, value):
        if value > 0:
            instance.__dict__[name] = value

        else:
            raise ValueError("{} must be set > 0".format(instance.__dict__[name]))

    return property(fget=get_pro, fset=set_pro)


# v2 中增加对数量和价格的非负限制
class LineItem_v3:
    weight = prop_factory('weight')
    price = prop_factory('price')
    def __init__(self, des, weight, price):
        self.des = des
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

line = LineItem_v3('cke', 2.0, 10)
print(line.subtotal())

line = LineItem_v3('milk',-10,-0.2)
"""
raise ValueError("{} must be set > 0".format(instance.__dict__[name]))
KeyError: 'weight'

"""