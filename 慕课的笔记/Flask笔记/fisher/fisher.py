# -*- coding:utf-8 -*-
from flask import Flask, make_response




app = Flask(__name__)
# 配置配置文件 - 配置文件的key都要写大写
app.config.from_object('config')
# print(app.config['DEBUG'])

# 路由
@app.route('/hello/')
def hello():
    # /hello/ 网页输入/hello会重定向过去 /hello/
    # 重定向的时候，第一次请求的response - headers - location 会有
    # 基于类的视图(即插视图) - 可以复印(可以自己查询)

    # ---------------------------------------------------
    # response 第一种写法
    headers = {
        'content-type': "application/json",
        "location": "https://cn.bing.com"
    }
    # response = make_response('<html></html>', 200)
    # response.headers = headers
    # return response

    # ----------------------------------------------------
    # response 第二种写法
    return '<html></html>', 301, headers

    # 返回的类型和值 - response对象
    # status code
    # content-type http headers
    # content-type的默认格式是：text/html

# 第二种路由注册方式 - 基于类的视图一般都是第二种
# app.add_url_rule('/hello', view_func=hello)


if __name__ == '__main__':
    # debug=True 就会自动重启，不然修改代码是不会自动重启的，性能比较差
    # host 可以直接指定地址 0.0.0.0 可以指定外网
    # port 可以指定端口
    # config 是dict的一个子类
    # 其他环境的时候，有可能入口不是这个入口，一定要是这个文件启动，才可以启动服务器
    app.run(host='0.0.0.0', debug=app.config["DEBUG"], port=81)