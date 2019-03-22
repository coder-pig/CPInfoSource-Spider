# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: mongodb_client.py
  Desc: 封装mongodb相关操作
  Author: CoderPig
  Date: 2019/3/22 0022 15:06
-------------------------------------------------
"""

from pymongo import MongoClient, errors
from config_getter import get_config


class MongodbClient:
    def __init__(self, name):
        self.name = name
        self.client = MongoClient(get_config('DB', 'host'), int(get_config('DB', 'port')))
        self.db = self.client[get_config('DB', 'DBName')]

    def insert_many(self, data):
        # ordered=false跳过插入错误的文档，不中断插入操作，然后对插入重复值异常进行捕获
        try:
            self.db[self.name].insert_many(data, ordered=False)
        except errors.BulkWriteError as e:
            print(e)
