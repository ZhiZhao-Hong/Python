# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :1/3/2019 2:17 PM
# @Author   :zhong
# @Software :PyCharm
from inspect import getgeneratorstate


def simple_coroutine():
    print('-> coroutine started')
    x = yield
    print('-> coroutine received:', x)


if __name__ == '__main__':
    my_coro = simple_coroutine()
    print(getgeneratorstate(my_coro))

    # 激活协程
    next(my_coro)
    print(getgeneratorstate(my_coro))
    my_coro.send('1')
