# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File     : xlkj.py
   Desc     : 新浪科技（https://tech.sina.com.cn/）
   Author   : CoderPig
   date     : 2019/7/12 0012 上午 11:32
-------------------------------------------------
"""

import random
import time

import requests as r

from news import News, MongodbClient
from tools import str_handle, user_agents

index_url = 'https://tech.sina.com.cn/'
data_base_url = 'https://cre.mix.sina.com.cn/api/v3/get'

# 新闻分类
category_key_dict = {
    'nt_home_tech_news': '产业',
    'nt_home_tech_chuangshiji': '创事纪',
    'nt_home_tech_mobil': '手机',
    'nt_home_tech_digi': '数码',
    'nt_home_tech_discovery': '探索',
    'nt_home_tech_chuangye': '创业',
}

headers = {
    'Host': str_handle.remove_url_scheme(index_url)[:-1],
    'User-Agent': user_agents.random_user_agent(),
    'Origin': index_url,
    'Referer': index_url,
}


def fetch_news(category):
    news_list = []
    for i in range(0, 2):
        resp = r.get(data_base_url, params={"cre": "tianyi", "mod": category, "_": int(round(time.time() * 1000)),
                                            "offset": 20 * i}, headers=headers)
        print('爬取：', resp.url)
        if resp is not None:
            resp_json = resp.json()
            data = resp_json['data']
            for d in data:
                news_list.append(News(
                    _id=d['uuid'],
                    title=d['title'],
                    overview=d['intro'],
                    image=d['thumb'],
                    publish_time=d['ctime'],
                    origin=d['author'],
                    url=d['url_https']
                ).to_dict())
        time.sleep(random.randint(0, 2))
    return news_list


if __name__ == '__main__':
    client = MongodbClient('xlkj')
    for i in category_key_dict.keys():
        client.insert_many(fetch_news(i))
        time.sleep(random.randint(0, 2))
    print("新浪科技爬取完毕！")
