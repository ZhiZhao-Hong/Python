# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :2018/11/26 10:55
# @Author   :zhong
# @Software :PyCharm
# 工作原理
# 路由键的工作原理：每个接收端的消息队列在绑定交换机的时候，可以设定相应的路由键，发送端通过交换机发送信息时，可以指明路由键，
# 交换机会根据路由键把消息发送到对应的消息队列，这样接收端就能接收到消息了

# 任何发送到Direct Exchange的消息都会被转发到routing_key中指定的queue：
#   1. 一般情况下可以使用rabbitMq自带的exchange：""(该exchange的名字为空字符串), 也可以自定义exchange
#   2. 这种模式下不需要将exchange进行任何绑定（bind）操作。当然也可以进行绑定，可以将不同的routing_key与不同的queue进行绑定，
#       不同的queue与不同exchange进行绑定
#   3. 消息传递时需要一个routing_key
#   4. 如果消息中中不存在routing_key 中绑定的队列名，则消息会被抛弃
# 如果一个exchange 声明为direct, 并且bind中指定了routing_key, 那么发送消息时需要同时指明该exchange和routing_key


import pika
from zhong.rabbitMq.connection import create_connection


connection = create_connection()


def consumer():
    channel = connection.channel()
    # 定义了exchange和类型
    channel.exchange_declare(exchange='direct_test', exchange_type='direct')

    # 生成随机队列
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    severities = ['error', '']

    # 将随机队列与routing_key关键字以及exchange进行绑定
    for severity in severities:
        channel.queue_bind(exchange='direct_test', queue=queue_name, routing_key=severity)

    print (' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))

    # 接收消息
    channel.basic_consume(callback, queue=queue_name, no_ack=True)
    channel.start_consuming()

def producer():
    channel = connection.channel()
    # 定义交换机名称以及类型
    channel.exchange_declare(exchange='direct_test', exchange_type='direct')

    severity = 'error'
    message = '123'
    # 发布消息至交换机direct_test, 且发布的消息携带的关键字routing_key是info
    channel.basic_publish(exchange='direct_test', routing_key=severity, body=message)

    print(" [x] Sent %r:%r" % (severity, message))

    connection.close()


if __name__ == '__main__':
    # consumer()
    producer()