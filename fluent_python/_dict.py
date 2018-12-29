# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :2018/11/29 14:57
# @Author   :zhong
# @Software :PyCharm
import sys
import re
import collections
# \w 匹配一个数字或者一个字母
# + 至少一个

def set_default():
    WORD_RE = re.compile(r'\w+')

    index = {}

    with open(sys.argv[1], encoding='utf-8') as fp:
        for line_no, line in enumerate(fp, 1):
            for match in WORD_RE.finditer(line):
                word = match.group()
                column_no = match.group()
                locations = (line_no, column_no)
                # 这其实是一种很不好的实现，这里写只是为了验证论点
                occurrences = index.get(word, [])
                occurrences.append(locations)
                index[word] = occurrences

                # 上面三个函数的效果
                # 先看是否有值，没有的话返回一个空的[],然后再把坐标添加进去，最后加到index对应的word下


                # 实际上最好的做法
                index.setdefault(word, []).append(locations)

    # 以字母的顺序打印出结果
    for word in sorted(index, key=str.upper):
        print (word, index[word])


def default_dict():
    index = collections.defaultdict(list)
    # 注意以下两种的差距，只有在a[]的这种情况下，才会触发创建默认值
    # 因为只有a[]的时候才是调用__getitem__的内置函数，而__missing__只会给__getitem__调用
    print (index.get('a'))
    #None

    print (index['a'])
    print (index)
    # defaultdict(<class 'list'>, {'a': []})


class StrKeyDict0(dict):

    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, item):
        return item in self.keys() or str(item) in self.keys()


if __name__ == '__main__':

    collections.UserDict