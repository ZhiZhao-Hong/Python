# -*- coding:utf-8 -*-
from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):

    id = Column(Integer, primary_key=True, autoincrement=True)  #自增长
    title = Column(String(length=50), nullable=False)
    author = Column(String(length=30), default='未名')
    binging = Column(String(20))        # 精装还是瓶装
    publisher = Column(String(50))      # 出版社
    price = Column(String(20))
    pages = Column(Integer)             # 页数
    pubdate = Column(String(20))        # 出版年月
    isbn = Column(String(15), nullable=False, unique=True)  # 唯一不能重复
    summary = Column(String(1000))      # 简介
    image = Column(String(50))