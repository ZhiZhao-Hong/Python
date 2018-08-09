# -*- coding:utf-8 -*-
from http_ import HTTP


class YuShuBook():

    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={q}&start={start}&count={count}'

    @classmethod
    def search_by_isbn(cls, isbn):
        url = cls.isbn_url.format(isbn)
        result = HTTP.get(url)
        return result

    @classmethod
    def search_by_keyword(cls, keyword, count=15, start=0):
        url = cls.keyword_url.format(q=keyword, start=start, count=count)
        result = HTTP.get(url)
        return result