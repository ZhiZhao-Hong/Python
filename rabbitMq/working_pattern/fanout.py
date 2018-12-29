# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :2018/11/26 10:55
# @Author   :zhong
# @Software :PyCharm

# fanout模式简介
# 任何发送到fanout exchange的消息都会被转发到exchange绑定（Binding）的所有Quene上
#   1. 可以理解为路由表的模式
#   2. 这种模式不需要routing_key(及时指定，也是无效的)
#   3. 这种模式需要提前将exchange与quene进行绑定，一个exchange可以绑定多个queue，一个queue可以同时多个exchange进行绑定
#   4. 如果接受到消息的exchange没有与任何的Queue进行绑定，则消息会被抛弃

import pika
from zhong.rabbitMq.connection import create_connection


connection = create_connection()

def producer():
    channel = connection.channel()
    channel.exchange_declare(
        exchange='logs_fanout',
        exchange_type='fanout'
    )

    message = 'Hello Python'
    # 将消息发送到交换机
    channel.basic_publish(
        exchange='logs_fanout', # 指定exchange
        routing_key='', #fanout不需要配置，配置了也不会生效
        body=message
    )
    print(" [x] sent %r" % message)
    connection.close()

def consumer():
    channel = connection.channel()
    channel.exchange_declare(
        exchange='logs_fanout',
        exchange_type='fanout'
    )

    # 随机创建队列
    # exclusive=True表示建立临时队列，当consumer关闭之后，该队列就会删除
    # 1
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    # 2
    result_1 = channel.queue_declare(exclusive=True)
    queue_name_1 = result_1.method.queue


    # 将队列与exchange进行绑定
    channel.queue_bind(exchange='logs_fanout',queue=queue_name)
    channel.queue_bind(exchange='logs_fanout',queue=queue_name_1)

    print (' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print (" [x] %s" % body)

    # 从队列获取信息
    channel.basic_consume(callback, queue=queue_name, no_ack=True)
    channel.basic_consume(callback, queue=queue_name_1, no_ack=True)
    # 阻塞
    channel.start_consuming()


if __name__ == '__main__':
    consumer()
    # producer()