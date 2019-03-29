# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: gasgoo.py
  Desc: 盖世汽车资讯（http://auto.gasgoo.com）
  Author: CoderPig
  Date: 2019/3/29 0029 14:41
-------------------------------------------------
"""

import time

import requests as r
import re

from news import News, MongodbClient
from tools import user_agents, str_handle
from pyquery import PyQuery

index_url = 'http://auto.gasgoo.com/'
page_base_url = index_url + 'auto-news/C-101-102-103-104-105-106-501-601/'
headers = {
    'User-Agent': user_agents.random_user_agent(),
    'Host': str_handle.remove_url_scheme(index_url)[:-1]
}
id_extract_pattern = re.compile("(.*?).shtml", re.S)  # 提取新闻id的正则


def fetch_news(page):
    news_list = []
    resp = r.get(page_base_url + str(page), headers=headers)
    print("爬取：", resp.url)
    if resp is not None:
        pq = PyQuery(resp.text)
        content = pq('div.content')
        for c in content.items():
            a = c('h2 > a')
            id_result = id_extract_pattern.search(a.attr('href').split('/')[-1])
            if id_result is not None:
                news_list.append(News(
                    _id=id_result.group(1),
                    title=a.text(),
                    overview=c('dl > dd > p').text(),
                    origin=c('div.feedCard > div.cardTags > a').text(),
                    image=c('dl > dt > a > img').attr('src'),
                    url=a.attr('href'),
                    publish_time=c('div.feedCard > div.cardTime').text(),
                ).to_dict())
    return news_list


if __name__ == '__main__':
    client = MongodbClient('gasgoo')
    cur_page = 1
    while True:
        result_list = fetch_news(cur_page)
        client.insert_many(result_list)
        last_publish_time = result_list[-1]['publish_time']
        if int(round(time.time())) - int(time.mktime(time.strptime(last_publish_time, "%Y-%m-%d %H:%M:%S"))) < 43200:
            cur_page += 1
            continue
        else:
            break
