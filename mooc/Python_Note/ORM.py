# -*- coding:utf-8 -*-
import numbers


class File():
    pass


class IntFile(File):

    def __init__(self, db_column, min_value=None, max_value=None):
        self._value = None
        self._min_value = min_value
        self._max_value = max_value
        self.db_column = db_column

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
        if value < self._min_value or value > self._max_value:
            raise ValueError("value must between minvalue and max_value")
        if self._min_value > self._max_value:
            raise ValueError("min_value must be smaller than max_value")
        self._value = value


class CharField(File):

    def __init__(self, db_column, max_length=None):
        self._value = None
        self.db_column = db_column
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

    def __new__(cls, name, bases, attrs):
        if name == "BaseModel":
            return super().__new__(cls, name, bases, attrs)

        fields = {} # 拿到和数据表所有相关的列
        for key, value in attrs.items():
            if isinstance(value,File):
                fields[key] = value
        attrs_meta = attrs.get("Meta", None)
        _meta = {}
        db_table = name.lower()
        if attrs_meta is not None:
            table = getattr(attrs_meta, "db_table", None)
            if table is not None:
                db_table = table
        _meta['db_table'] = db_table

        attrs["_meta"] = _meta
        attrs["fields"] = fields
        del attrs['Meta']
        return super().__new__(cls, name, bases, attrs)

class BaseModel(metaclass=ModelMetaClass):

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        super().__init__()

    def save(self):
        fields = []
        values = []
        for key, value in self.fields.items():
            db_column = value.db_column #value 是CharFiled对象或者IntFiled对象
            if db_column is not None:
                db_column = key.lower()
            fields.append(db_column)
            value = getattr(self, key)
            values.append(str(value))

        sql = "insert {db_table}({fields}) value({value})".format(
            db_table = self._meta["db_table"],
            fields = ",".join(fields),
            value = ','.join(values)
        )
        print (sql)

class User(BaseModel):
    name = CharField(db_column="", max_length=10)
    age = IntFile(db_column="", min_value=0, max_value=100)

    class Meta():
        db_table = "user"


if __name__ == '__main__':
    user = User(name='booby2',age=28)
    # user.name = "bobby"
    # user.age = 28
    user.save()