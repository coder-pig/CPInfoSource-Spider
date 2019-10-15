# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: xinlvjie.py
  Desc: 新旅界（http://www.lvjie.com.cn/）
  Author: CoderPig
  Date: 2019/3/29 0029 15:57
-------------------------------------------------
"""
import requests as r
from pyquery import PyQuery

from news import News, MongodbClient
from tools import user_agents, str_handle

index_url = 'http://www.lvjie.com.cn/'

headers = {
    'User-Agent': user_agents.random_user_agent(),
    'Host': str_handle.remove_url_scheme(index_url)[:-1],
}


def fetch_news():
    news_list = []
    resp = r.get(index_url, headers=headers)
    print("抓取：", resp.url)
    if resp is not None:
        resp.encoding = 'utf8'
        pq = PyQuery(resp.text)
        data_list = pq('ul#date-list-ul')
        for li in data_list('li').items():
            img = li('a > img')
            print(li('p').text())
            news_list.append(News(
                url=li('a').attr('href'),
                _id=li('a').attr('href').split('/')[-1].replace('.html', ''),
                title=img.attr('alt'),
                image=img.attr('src'),
                overview=li('div#list-t p#list-abs').text(),
                publish_time=li('div#list-t > p#list-sm span:first').text(),
                origin=li('div#list-t > p#list-sm > span:last').text(),
            ).to_dict())
    return news_list


if __name__ == '__main__':
    client = MongodbClient('xinlvjie')
    client.insert_many(fetch_news())
    print("新旅社爬取完毕!")
