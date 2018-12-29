# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :2018/11/23 13:29
# @Author   :zhong
# @Software :PyCharm

import pika
from zhong.rabbitMq.connection import create_connection


#  生成者


# 账号密码需要在linux上创建
# 先启动rabbitMq的服务再创建用户 rabbit-server start
# rabbitMq的创建命令：rabbitmqctl add_user root heygears
# 创建失败的话, 重启一下服务器，service rabbitmq-server restart
# 服务暂停 rabbitmqctl stop

connection = create_connection()
# 创建频道
channel = connection.channel()

# 声明消息队列，消息将在这个队列中进行传递。
# 如果将信息发送到不存在的队列，rabbitmq将会自动清除这些信息。
# 如果队列不存在，则创建
channel.queue_declare(queue='hello')

# exchange -- 它使我们能够确切地指定消息应该到哪个队列去
# 向队列插入数值 routing_key 是队列名 body是要插入的内容
channel.basic_publish(
    exchange= '',
    routing_key = 'hello',
    body = 'Hello Word！'
)
print ("开始队列")
connection.close()

