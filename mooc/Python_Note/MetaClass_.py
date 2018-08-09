# -*- coding:utf-8 -*-
# 元类编程
import numbers
from datetime import date,datetime

# __new__ 和 __init__的区别

class User():

    def __new__(cls, *args, **kwargs):
        return super.__new__(cls)

    def __init__(self):
        pass

# new 是用来控制对象的生成过程, 在对象生成之前
# init 是用来完善对象的
# new如果返回对象，则init不会调用

# ----------------------------------------------------------------------------------------------------------------------
def say(self):
    return 0

# 动态创建类
type("ClassName", (object,) ,{"name":"user", "say":say})

# 什么是元类，元类是创建类的类
class MetaClass(type):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

class Users(metaclass=MetaClass):
    def __init__(self, name):
        self.name = name


# python中实例化的过程


# ----------------------------------------------------------------------------------------------------------------------
# # 属性描述符
class IntField():
    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if not isinstance(value,numbers.Integral):
            raise ValueError("Int value need")
        self.value = value

    def __delete__(self, instance):
        pass


class NonDataIntFiled():
    """非数据属性描述符"""
    def __get__(self, instance, owner):
        return self.value


class Users():
    age = IntField()

if __name__ == '__main__':
    user = Users()
    user.age = "abc"
    print (user.age)

'''
如果user是某个类的实例，那么user.age(以及等价的getattr(user,'age'))
首先调用 __getattribute__. 如果类定义了 __getattr__方法，
那么在 __getattribute__ 抛出 AttributeError 的时候就会调用 __getattr__，
而对于描述符 (__get__)的调用，则是发生在 __getattribute__ 内部的。
user = User(), 那么user.age 顺序如下：

1 -> 如果 age 是出现在User或者其基类的 __dict__中，且 age 是 data descriptor(数据描述符) ，那么会调用 data descriptor 的 __get__
2 -> 如果 age 出现在 User 的 __dict__ 中，那么直接返回obj.__dict__['age']
3 -> 如果 age 出现在 User 或其 基类的 __dict__中
    1 -> 如果 age 是 non-data descriptor ，那么调用其 __get__方法
    2 -> 返回 __dict__['age']
4 -> 如果 User 有 __getattr__ 方法，调用 __getattr__方法
5 -> 抛出AttributeError

总结： 数据描述符 -> 类的__dict__ -> 非数据描述符 -> 类的成员变量 -> __getattr__/__getattribute__ -> 抛出异常
'''

# ----------------------------------------------------------------------------------------------------------------------
# __getattr__ 和__getattribute__ 的使用方法，已经set和get的使用
class User():

    def __init__(self, name, birthday, info):
        self.name = name
        self.birthday = birthday
        self._age = 0
        self.info = info

    def __getattr__(self, item):
        '''查找不到属性的时候的处理操作 - '''
        return self.info[item]

    # def __getattribute__(self, item):
    #     '''这个优先级最高，所有的属性都是这里返回的，不管存在不存在，所以这个不要乱写，不然容易奔溃'''

    @property
    def age(self):
        # 类似于get
        return datetime.now().year - self.birthday.year

    @age.setter
    def age(self,value):
        # 类似于set
        self._age = value

if __name__ == '__main__':
    user = User('shine',date(year=2018, month=7, day=24),{"name":"shine"})