# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :1/4/2019 2:37 PM
# @Author   :zhong
# @Software :PyCharm
import keyword
from collections import abc


class FrozenJSON:
    """一个只读接口，使用属性表示法访问JSON对象"""

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
            return FrozenJSON.build(self._data[item])

    def __getitem__(self, item):
        return self._data[item]

    @classmethod
    def build(cls, obj):
        # Mapping 映射类型，在Python中就只有dict类型是映射类型的
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        # 判断是否为列表
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj


class Test:

    def __init__(self):
        self._data = {"A": {"B": "1"}}

    def __getattr__(self, item):
        return self._data


if __name__ == '__main__':
    A = {"class": {"B": "1"}}
    f = FrozenJSON(A)
    print(f['class'])