# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :1/3/2019 9:15 AM
# @Author   :zhong
# @Software :PyCharm
import time
from concurrent import futures


# 计算两个数的最大公约数
numbers = [
    (1963309, 2265973), (1879675, 2493670), (2030677, 3814172),
    (1551645, 2229620), (1988912, 4736670), (2198964, 7876293)
]


def gcd(pair):
    a, b = pair     # 元组拆包
    min_number = min(a, b)
    for i in range(min_number, 0, -1):
        if a%i==0 and b%i==0:
            return i

def test_1():
    """不使用多线程"""
    start = time.time()
    result = list(map(gcd, numbers))
    end = time.time()
    print('Took %.3f seconds.' % (end-start))


def test_2():
    """使用多线程"""
    start = time.time()
    loop = futures.ThreadPoolExecutor(max_workers=5)
    result = list(loop.map(gcd, numbers))
    end = time.time()
    print('Took %.3f seconds.' % (end - start))


def test_3():
    """使用多进程"""
    start = time.time()
    loop = futures.ProcessPoolExecutor(max_workers=5)
    result = list(loop.map(gcd, numbers))
    end = time.time()
    print('Took %.3f seconds.' % (end - start))


if __name__ == '__main__':
    # 0.663
    test_1()
    # 0.605
    test_2()
    # 0.537
    test_3()