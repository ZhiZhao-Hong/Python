# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :2018/11/28 14:04
# @Author   :zhong
# @Software :PyCharm

# # 具名元组的使用方法
# from collections import namedtuple
#
# City = namedtuple('City', 'name country population coordinates')
# tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
# # print (tokyo.name)
# # Tokyo
# # print (City._fields)
# # ('name', 'country', 'population', 'coordinates')
#
# LatLong = namedtuple('LatLong', 'lat long')
# delhi_data = ('Delhi NCR', 'IN', 21.935, LatLong(28.613889, 77.208889))
# delhi = City._make(delhi_data)
# # print (delhi)
# # 等于City(*delhi_data)
#
# # print (delhi._asdict())
# # 把具名元组以collections.OrderedDict的形式返回
# # OrderedDict([('name', 'Delhi NCR'), ('country', 'IN'), ('population', 21.935),
# # ('coordinates', LatLong(lat=28.613889, long=77.208889))])
#
#
# # 切片 - 高阶用法
# invoice = """
# 0.......8..........................35......43..47.....
# 1909    Pimoroni PiBrella          $17.50  3   $52.50
# 1489    6mm Tactile Switch x20     $4.95   2   $9.90
# 1510    Panavise Jr. - PV-201      $28.00  1   $28.00
# 1601    PiTFT Mini Kit 320x240     $34.95  1   $34.95
# """
# SKU = slice(0, 8)
# DESCRIPTION = slice(8, 35)
# UNIT_PRICE = slice(35, 43)
# QUANTITY = slice(43, 47)
# ITEM_TOTAL = slice(47, None)
# # 去掉 第一行的\n和第二行的。。。。6
# line_items = invoice.split('\n')[2:]
# for item in line_items:
#     print (item[UNIT_PRICE], item[DESCRIPTION])
# # 可以快速对位文本的位置进行截取
#
# # 列表叠加的区别
# a = [1]
# print (id(a))
# b = [2]
# # 第一种叠加的方法
# a +=b
# print (id(a))
# print (a)
# # 第二种叠加的方法
# a = a+b
# print (id(a))
# print (a)
# # 结果比较：两种的结果都是一样的，但是只有第一种的叠加的方法与a原来的id是一样


# 列表排序
number = [2, 5, 3, 1, 6, 4, 8]

print (number)
print (sorted(number))
print (sorted(number, reverse=True))
