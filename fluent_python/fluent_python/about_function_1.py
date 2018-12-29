# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :2018/12/5 13:37
# @Author   :zhong
# @Software :PyCharm
from abc import ABC, abstractmethod
from collections import namedtuple

# 顾客 -> 记录名字和积分
Customer = namedtuple('Customer', 'name, fidelity')


class LineItem:

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


# 上下文
class Order:

    def __init__(self, customer, cart, promotion=None):
        self.customer = customer    # Customer 对象
        self.cart = cart    # list
        self.promotion = promotion  # 策略

    def total(self):
        # hasattr 判断对象是否含有某属性
        if not hasattr(self, '__total'):
            self.__total = sum(item.total for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            # discount = self.promotion.discount(self)  # 以类为基准
            discount = self.promotion(self) # 以函数为基准
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())


class Promotion(ABC):

    @abstractmethod
    def discount(self, order):
        """"返回折扣金额（正职）"""


class FidelityPromo(Promotion):
    """为积分为1000或者以上的客户提供5%的折扣"""

    def discount(self, order):
        return order.total() * .05 if order.customer.fidelity >= 1000 else 0


class BulkItemPromo(Promotion):
    """单个商品为20个或以上提供10%折扣"""

    def discount(self, order):
        discount = 0
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * .1
        return discount


class LargeOrderPromo(Promotion):
    """订单中的不同商品达到10个或以上时提供7%折扣"""

    def discount(self, order):
        distinct_items = {item.prodcut for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * .07
        return 0

# -----------------------------------------------------------------------
# 函数替代
def fidelity_promo(order):
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0


def bulk_item_promo(order):
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount


def large_order_promo(order):
    distinct_items = {item.prodcut for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * .07
    return 0
# ---------------------------------------------------------------------------

# 最佳优惠方式
def best_promo(order):
    import inspect

    """选择可用的最佳折扣"""
    promos = [fidelity_promo, bulk_item_promo, large_order_promo]
    # 自动找出全局模块 (相同结尾)
    promos_ = [globals()[name] for name in globals() if name.endswith('_promo') and name != 'best_promo']

    return max(promo(order) for promo in promos)

# ----------------------------------------------------------------------------------------------------------------------
# 装饰器的方式来解决最佳优惠方式 (不相同结尾的方式)

promos = []

def promotion(promos_func):
    promos.append(promos_func)
    return promos_func

@promotion
def new_fidelity(order):
    pass
# ----------------------------------------------------------------------------------------------------------------------
# 变量作用域规则



if __name__ == '__main__':
    # 两个客户
    joe = Customer('john Doe', 0)
    ann = Customer('Ann Smith', 1100)
    # 购物车
    cart = [LineItem('banana', 4, .5), LineItem('apple', 10, 1.5), LineItem('water_mellon', 5, 5.0)]
    # 进行下单 -> 计算
    Order(joe, cart, FidelityPromo)
