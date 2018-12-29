# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :2018/12/10 13:59
# @Author   :zhong
# @Software :PyCharm

# 输出函数的运行时间
import time


def clock(func):
    def clocked(*args):
        # time.perf_counter : 返回计算机的精准时间
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ','.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked
# from zhong.fluent_python._decorator_model import snooze
# print(snooze.__name__)  -> clocked
# 所以上面的装饰器有个缺点：掩盖了被装饰函数的__name__和__doc__属性。

# 改进版本
import functools
def new_clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        # time.perf_counter : 返回计算机的精准时间
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        name = func.__name__

        arg_list = []
        if args:
            arg_list.append(','.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_list.append(','.join(pairs))
        arg_str = ','.join(arg_list)

        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked

# ----------------------------------------------------------------------------------------------------------------------
# lru_cache、singledispatch
# lru = least recently used : 表明缓存不会无限制增长，一段时间不用的缓存条目会被扔掉
# Python 内置三个装饰器：1.property, 2.classmethod, 3.staticmethod

# 菲薄那切数列变通版本
# 参数maxsize: 缓存个数(最好是2的幂次方)， typed: True -> 把不同参数类型得到的结果分别保存
# 因为lru_cache使用字典存储结果，而且键是根据调用是传入的对位参数和关键字参数创建的，所以给装饰的参数必须是可散列的
@functools.lru_cache()
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)
# -
# singleddispatch
import html

# ----------------------------------------------------------------------------------------------------------------------
# 参数化装饰器
registry = []

def register(func):
    print('running register(%s)' % func)
    registry.append(func)
    return func

@register
def f1():
    print ('running f1()')

# ----------------------------------------------------------------------------------------------------------------------
@clock
def snooze(seconds):
    time.sleep(seconds)


if __name__ == '__main__':
    # snooze(2)
    # ---------
    print (fibonacci(60))