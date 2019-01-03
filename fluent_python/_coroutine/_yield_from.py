# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :1/3/2019 2:24 PM
# @Author   :zhong
# @Software :PyCharm

def gen():
    for c in 'AB':
        yield c

    for i in range(0, 3):
        yield i


def gen_1():
    yield from 'AB'
    yield from range(1, 3)


def chain():
    print('start')
    yield from 'AB'
    yield from range(0, 3)


if __name__ == '__main__':
    c = chain()
    next(c)