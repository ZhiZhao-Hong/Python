# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :2018/11/27 15:45
# @Author   :zhong
# @Software :PyCharm
# 向量问题

from math import hypot


class Vector():

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # __repr__ 和 __str__和差别
    # __repr__ : repr()函数输出的内容，相当于在ide模式下，直接控制台直接输出的内容，当类中无__str__，print也可以输出
    # __str__ : print 输出的内容

    def __repr__(self):
        return 'Vector(%r, %r)' % (self.x, self.y)

    # def __str__(self):
    #     return '1'

    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, other):
        return Vector(self.x*other, self.y*other)


from array import array
import math

from array import array
import reprlib
import math, numbers


class Vector3:

    type_code = 'd'

    def __init__(self, components):
        self._components = array(self.type_code, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.type_code)]) + bytes(self._components))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.sqrt(sum(x*x for x in self))

    def __bool__(self):
        return bool(abs(self))

    @classmethod
    def from_bytes(cls, octets):
        type_code = chr(octets[0])
        men_v = memoryview(octets[1:]).cast(type_code)
        return cls(men_v)

    def __len__(self):
        return len(self._components)

    def __getitem__(self, item):
        cls = type(self)
        if isinstance(item, slice):
            return cls(self._components[item])
        elif isinstance(item, numbers.Integral):
            return self._components[item]
        else:
            msg = '{cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=cls))
