# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :1/4/2019 4:52 PM
# @Author   :zhong
# @Software :PyCharm
import warnings
from Meta import osconfeed


DB_NAME = 'data/schedule1_db'
CONFERENCE = 'conference.115'


class Record:

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def load_db(db):
    raw_data = osconfeed.load()
    warnings.warn('loading ' + DB_NAME)
    for collection, rec_list in raw_data["Schedule"].items():
        record_type = collection[:-1]
        for record in rec_list:
            key = '{}.{}'.format(record_type, record['serial'])
            db[key] = Record(**record)
