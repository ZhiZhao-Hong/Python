# -*- coding:utf-8 -*-


# 魔法函数
class Company(object):
    def __init__(self, employ_list):
        self.employee = employ_list

    def __getitem__(self, item):
        """存在这个的时候，就可以变成个迭代的一个对象,当抛出异常的时候，才会停止"""
        return self.employee[item]

    def __len__(self):
        """当 getitem 不存在的时候，又想返回长度，可以用这个"""
        return len(self.employee)

    def __str__(self):
        """print(company) 的时候 相当于 print(str(company)) 这个时候是调用这个内置函数的"""
        return('我是__str__')

    def __repr__(self):
        """这个是在开发模式下，也就是cmd模式下，输入company回车输出的内容,常见的是这个类的地址 相当于内部的repr(company)"""
        return('我是__repr__')


company = Company(["tom", "bob", "jane"])
# emploee = company.employee
# for em in company:
#     print(em)

# python 的数据模型以及数据模型对Python的影响
company1 = company[:2]
# 切片，因为是可迭代对象。所以这种时候就改变的Company这的数据结构。

# 魔法函数一览
'''
非数学运算：
    字符串表示 : __repr__ , __str__
    集合、序列相关 : __len__ , __getitem__ , __setitem__ , __delitem__ , __contains__
    迭代相关 : __iter__ , __next__
    可调用 : __call__
    with上下文管理器 : __enter__ , __exit__
    数值转换 : __abs__ , __bool__ , __int__ , __float__ , __hash__ , __index__
    元类相关 : __new__ , __init__
    属性相关 : __getattr__ , __setattr__ , __getattribute__ , __setattribute__ , __dir__
    属性描述符 : __get__ , __set__ , __delete__
    协程 : __await__ , __aiter__ , __anext__ , __aenter__ , __aexit__
数学运算：
    用的比较少，可以自己去了解一下。数据处理的时候比较多。
'''
# 常用的cmd下的ipython 还有一个增强工具notebook
# pip install notebook -i https://pypi.douban.com/simple
# len 内置函数，一般情况下会去调用底层的c语言，直接读取长度，效率更好，如果有__len__才去调用python的

# 深入了解类和对象
# 鸭子类型 和 多态
# 当看到一只鸟走起来像鸭子，游泳起来像鸭子，叫起来也像鸭子，那么这只鸟就可以被称为鸭子
class Cat(object):
    def say(self):
        print('i am a cat')

class Dog(object):
    def say(self):
        print('i am a dog')

class Duck(object):
    def say(self):
        print('i am a duck')


# animal_list = [Cat, Dog, Duck]
# for animal in animal_list:
#     animal().say()


# 抽象基类
# 我们要去检查某个类是否有某种方法
print (hasattr(company,"__len__"))

# 我们在某些情况下希望判断某个对象的类型
from collections.abc import Sized
print (isinstance(company,Sized))
# 我们需要强制某个子类必须实现某些方法
# 实现一个web框架，集成cache(redis, cache, memerychache)
# 需要设计一个抽象基类，指定子类必须实现某些方法

# 如何去模拟一个抽象基类
# class CacheBase():
#     def get(self, key):
#         raise NotImplementedError
#
#     def set(self, key, value):
#         raise NotImplementedError
#
#
# class RedisCache(CacheBase):
#     def get(self, key):
#         pass
#
#
# redis_cache = RedisCache()
# redis_cache.get('key')
'''强制通过抛出异常，如果不重写就直接报异常'''

# 第二种 abc的模块
import abc
# 通用的基类
from collections.abc import *
class CacheBase1(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self, key):
        pass

    @abc.abstractmethod
    def set(self, key, value):
        pass


class RedisCache1(CacheBase1):
    pass


# redis_cache1 = RedisCache1()


# isinstance 和 type的区别


class A:
    aa = 1 # 类变量
    def __init__(self,x,y):
        self.x = x
        self.y = y

# 类变量是共享的，成员变量不是共享的
a = A(1,2)
A.aa = 11
b = A(2,3)
# b.aa = 11

# 类属性和砬属性以及查找顺序


# python的类方法，静态方法，和实例方法
# 普通情况下，我们定义的方法都是实例方法
class Date():
    # 构造函数
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def tomorrow(self):
        self.day += 1

    # 返回的时候，Date是硬编码，如果类名修改，则需要修改
    @staticmethod
    def parse_from_str(data_str):
        year, month, day = tuple(data_str.split('-'))
        return Date(int(year), int(month), int(day))

    @staticmethod
    def valid_str(data_str):
        year, month, day = tuple(data_str.split('-'))
        if int(year)>0 and (12>=int(month)>0) and (31>=int(month)>0):
            return True
        else:
            return False

    @classmethod
    def from_str(cls,data_str):
        year, month, day = tuple(data_str.split('-'))
        return cls(int(year), int(month), int(day))


    def __str__(self):
        return "{year}/{month}/{day}".format(year=self.year, month=self.month, day=self.day)

# 私有模式
class Users:
    def __init__(self, birthday):
        self.birthday = birthday
        self.__test = '1'  # _ClassName__attr 会编译成这种，也就是继承的时候，私有属性是不会覆盖的

    def get_age(self):
        return 2018 - self.birthday.year

# 自省机制  通过一定的机制查询到对象的内部机构
class Person():
    name = 'user'

class Student(Person):
    def __init__(self, school_name):
        self.scool_name = school_name

# supper函数 - 调用父类

class A():
    def __init__(self):
        print ('a')

class B():
    def __init__(self):
        print ('b')
        super() .__init__()

# with 上下文管理器
try:
    print ("code started")
    # 引发异常
    # raise IndexError
except KeyError as e:
    # 捕获对应的异常
    print ("key error")
else:
    # 未抛异常的时候
    print ('')
finally:
    # 全部完成之后,如何这里有return 都是返回这里的。因为这里是栈，最后入栈的，都是最早出的
    print ('')

# 上下文管理器的协议
class Sample():
    def __enter__(self):
        # 获取资源
        print ('enter')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 释放资源
        print ("exit")

    def do_something(self):
        print ('doing something')

with Sample() as sample:
    sample.do_something()

# 简化上下文管理器
import contextlib
@contextlib.contextmanager # 修饰的是生成器
def file_open(file_name):
    print ('file open')         # __enter__
    yield {}
    print ('file end')          # __exit__

with file_open('bobby.txt') as f_opened:
    print ("file processing")

# ----------------------------------------------------------------------------------------------------------------------
# 序列类
# +  +=  extent
# + 两个list相加，链接成一个list，两边类型需要相同
# += 也是两个相加，但是类型可以不相同，就是一个是list，一个是tuple，相当于是extent的方法
# extend 和+=一样
# append是直接相加，不是迭代相加。会把列表直接加进去  [1,2,3,[1,2]]

# 切片  [start:end:step]
import numbers
class Group():

    def __init__(self, group_name, company_name, staffs):
        self.group_name = group_name
        self.company_name = company_name
        self.staffs = staffs  # 这个是列表

    def __reversed__(self):
        self.staffs.reversed()

    def __getitem__(self, item):
        cls = type(self)
        if isinstance(item,slice):
            return cls(group_name=self.group_name,company=self.company_name,staffs=self.staffs[item])
        elif isinstance(item,numbers.Integral):
            return cls(group_name=self.group_name,company=self.company_name,staffs=[self.staffs[item]])

        # return self.staffs[item ]
    def __len__(self):
        return len(self.staffs)

    def __iter__(self):
        return iter(self.staffs)

    def __contains__(self, item):
        if item in self.staffs:
            return True
        else:
            return False

import bisect
# 用来处理已排序的序列，用来维持已排序的序列，升序(二分查找)
inter_list = []
bisect.insort(inter_list,3)
bisect.insort(inter_list,2)
bisect.insort(inter_list,5)
bisect.insort(inter_list,1)
bisect.insort(inter_list,6)
# [1,2,3,4,5]
# 查询位置
# bisect.bisect = bisect.bisect_right()


# 列表的使用情况
# array,deque的使用
# 数组
# array 和 list 的一个重要的区别， array只能存放指定的数据类型
import array
my_array = array.array("i")

# 列表推导式、生成器表达式、字典推导式
# 列表推导式 []
# 生成器表达式 ()
# 字典推导式 {} {value:key for key, value in my_dict.items()}
# 集合推导式 - set - my_set = {key for key, value in my_dict.items()} / set(my_dict.keys())

# ----------------------------------------------------------------------------------------------------------------------
# dict 和 abc的关系
from collections.abc import Mapping
# dict 属于mapping类型
a = {}
print (isinstance(a ,MutableMapping))

# 深拷贝
import copy
# copy.deepcopy()
new_list = ['shine', 'shine1']
new_dict = dict.fromkeys(new_list, "")   # 给list转化为dict，并设置默认值
value  = new_dict.get("shine2", {})      # 获取new_dict['shine2']如果不存在的，则返回{}
value1 = new_dict.setdefault('shine2','test')   #同上，但是查询不到，则可以会自动添加进去

# set 和 fronzenset (不可以变集合) 无序的集合，消除重复
# fronzenset 可以作为dict的key

# dict 查找的性能，远远大于list。
# 在list中，随着list的数据的增大，查找的时间会增大。
# 在dict中，查找元素。不会随着dict的增大而增大。
# 1. dict的key或者set的值，都必须是可以hash的，不可变对象都是可以hash的。
# 2. dict的内存花销大，但是查询速度快。
# 3. dict的存储顺序是添加顺序有关。
# 4. 添加数据有可能已有数据的顺序 (hash的时候有可能插入前面的空白)。

#-----------------------------------------------------------------------------------------------------------------------
# 对象引用，可变性和垃圾回收
# python和java中的变量本质不一样，python的变量实质上是一个指针，int，str。

# python 中垃圾回收的算法是采用 应用计数的，del - number减一
a = 1 # number = 1
b = a # number +=1
# number - 到0的时候，就会回收

#

if __name__ == '__main__':
    # new_day = Date(2018, 12, 31)
    # new_day.tomorrow()
    # # print (new_day)
    #
    # new_day_1 = Date.parse_from_str('2018-12-31')
    # print (new_day_1)
    # u = Users(Date(1990,2,1))
    # print (u.get_age())
    # print (u._Users__test)
    user = Student('慕课网')
    print (user.__dict__)   # 列出主要属性
    print (dir(user))   # 列出所有的属性