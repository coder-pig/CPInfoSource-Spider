# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: jingmeiti.py
  Desc: 鲸媒体（http://www.jingmeiti.com/）
  Author: CoderPig
  Date: 2019/3/28 0028 14:49
-------------------------------------------------
"""
import time

from news import News, MongodbClient
from tools import str_handle, user_agents
import requests as r
from pyquery import PyQuery
import re

index_url = 'http://www.jingmeiti.com/'

headers = {
    'Host': str_handle.remove_url_scheme(index_url)[:-1],
    'User-Agent': user_agents.random_user_agent(),
}

# 提取多少个小时前的正则
hours_pattern = re.compile(r'(\d+)小时前', re.S)


def fetch_news(page):
    news_list = []
    resp = r.get('{}page/{}'.format(index_url, page), headers=headers)
    print("抓取：", resp.url)
    if resp is not None:
        pq = PyQuery(resp.text)
        content = pq('div.posts-default-img')
        for c in content.items():
            a = c('a')
            news_list.append(News(
                _id=a.attr('href').split('/')[-1],
                url=a.attr('href'),
                title=a.attr('title'),
                image=a('img').attr('src'),
                overview=c.parent('div .posts-default-content > div.posts-text').text(),
                origin=c.parent('div .posts-default-content > div.posts-default-info > ul > li.ico-cat').text(),
                publish_time=c.parent('div .posts-default-content > div.posts-default-info > ul > li.ico-time').text()
            ).to_dict())
    return news_list


if __name__ == '__main__':
    cur_page = 1
    client = MongodbClient('jingmeiti')
    while True:
        result_list = fetch_news(cur_page)
        client.insert_many(result_list)
        publish_time = result_list[-1]['publish_time']
        if '小时前' in publish_time:
            hours_before = hours_pattern.search(result_list[-1]['publish_time'])
            print(hours_before)
            if hours_before is not None:
                if int(hours_before.group(1)) > 12:
                    break
                else:
                    cur_page += 1
                    continue
        else:
            break
