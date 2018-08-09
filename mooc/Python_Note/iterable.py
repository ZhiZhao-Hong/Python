# -*- coding:utf-8 -*-

# 什么是迭代协议
# 迭代器是访问集合内元素的一种方式，一般用来遍历数据
# 迭代器和以下标的访问方式不一样，迭代器是不能返回的，迭代器提供了一种惰性方式的数据方式
# [] list 下标是使用了 __getitems__的内置函数，迭代协议是 __iter__

from collections.abc import Iterable,Iterator

# Iterable 可迭代的  __iter__ 返回迭代器的
# Iterator 迭代器  __next__ 拿到下一个数据


class Company(object):

    def __init__(self, employee_list):
        self.employee = employee_list

    def __iter__(self):
        return MyIterator(self.employee)

    def __getitem__(self, item):
        return self.employee[item]


class MyIterator(Iterator):

    def __init__(self, employee_list):
        self.iter_list = employee_list
        self.index = 0

    def __next__(self):
        try:
            word = self.iter_list[self.index]
        except IndexError as e:
            raise StopIteration
        finally:
            self.index += 1
        return word

# 生成器 ，函数只要有yield关键字，就是生成器
def gen_func():
    yield 1
    yield 2
    yield 3
    # 惰性求值，延迟求值

def func():
    return 1


# 生成器的原理
'''
python 中函数的工作原理


'''

if __name__ == "__main__":
    # 生成器对象，python编辑字节码的时候就产生了
    pass

# ----------------------------------------------------------------------------------------------------------------------
#抓取天气的信息，一个一个的显示出来
'''
北京 : 高温 15.0℃ , 低温 8.0℃
广州 : 高温 28.0℃ , 低温 19.0℃
'''

# import requests,time
#
# def getWeather(city):
#     response = requests.get('http://www.sojson.com/open/api/weather/json.shtml?city='+city)
#     data = response.json()['data']['forecast'][0]
#     return ('%s : %s , %s' % (city, data['high'], data['low']))
#
# #['北京','上海','广州','深圳']
# print (getWeather('北京'))
# time.sleep(3)
# print (getWeather('广州'))

#迭代器和迭代对象
a = ['1','2','3']
#
print (iter(a))
print (dir(a))
#
# t = iter(a)
# print (t.__next__())
# print (t.__next__())
# print (t.__next__())
# print (t.__next__())

from collections import Iterator,Iterable
import requests,time
class WeatherIterator(Iterator):

    def __init__(self,city):
        self.city = city
        self.index = 0

    def getWeather(self,city):
        response = requests.get('http://www.sojson.com/open/api/weather/json.shtml?city='+city)
        data = response.json()['data']['forecast'][0]
        return ('%s : %s , %s' % (city, data['high'], data['low']))

    def __next__(self):
        if self.index == len(self.city):
            raise StopIteration
        # else:
        time.sleep(3)
        city = self.city[self.index]
        self.index +=1
        return self.getWeather(city)

class WeatherIterable(Iterable):
    def __init__(self,cities):
        self.cities = cities

    def __iter__(self):
        return WeatherIterator(self.cities)

for i in WeatherIterable(['北京', '上海', '广州', '深圳']):
    print (i)


# ----------------------------------------------------------------------------------------------------------------------
# 装饰器
import time
# def f1(n):
#     if n<=1:
#         return 1
#     else:
#         return f1(n-1) + f1(n-2)



# def f(n,cache=None):
#     if cache is None:
#         cache = dict()
#     if n in cache.keys():
#         return cache[n]
#     if n<=1:
#         return 1
#     else:
#         cache[n] = f(n-1,cache) + f(n-2,cache)
#         return cache[n]
#
# start_time = time.time()
# print(f(40))
# end_time = time.time()
# print(end_time - start_time)

def memo(func):
    cache = {}
    def warp(*args):
        if args not in cache:
            # print (*args)
            cache[args] = func(*args)
        return cache[args]
    return warp

@memo
def f1(n):
    if n<=1:
        return 1
    else:
        return f1(n-2) + f1(n-1)
print (f1(40))


@memo
def climb(n,steps):
    count = 0
    if n == 0:
        count = 1
    elif n > 0:
        for step in steps:
            count += climb(n - step,steps)
    return count

print (climb(40,(1,2,3)))

# ----------------------------------------------------------------------------------------------------------------------
# 函数签名
from inspect import signature
def type_assert(*ty_args,**ty_kwargs):
    def decorator(func):
        sig = signature(func)
        b_type = sig.bind_partial(*ty_args,**ty_kwargs).arguments
        def wrapper(*args,**kwargs):
            for name,obj in sig.bind(*args,**kwargs).arguments.items():
                print (name,obj)
                if name in b_type:
                    if not isinstance(obj,b_type[name]):
                        raise TypeError('"%s" must be %s' % (name,b_type[name]))
            return func(*args,**kwargs)
        return wrapper
    return decorator

@type_assert(c=int)
def f(a,b,c=1):
    print (a,b,c)
f(1,1,3)
#提取函数签名
from inspect import signature
def f(a,b,c=1): pass
sig = signature(f)
# print (sig)
# print (sig.parameters)
# a = sig.parameters['c'] # 转化成字典
# print (dir(a))
# print (a.name)          # a的名字
# print (a.kind)          # 参数属于哪种类型
# print (a.default)       # a的默认参数值

# 建立一个字典
#bin 和 bind_partial的区别，前者默认参数一定要传齐，后者不用
# bargs = sig.bind_partial(str,int,int)       # 传的参数是必须传递齐，不然会报错



#-----------------------------------------------------------------------------------------------------------------------
from inspect import signature

def type_assert(*ty_args,**ty_kwargs):
    def decorator(func):
        # 获取函数的数字签名
        # d = {'a':'int','b':'str','c':'int'}
        sig = signature(func)
        b_type = sig.bind_partial(*ty_args,**ty_kwargs).arguments
        def wrapper(*args,**kwargs):
            # args in d : isinstance(args,d[args])
            for name,obj in sig.bind(*args,**kwargs).arguments.items():
                if name in b_type:
                    if not isinstance(obj,b_type[name]):
                        raise TypeError('"%s" must be "%s"' % (name,b_type[name]))
            return func(*args,**kwargs)
        return wrapper
    return decorator


@type_assert(a = int )
def f(a,b,c=1):
    print (a,b,c)

f('str',2,3)