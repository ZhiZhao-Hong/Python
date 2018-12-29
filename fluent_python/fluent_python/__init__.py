# -*- coding:utf-8 -*-

class Iterable:

    def __init__(self):
        self.value = [1,2,3,4]

    def __iter__(self):
        return Iterator(self.value)


class Iterator:

    def __init__(self, value):
        self.value = value
        self.index = 0

    def __next__(self):
        try:
            number = self.value[self.index]
        except IndexError:
            raise StopIteration()
        else:
            self.index += 1
        return number

def iterable():
    for i in range(0, 4):
        yield i


class Iterable1:

    def __init__(self):
        self.value = [1,2,3,4]

    def __iter__(self):
        for i in self.value:
            yield i


def simple_coroutine():
    print('-> coroutine started')
    x = yield
    print('-> coroutine received:', x)


def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total/total

