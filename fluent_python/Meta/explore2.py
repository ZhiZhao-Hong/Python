# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :1/4/2019 4:17 PM
# @Author   :zhong
# @Software :PyCharm
import keyword
from collections import abc


class FrozenJson:
    """一个只读接口，使用属性描述符访问json类对象"""

    def __new__(cls, args):
        if isinstance(args, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(args, abc.MutableSequence):
            return [FrozenJson(item) for item in args]
        else:
            return args

    def __init__(self, mapping):
        self._data = {}
        # 处理关键字属性
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self._data[key] = value

    def __getattr__(self, item):
        if hasattr(self._data, item):
            return getattr(self._data, item)
        else:
            return FrozenJson(self._data[item])


if __name__ == '__main__':
    a = {"A": {"B": "1"}}
    f = FrozenJson(a)
    print(f.A)