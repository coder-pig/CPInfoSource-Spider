# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: test.py
  Desc: 字符串处理相关
  Author: CoderPig
  Date: 2019/3/22 0022 14:46
-------------------------------------------------
"""


# 移除协议头
def remove_url_scheme(url):
    results = url.split('://')
    return results[-1] if results is not None else None
