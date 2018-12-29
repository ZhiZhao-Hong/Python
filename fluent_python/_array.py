# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :2018/11/29 13:14
# @Author   :zhong
# @Software :PyCharm

from array import array
from random import random


# random() 随机返回十六位的小数
floats = array('d', (random() for i in range(10**7)))
print (floats[-1])

# floats.bin 二进制文件
def to_file():
    fp = open('floats.bin', 'wb')
    floats.tofile(fp)
    fp.close()

def from_file():
    floats_2 = array('d')
    fp = open('floats.bin', 'rb')
    floats_2.fromfile(fp, 10**7)
    fp.close()
    print (floats_2[-1])

# floats_2 == floats    True

if __name__ == '__main__':
    to_file()
    from_file()