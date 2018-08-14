# -*- coding:utf-8 -*-
from flask import jsonify, request
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from app.web import web
from app.forms.book import SearchForm
from app.view_models.book import BookViewModel, BookCollection

'''
测试使用的url

http://localhost:81/book/search/郭敬明
http://t.yushu.im/v2/book/isbn/9787501524044

http://locahlost:81/book/search/9787501524044/1
http://locahlost:81/book/search?q=9787501524044&page=1
http://locahlost:81/book/search?q=9787501524044

http://t.yushu.im/v2/book/search?q=9787501524044
'''


@web.route('/book/search_1/<q>/<page>')
def search_1(q, page):
    """
    api_1 : http://t.yushu.im/v2/book/search?q={}&start={}&count={}
    api_2 : http://t.yushu.im/v2/book/isbn/{isbn}
    :q:  普通关键字查询/isbn查询
    :page:
    :return:
    """
    # isbn13  13个0-9的数字组成
    # isbn10 10个0-9的数字组成，含有一些 '-'

    # 写在这里，代码不可以重用，一眼也看不出什么问题
    # isbn_or_key = 'key'
    # if len(q) == 13 and q.isdigit():
    #     isbn_or_key = 'isbn'
    # short_q = q.replace('-', '')
    # # if判断也会影响整体的性能，应该先把最大可能出现异常的代码放在前面
    # if '-' in q and len(short_q)== 10 and short_q.isdigit():
    #     isbn_or_key = 'isbn'

    # -----------------
    # 这样写比较简洁点 - 尽量保证视图函数简洁易懂的，因为这里是了解业务的地方，尽量保证简单易懂
    # isbn_or_key = is_isbn_or_key(q)
    # if isbn_or_key == 'isbn':
    #     # 导入快捷键  alt + enter
    #     result = YuShuBook.search_by_isbn(q)
    # else:
    #     result = YuShuBook.search_by_keyword(q)
    # # return json.dumps(result), 200, {"content-type": "application/json"}  这个是python内部的方法
    # # flask 的方法
    # return jsonify(result)


@web.route('/book/search')
def search():

    # q = request.args['q']
    # # 至少要有一个字符，长度限制
    # page = request.args['page']
    # # 正整数，也要有一个最大值的限制
    # # 如何验证数据？
    # ---------------------------------------
    form = SearchForm(request.args)
    book = BookCollection()
    # 验证一下数据是否符合我们的设定的验证层
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()
        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
            # result = YuShuBook.search_by_isbn(q)
            # result = BookViewModel.package_single(result, q)
        else:
            yushu_book.search_by_keyword(q)
            # result = YuShuBook.search_by_keyword(q, page)
            # result = BookViewModel.package_collection(result, q)
        # return jsonify(result)
        book.fill(yushu_book, q)
        return jsonify(book)
    else:
        # return jsonify(form.errors)
        return jsonify