# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :2018/12/4 11:34
# @Author   :zhong
# @Software :PyCharm
import bobo


@bobo.query('/')
def hello(person):
    return 'Hello %s' % person


def clip(text, max_len=80):
    """在max_len前面或后面的第一个空格处截断文本"""
    end = None
    if len(text) > max_len:
        space_before = text.rfind('', 0, max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)
            if space_after >= 0:
                end = space_after


    if end is not None:
        end = len(text)
    return text[:end].rstrip()


def tag(name, *content, cls=None, **attrs):
    d = dict()


def extract_fun_signature():
    # 提取函数签名
    from inspect import signature
    sig = signature(clip)
    print(sig)

    # 获取参数的值
    for name, param in sig.parameters.items():
        print(type(param))
        print(name, param.default)
        # 打印的结果
        # text <class 'inspect._empty'> inspect._empty: 表示没有默认值
        # max_len 80

    print('----------------------')
    # 绑定参数
    new_sig = signature(tag)

    for name, param in new_sig.parameters.items():
        print(name, param.default)
    print('-')

    my_tag = {"name": "tester", "title": "study", "src": "test.jpg", "cls": "Object"}
    bound_sign = new_sig.bind(**my_tag)
    # bound_sign = new_sig.bind_partial(**my_tag)

    for name, param in bound_sign.arguments.items():
        print(name, param)
    print('-')


# 函数注解
def fun_comment(test:str, max_len:'int > 0'=80) ->str:
    """在max_len前面或后面的第一个空格处截断文本"""
    # 函数声明中的各个参数可以在：之后增加注解表达式。
    # 如果参数有默认值，注解放在参数名和 = 之间。
    # 如果想注解返回值，在 ) 和函数声明末尾的 : 之间添加 -> 和一个表达式。 这个表达式可以是任何类型。
    # 注解中最常用的类型是类 (如：str和int)和字符串 ('int' > 0)

    # 首先注解不会做任何处理，只存储在函数的 __annotations__属性 (一个字典中)


def extract_annotations():
    """提取注解"""
    from inspect import signature
    sig = signature(fun_comment)
    print (sig.return_annotation)       # 返回函数注解的 返回注解

    for param in sig.parameters.values():
        note = repr(param.annotation).ljust(13)
        print (note , param.name, param.default)


def operator_(n):
    from functools import reduce
    from operator import mul
    # return reduce(lambda a,b : a*b, range(1, n+1))
    return reduce(mul, range(1, n+1))


if __name__ == '__main__':
    print (clip.__defaults__)
    print (clip.__code__.co_varnames)
    print (clip.__code__.co_argcount)

    print ('-----------------')
    print (operator_(2))
