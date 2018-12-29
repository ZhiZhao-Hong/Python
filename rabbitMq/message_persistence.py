# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :2018/11/26 10:45
# @Author   :zhong
# @Software :PyCharm


# 消息持久化
import pika
from zhong.rabbitMq.connection import create_connection
connection = create_connection()


def producer():
    # ######################### 生产者 #########################
    #创建频道
    channel = connection.channel()

    # 声明消息队列，消息将在这个队列中进行传递。如果将消息发送到不存在的队列，rabbitmq将会自动清除这些消息。如果队列不存在，则创建
    # rabbitmq不允许使用不同的参数来重新定义存在的队列。因此需要重新定义一个队列
    channel.queue_declare(queue='hello', durable=True)  # 声明队列持久化

    # 如果仅仅是设置了队列的持久化，仅队列本身可以在rabbit-server宕机后保留，
    # 队列中的信息依然会丢失，如果想让队列中的信息或者任务保留，还需要做以下设置：
    channel.basic_publish(
        exchange='',
        routing_key='hello',
        body='Hello World!',
        properties=pika.BasicProperties(
            delivery_mode=2,  # 使消息或任务也持久化存储
        )
    )
    # 消息队列持久化包括3个部分：
    #     　　（1）exchange持久化，在声明时指定durable => 1
    #     　　（2）queue持久化，在声明时指定durable => 1
    #     　　（3）消息持久化，在投递时指定delivery_mode=> 2（1是非持久化）
    # 如果exchange和queue都是持久化的，那么它们之间的binding也是持久化的。
    # 如果exchange和queue两者之间有一个持久化，一个非持久化，就不允许建立绑定。

    print("开始队列")
    #缓冲区已经flush而且消息已经确认发送到了RabbitMQ中，关闭链接
    connection.close()


def consumer():
    # 创建频道
    channel = connection.channel()
    # 如果生产者没有运行创建队列，那么消费者创建队列
    channel.queue_declare(queue='hello')


    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        import time
        time.sleep(10)
        print('ok')
        ch.basic_ack(delivery_tag=method.delivery_tag)  # 主要使用此代码

    channel.basic_consume(callback,
                          queue='hello',
                          no_ack=False)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()