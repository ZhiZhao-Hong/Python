# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :2018/12/7 14:02
# @Author   :zhong
# @Software :PyCharm

# 装饰器的特性
# 1. 能被装饰的函数替换成其他函数。
# 2. 装饰器在加载模块是立即运行。


registry = []


def register(func):
    print('running register(%s)' % func)
    registry.append(func)
    return func


@register
def f1():
    print ('running f1()')


@register
def f2():
    print ('running f2()')


@register
def f3():
    print ('running f3()')


def main():
    print ('running main()')
    print('registry ->', registry)
    f1()
    f2()
    f3()


if __name__ == '__main__':
    main()