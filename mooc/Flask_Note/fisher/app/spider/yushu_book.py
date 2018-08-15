# -*- coding:utf-8 -*-
from app.libs.http_ import HTTP
from flask import current_app

class YuShuBook():
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={q}&start={start}&count={count}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = HTTP.get(url)
        self.__fill_single(result)

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def search_by_keyword(self, keyword, page=1):
        url = self.keyword_url.format(q=keyword, start=self.calculate_start(page), count=current_app.config['PER_PAGE'])
        result = HTTP.get(url)
        self.__fill_collection(result)

    def __fill_collection(self, data):
        self.total = data['total']
        self.books = data['book']

    def calculate_start(self, page):
        return (page - 1) * current_app.config['PER_PAGE']