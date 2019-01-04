# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :1/4/2019 1:31 PM
# @Author   :zhong
# @Software :PyCharm

a = {"A":{"a":{"97":"1"}}}



class TestJson:

    def __init__(self, mapping):
        self._data = mapping

    def __getattr__(self, item):
        pass


A = TestJson(a)
