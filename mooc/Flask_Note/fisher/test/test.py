# -*- coding:utf-8 -*-
from flask import Flask, current_app


app = Flask(__name__)

# 应用上下文 对象 Flask
# 请求上下文 对象 Request
# Flask APPContext
# Request RequestContext
# -----------------------------------
# 需要入栈，代理才可以栈中寻找到
ctx = app.app_context()
ctx.push()  # 入栈

a = current_app
d = current_app.config['DEBUG']
ctx.pop()   # 出栈

# ------------------------------------
'''
为什么我们实际使用代理的时候，又不用推入栈了呢？

在实际上路由进行请求的时候，request会把Request context -> Request 推入(push)到(通过_request_ctx_stack) 栈中

注：
    1. 在推入的过程中，会先去 App context -> app 对应的栈中检查 app是否在栈顶中
    2. 如果不在栈顶中，则会先把 App context -> app 对象推入 (push) 到 (通过_app_ctx_stack) 栈中
    3. 这个时候，外部直接使用current_app(代理app)的时候，栈中已经存在app。所以实际使用的时候，app是不用入栈的。
'''