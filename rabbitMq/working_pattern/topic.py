# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :2018/11/26 10:56
# @Author   :zhong
# @Software :PyCharm

# topic的工作原理
# 路由键模糊匹配，其实是路由键（routint_key）的扩展，就是可以使用正则表达式，和常用的正则表达式不同，这里的话
# #：表示所有、全部的意思； *：只匹配到一个词

# 任何发送到topic Exchange的消息都会呗转发到所有关系routing_key中指定话题的queue上
#   1. 这种模式较为复杂，简单来说，就是每个队列都有其关心的主题，所有的消息都带有一个标题（routing_key），Exchange会将消息转发到
#       所有关注主题能与routing_key模糊匹配的队列。
#   2. 这种模式需要routing_key，也许要提前绑定exchange和queue
#   3. 在进行绑定时，需提供一个该队列关心的主题，如 "#.log." 表示该队列关系所有涉及log的消息（一个routing_key为 “MQ.log.error”的
#       消息会被转发该队列）
#   4. # 表示0个或者若干个关键字， * 表示一个关键字。 如 “log.warn”匹配, 无法与“log.warn.timeout”匹配；
#       但“log.#”能与上述两者进行匹配
#   5. 同样，如果exchange没有发现能够与routing_key匹配的Queue，则会抛弃此信息