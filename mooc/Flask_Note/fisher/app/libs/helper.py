# -*- coding:utf-8 -*-

def is_isbn_or_key(word):
    """
    判断word是否属于isbn类型
    :param word:字符串
    :return:如果是isbn，直接返回isbn，否则返回key
    """
    isbn_or_key = 'key'
    if len(word) == 13 and word.isdigit():
        isbn_or_key = 'isbn'
    short_word = word.replace('-', '')
    # if判断也会影响整体的性能，应该先把最大可能出现异常的代码放在前面
    if '-' in word and len(short_word) == 10 and short_word.isdigit():
        isbn_or_key = 'isbn'
    return isbn_or_key