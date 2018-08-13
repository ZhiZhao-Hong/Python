# -*- coding:utf-8 -*-
# Flask web框架

# 请求 线程
# 10个线程 flask开启多少个线程来处理请求
# webserver


# ----------------------------------------------------------------------------------------------------------------------
# 线程隔离 - (字典 保存数据 requests = {thread_key1: value, thread_key2: value})
# 操作数据
# Flask-werkzeug local Local

import werkzeug, threading, time
from werkzeug.local import Local
# t1 l.a t2 l.a

#
# class A:
#     b = 1

my_obj = Local()
my_obj.b = '1'

def worker():
    # 新线程
    my_obj.b = '2'
    print('in new thread b is :' + my_obj.b)


new_t = threading.Thread(target=worker, name='shine_thread')
new_t.start()
new_t.join()
print('in main thread b is :' + my_obj.b)


# -----------------------------------------------------------------
# Local LocalStack Dict
# Local 使用字典的方式实现的线程隔离
# 线程隔离的栈结构 - LocalStack
# 封装 - 如果一次封装解决不了问题，那就再来一次
# -----------------------------------------------------------------

# 栈的三个操作
# push, pop, top
from werkzeug.local import LocalStack
s = LocalStack()
s.push(1)
print(s.top) # 取出栈顶元素，但不删除元素，pop会删除栈栈顶元素