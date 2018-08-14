# -*- coding:utf-8 -*-
from flask import Flask
from app.models.book import db

def create_app():

    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)

    #
    # db.init_app(app)    # 默认去config里面加载对应的mysql的链接，可以看源代码
    # db.create_all(app=app)
    return app


def register_blueprint(app_):
    from app.web.book import web
    app_.register_blueprint(web)