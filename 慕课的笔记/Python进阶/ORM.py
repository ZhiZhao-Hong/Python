# -*- coding:utf-8 -*-
import numbers

class File():
    pass

class IntFile(File):

    def __init__(self, db_column, min_value=None, max_value=None):
        self._value = None
        self._min_value = min_value
        self._max_value = max_value
        self._db_column = db_column

        if min_value is not None:
            if not isinstance(min_value,numbers.Integral):
                raise ValueError("min_value must be int")
            elif min_value < 0:
                raise ValueError("min_value must be positive int")

        if max_value is not None:
            if not isinstance(max_value,numbers.Integral):
                raise ValueError("max_value must be int")
            elif max_value < 0:
                raise ValueError("max_value must be positive int")

        if min_value is not None and max_value is not None:
            if min_value > max_value:
                raise ValueError("min_value must be smaller than max_value")


    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        if not isinstance(value, numbers.Integral):
            raise ValueError("int value need")
        if value < self._max_value or value > self._max_value:
            raise ValueError("value must between minvalue and max_value")
        if self._min_value > self._max_value:
            raise ValueError("min_value must be smaller than max_value")
        self._value = value

class CharField(File):

    def __init__(self, db_column, max_length=None):
        self._value = None
        self._db_column = db_column
        self._max_length = max_length

        if max_length is None:
            raise ValueError("you must spcify max_lenth for CharFiled")

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        if not isinstance(value,str):
            raise ValueError('string value need')
        if len(value) > self._max_length:
            raise ValueError('value len excess len of max_length')
        self._value = value

class ModelMetaClass(type):

    def __new__(cls, name, bases, attrs, **kwargs):
        fields = {}
        for key,value in attrs.items():
            if isinstance(value,File):


class User(metaclass=ModelMetaClass):

    name = CharField(db_column="", max_length=10)
    age = CharField(db_column="", min_vakue=0, max_length=10)

    class Meta():
        db_table = "user"


if __name__ == '__main__':
    user = User()
    user.name = "bobby"
    user.age = 28
    user.save()