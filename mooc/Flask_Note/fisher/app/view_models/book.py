# -*- coding:utf-8 -*-

# 基于下面的优化版本
class BookViewModel():

    def __init__(self, book):
        self.title = book["title"]
        self.publisher = book["publisher"]
        self.pages = book["pages"] or ''
        self.author = '、'.join(book["author"])
        self.price = book["price"]
        self.summary = book["summary"] or ''
        self.image = book["image"]

class BookCollection():

    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]

class _BookViewModel():
    """因为两种查询方式返回的结果不一致，应该把返回的结果的数据格式定位一致的"""
    """
    什么是类：
        1. 描述特征 (类变量、实例变量)
        2. 行为 (方法)
    """
    @classmethod
    def package_single(cls, data, keyword):
        # 单个查询的裁剪 - single 单一的
        returned = {
            "books": [],
            "total": 0,
            "keyword": keyword
        }
        if data:
            returned["total"] = 1
            returned["books"] = [cls.__cut_book_data(data)]
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        # 多个查询的裁剪
        returned = {
            "books": [],
            "total": 0,
            "keyword": keyword
        }
        if data:
            returned["total"] = data["total"]
            returned['books'] = [cls.__cut_book_data(book) for book in data["books"]]
        return returned

    @staticmethod
    def __cut_book_data(data):
        book = {
            "title": data["title"],
            "publisher": data["publisher"],
            "pages": data["pages"] or '',
            "author": '、'.join(data["author"]),
            "price": data["price"],
            "summary": data["summary"] or '',
            "image": data["image"]
        }
        return book