# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :2018/11/26 10:57
# @Author   :zhong
# @Software :PyCharm
import pika

def create_connection():
    # 连接到rabbitmq服务器
    credentials = pika.PlainCredentials('root', 'heygears')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='192.168.101.162',
        port=5672,
        virtual_host='/',
        credentials=credentials
    ))
    return connection