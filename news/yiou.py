# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: yiou.py
  Desc: 亿欧（https://www.iyiou.com/）
  Author: CoderPig
  Date: 2019/3/27 0027 16:18
-------------------------------------------------
"""
import re

import requests as r
from pyquery import PyQuery

from news import News, MongodbClient
from tools import user_agents

base_url = 'https://www.iyiou.com/breaking/'
headers = {
    'User-Agent': user_agents.random_user_agent()
}


def fetch_news(url):
    news_list = []
    resp = r.get(url, headers=headers)
    print("抓取：", resp.url)
    if resp is not None:
        pq = PyQuery(resp.text)
        a_s = pq('.newsFlashListWrap > div > ul > li > a')
        for item in a_s.items():
            news_list.append(News(
                _id=item.attr('href').split('/')[-1].replace('.html', ''),
                url=item.attr('href'),
                title=item('span.fl').text(),
                publish_time=item('span.fr').text()
            ).to_dict())
        return news_list


if __name__ == '__main__':
    client = MongodbClient('yiou')
    for i in range(1, 3):
        client.insert_many(fetch_news("{}p{}.html".format(base_url, i)))
