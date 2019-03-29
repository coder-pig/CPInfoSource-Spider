# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: diyidiandong.py
  Desc: 第一电动（https://www.d1ev.com/）
  Author: CoderPig
  Date: 2019/3/29 0029 15:35
-------------------------------------------------
"""

import time
import requests as r
import re
from news import News, MongodbClient
from tools import user_agents, str_handle
from pyquery import PyQuery

index_url = 'https://www.d1ev.com/'
news_flash_url = index_url + 'newsflash'
headers = {
    'User-Agent': user_agents.random_user_agent(),
    'Host': str_handle.remove_url_scheme(index_url)[:-1],
    'Referer': news_flash_url
}


def fetch_news(page):
    news_list = []
    resp = r.get('{}/list-{}'.format(news_flash_url, page), headers=headers)
    print("爬取：", resp.url)
    if resp is not None:
        pq = PyQuery(resp.text)
        news = pq('div.ws-newsflash-list01')
        for n in news.items():
            a = n('a')
            news_list.append(News(
                _id=a.attr('href').split('/')[-1],
                url=index_url + a.attr('href'),
                title=a('h5').text(),
                overview=n('div.ws-newsflash-content').text().replace("【查看原文】", ''),
                publish_time=n('div > div > time').text()
            ).to_dict())
    return news_list


if __name__ == '__main__':
    client = MongodbClient('diyidiandong')
    cur_page = 1
    while True:
        result_list = fetch_news(cur_page)
        client.insert_many(result_list)
        last_publish_time = result_list[-1]['publish_time']
        if int(round(time.time())) - int(time.mktime(time.strptime(last_publish_time, "%Y-%m-%d %H:%M"))) < 43200:
            cur_page += 1
            continue
        else:
            break

