"""
    Des：python实现策略设计模式
    Date: 2021.05.17
"""

"""电商策略
针对订单，支持插入式折扣策略
"""
from abc import ABC, abstractmethod
from collections import namedtuple

Customer = namedtuple('customer', 'name credits')


class Product:
    def __init__(self, sku, quality, price):
        self.sku = sku
        self.quality = quality
        self.price = price

    def total(self):
        return self.quality * self.price

class Order:
    """订单类

    """
    def __init__(self, customer: Customer, cart, promotion = None):
        self.customer = customer
        self.cart = cart if cart else []
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '_total'):
            self._total = sum(product.total() for product in self.cart)

        return self._total

    def get_due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount

    def update_cart(self, product):
        self.cart.append(product)

    def __repr__(self):
        fmt = '<Order : customer:{} /total:{:.2f} / due:{:.2f} >'
        return fmt.format(self.customer.name, self.total(), self.get_due())

# 策略：抽象基类
class Promotion(ABC):

    @abstractmethod
    def discount(self, order):
        pass

class FidelityPromo(Promotion):
    """
    为满足积分要求的顾客提供折扣
    """
    def discount(self, order):
        return order.total() * .05 if order.customer.credits >1000 else 0

class BulkItemPromo(Promotion):
    """
    订单中单个商品数量达到20个及以上的提供10%折扣
    """
    def discount(self, order):
        has_discount = False
        for product in order.cart:
            if product.quality >= 20:
                has_discount = True
        return order.total() * 0.1 if has_discount else 0

class LargeOrderPromo(Promotion):
    """
    订单种不同商品达到10个或以上提供7%折扣
    """
    def discount(self, order):
        distinct_items = {product for product in order.cart}
        return order.total() * .07 if len(distinct_items) >= 10 else 0


# 构建测试用例
jack = Customer('jack',1500)
fideity_cart = [Product('milk', 10, .5), Product('coke', 8, 2), Product('orange', 14, 3)]
print(Order(jack, fideity_cart, FidelityPromo()))
lucy = Customer('lucy',100)
bulk_cart = [Product('milk', 12, .5), Product('coke', 30, 2), Product('orange', 14, 3)]
print(Order(lucy, bulk_cart, BulkItemPromo()))
Bob = Customer('bob', 300)
large_cart = [Product(str(i), i, i*0.5)for i in range(15)]
print(Order(Bob, large_cart, LargeOrderPromo()))


"""将函数作为对象简化策略模式
原始策略模式，会在每一个新的上下文中使用相同策略时不断创建具体策略对象，增加开销。
因此对于具体处理数据的策略，可以尝试使用函数替代类，避免编写只有一个类的方法，然后在另一个类实现调用这个单类的接口
引入方法对象，实现方法的共享，因此不必在上下文中不断创建新的具体对象策略。
"""
from typing import Callable
class Order_v2:
    def __init__(self, customer, cart, promotion: Callable):
        self.cutomer = customer
        self.cart = cart if cart else []
        self.promotion = promotion

    def total(self):
        if hasattr(self, '_total'):
            self._total = sum(product.total() for product in self.cart)
        return self._total
    def due(self):
        if self.promotion is not None:
            discount = self.promotion(self)
        else:
            discount = 0
        return self.total() - discount

def fidelitypromo(order):
    return order.total() * .05 if order.customer.credits >1000 else 0

def bulkitempromo(order):
    has_discount = False
    for product in order.cart:
        if product.quality >= 20:
            has_discount = True
    return order.total() * 0.1 if has_discount else 0

def largerorderpromo(order):
    distinct_items = {product for product in order.cart}
    return order.total() * .07 if len(distinct_items) >= 10 else 0

# 利用内省函数，对比所有策略的折扣，选择折扣最大的策略并输出
import inspect
# inspect.getmembers(module_name, inspect.isfunction)


# 利用装饰器重构策略
promos = []
def promo(func):
    promos.append(func)
    return func
@promo
def fidelitypromo(order):
    return order.total() * .05 if order.customer.credits >1000 else 0
@promo
def bulkitempromo(order):
    has_discount = False
    for product in order.cart:
        if product.quality >= 20:
            has_discount = True
    return order.total() * 0.1 if has_discount else 0
@promo
def largerorderpromo(order):
    distinct_items = {product for product in order.cart}
    return order.total() * .07 if len(distinct_items) >= 10 else 0

def best_prom(order):
    return max( pro(order) for pro in promos)
