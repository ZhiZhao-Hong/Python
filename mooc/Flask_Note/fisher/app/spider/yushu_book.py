# -*- coding:utf-8 -*-
from app.libs.http_ import HTTP
from flask import current_app

class YuShuBook():
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={q}&start={start}&count={count}'

    @classmethod
    def search_by_isbn(cls, isbn):
        url = cls.isbn_url.format(isbn)
        result = HTTP.get(url)
        return result

    @classmethod
    def search_by_keyword(cls, keyword, page=1):
        url = cls.keyword_url.format(q=keyword, start=cls.calculate_start(page), count=current_app.config['PER_PAGE'])
        result = HTTP.get(url)
        return result

    @staticmethod
    def calculate_start(page):
        return (page - 1) *current_app.config['PER_PAGE']