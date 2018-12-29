# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :2018/11/29 14:02
# @Author   :zhong
# @Software :PyCharm
import numpy
a = numpy.arange(12)
print (a)
print (type(a))

print (a.shape) # a的形状
# (12,)

a.shape = 3, 4
print (a)
#[[ 0  1  2  3]
# [ 4  5  6  7]
# [ 8  9 10 11]]

print (a[0])
# [0 1 2 3]
print (a[2][1])
# 9
print (a[:,1])
# [1 5 9]
print (a.transpose())
#[[ 0  4  8]
# [ 1  5  9]
# [ 2  6 10]
# [ 3  7 11]]