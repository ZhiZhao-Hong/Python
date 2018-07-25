# -*- coding:utf-8 -*-

class Filed():
    pass

class MethodFile(Filed):
    """请求类型修饰符"""
    def __init__(self):
        self.method = None

    def __get__(self, instance, owner):
        return self.method

    def __set__(self, instance, value):
        if value not in ['POST', 'Post', 'post']:
            raise ValueError("The method is not effective : {method}".format(method=value))
        else:
            self.method = value


class CharFile(Filed):
    """字符串修饰符"""
    def __init__(self):
        self.str_ = None

    def __get__(self, instance, owner):
        return self.str_

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError("The value is not str: {str}".format(str=value))
        else:
            self.str_ = value


class BoolFile(Filed):
    """布尔值修饰符"""
    def __init__(self):
        self.bool = None

    def __get__(self, instance, owner):
        return self.bool

    def __set__(self, instance, value):
        if not isinstance(value, bool):
            raise ValueError("The value is not str: {str}".format(str=value))
        else:
            self.bool = value


class IntFile(Filed):
    """整型属性修饰符"""
    def __init__(self):
        pass

    def __get__(self, instance, owner):
        pass

    def __set__(self, instance, value):
        pass


class DictFile(Filed):
    """字典属性修饰符"""
    def __init__(self):
        self._dict = None

    def __get__(self, instance, owner):
        return self._dict

    def __set__(self, instance, value):
        if not isinstance(value, dict):
            raise ValueError("The value type is not dict")
        else:
            self._dict = value