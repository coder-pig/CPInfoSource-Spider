# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File     : txty.py
   Desc     : 腾讯体育首页要闻(https://sports.qq.com/)
   Author   : CoderPig
   date     : 2019/7/12 0012 下午 02:58
-------------------------------------------------
"""
import random
import time

import requests as r
from bs4 import BeautifulSoup

from news import News, MongodbClient
from tools import str_handle, user_agents

index_url = "https://sports.qq.com/"

headers = {
    'Host': str_handle.remove_url_scheme(index_url)[:-1],
    'User-Agent': user_agents.random_user_agent(),
}


def fetch_news():
    news_list = []
    resp = r.get(index_url, headers=headers)
    print("抓取：", resp.url)
    if resp is not None:
        bs = BeautifulSoup(resp.text, 'lxml')
        data_list = bs.find_all("div", attrs={"class": "scr-newsarea"})[0]
        a_s = data_list.find_all("a")
        cur = 1
        for a in a_s:
            news_list.append(News(
                _id=cur,
                title=a['title'],
                origin="腾讯体育",
                url=a['href']
            ).to_dict())
            cur += 1
    return news_list


if __name__ == '__main__':
    client = MongodbClient('txty')
    client.insert_many(fetch_news())
