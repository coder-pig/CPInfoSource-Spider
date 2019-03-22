# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: test.py
  Desc: 新闻类
  Author: CoderPig
  Date: 2019/3/22 0022 14:46
-------------------------------------------------
"""

import time
from collections import OrderedDict


class News:
    def __init__(self, _id, title=None, overview=None, url=None, image=None, publish_time=None, origin=None,
                 create_time=int(round(time.time() * 1000)), update_time=None):
        self._id = _id    # 新闻id
        self.title = title  # 新闻标题
        self.overview = overview  # 新闻概述
        self.url = url  # 新闻链接
        self.image = image  # 新闻配图
        self.publish_time = publish_time  # 新闻发布时间
        self.origin = origin  # 新闻来源
        self.create_time = create_time  # 新闻创建时间
        self.update_time = update_time  # 新闻更新时间

    def to_dict(self):
        news_dict = OrderedDict()
        news_dict['_id'] = self._id
        news_dict['title'] = self.title
        news_dict['overview'] = self.overview
        news_dict['url'] = self.url
        news_dict['image'] = self.image
        news_dict['publish_time'] = self.publish_time
        news_dict['origin'] = self.origin
        news_dict['create_time'] = self.create_time
        news_dict['update_time'] = self.update_time
        return news_dict

