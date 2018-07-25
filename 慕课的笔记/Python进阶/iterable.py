# -*- coding:utf-8 -*-

# 什么是迭代协议
# 迭代器是访问集合内元素的一种方式，一般用来遍历数据
# 迭代器和以下标的访问方式不一样，迭代器是不能返回的，迭代器提供了一种惰性方式的数据方式
# [] list 下标是使用了 __getitems__的内置函数，迭代协议是 __iter__

from collections.abc import Iterable,Iterator

# Iterable 可迭代的  __iter__ 返回迭代器的
# Iterator 迭代器  __next__ 拿到下一个数据


class Company(object):

    def __init__(self, employee_list):
        self.employee = employee_list

    def __iter__(self):
        return MyIterator(self.employee)

    def __getitem__(self, item):
        return self.employee[item]


class MyIterator(Iterator):

    def __init__(self, employee_list):
        self.iter_list = employee_list
        self.index = 0

    def __next__(self):
        try:
            word = self.iter_list[self.index]
        except IndexError as e:
            raise StopIteration
        finally:
            self.index += 1
        return word

# 生成器 ，函数只要有yield关键字，就是生成器
def gen_func():
    yield 1
    yield 2
    yield 3
    # 惰性求值，延迟求值

def func():
    return 1


# 生成器的原理
'''
python 中函数的工作原理


'''

if __name__ == "__main__":
    # 生成器对象，python编辑字节码的时候就产生了
    pass