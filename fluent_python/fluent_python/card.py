# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :2018/11/27 14:23
# @Author   :zhong
# @Software :PyCharm
# 卡牌类


import collections

# 初始化类的对象
Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck():
    # 扑克牌的等级 A 2 3 .. J Q K
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    # 花色 -- spades黑桃、diamonds红心、clubs梅花、hearts方块
    suits = 'spades diamonds clubs hearts'.split()
    # 细节点：
    # split默认是以空格作为分隔符

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    # len(x) 如果x是内置的类型，比如列表(list)、字符串(str)、字节序列(byteArray)、等，那么CPython会抄个近路，
    # __len__实际上会直接返回PyVarObject里的ob_size属性，PyVarObject是表示内存中长度可变的内置对象的C语言结构体
    # 直接读取这个值比调用一个方法要快很多。
    def __len__(self):
        return len(self._cards)

    def __getitem__(self, item):
        return self._cards[item]

    def random_card(self):
        from random import choice
        return choice(self._cards)




import collections




if __name__ == '__main__':
    deck = FrenchDeck()
    # print (len(deck))       # -- __len__ 提供
    #
    # print (deck[0])         # -- __getitem__ 提供
    # print (deck[-1])
    #
    # print (deck.random_card())  # 随机返回卡片

    # 排序
    suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)
    def spades_high(card):
        # 获取值的索引  index
        rank_value = FrenchDeck.ranks.index(card.rank)
        # 牌号*花色 + 花色的值 = 这张牌的权重值
        return rank_value*len(suit_values) + suit_values[card.suit]
    # 从小到大 sorted
    for card in sorted(deck, key=spades_high):
        print (card)