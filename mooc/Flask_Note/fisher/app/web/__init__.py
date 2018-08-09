# -*-coding:utf-8 -*-
from flask.blueprints import Blueprint

web = Blueprint('web', __name__)

# 不导入的话，在使用对应的文件的是，里面的web是不会生效的。路由也就是不会生效的
from app.web import book
from app.web import user