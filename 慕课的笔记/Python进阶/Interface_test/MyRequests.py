# -*- coding:utf-8 -*-
import requests
from Interface_test.Filed import *


class MetaClass(type):

    def __new__(cls, name, bases, attr):
        fields = {}
        className = name
        for key, value in attr.items():
            if isinstance(value, Filed):
               fields[key] = value
        attr['fields'] = fields
        attr['className'] = className
        return super().__new__(cls, name, bases, attr)


class BaseModel(metaclass=MetaClass):

    def __init__(self, *args, **kwargs):

        for key, value in kwargs.items():
            if self.fields.get(key, None) is not None:
                setattr(self, key, value)
            else:
                raise KeyError("'{className}' object has no attribute '{key}'".format(className=self.className,key=key))

        session_bool = kwargs.get('session', None)
        if session_bool is not None:
            if session_bool is True:
                self.re = requests.session()
            else:
                self.re = requests
        else:
            self.re = requests

        super().__init__()


class MyRequests(BaseModel):

    url = CharFile()
    method = MethodFile()
    session = BoolFile()    # 默认不开启
    headers = DictFile()


        
if __name__ == '__main__':
    r = MyRequests(url='1',method='post')