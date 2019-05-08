# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: test.py
  Desc: 字符串处理相关
  Author: CoderPig
  Date: 2019/3/22 0022 14:46
-------------------------------------------------
"""
import time


# 移除协议头
def remove_url_scheme(url):
    results = url.split('://')
    return results[-1] if results is not None else None


# 获得当前时间格式化后的字符串
def format_current(fm):
    return time.strftime(fm, time.localtime(time.time()))
