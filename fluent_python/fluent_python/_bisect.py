# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :2018/11/28 17:41
# @Author   :zhong
# @Software :PyCharm
import bisect
import sys

HAYSTACK = [1, 4, 5, 6, 8, 12, 15, 20, 21, 23, 23, 26, 29, 30]
NEEDLES = [0, 1, 2, 5, 8, 10, 22, 23, 29, 30, 31]

ROW_FMT = '{0:2d} @ {1:2d}  {2}{0:<2d}'

def demo(bisect_fn):
    for needle in reversed(NEEDLES):
        position = bisect_fn(HAYSTACK, needle)
        offset = position * '   |'
        print (ROW_FMT.format(needle, position, offset))

# 根据一个分数，找到它所对应的成绩
def grade(score, grades='FDCBA'):
    breakpoints = [60, 70, 80, 90]
    i = bisect.bisect(breakpoints, score)
    return grades[i]

if __name__ == '__main__':

    # sys.argv： 返回脚本本身的路径+传入的参数
    # [-1] 如果没有传入参数，取的就是路径。如果有传入，则取最后一个值
    if sys.argv[-1] == 'left':
        bisect_fn = bisect.bisect_left
    else:
        bisect_fn = bisect.bisect

    print ('DEMO:', bisect_fn.__name__)
    print ('haystack ->', ' '.join('%2d' % n for n in HAYSTACK))
    demo(bisect_fn)

    print ([grade(score) for score in [33, 99, 77, 70, 89, 90, 100]])