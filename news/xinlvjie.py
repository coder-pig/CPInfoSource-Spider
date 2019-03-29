# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: xinlvjie.py
  Desc: 
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
        data_list = pq('div#data_list')
        for div in data_list('div.li').items():
            img = div('a > img')
            shuoming = div('div > p.shuoming')
            news_list.append(News(
                _id=div('a').attr('href').split('/')[-1].replace('.html', ''),
                title=img.attr('alt'),
                overview=div('div > p.listCont > a').text(),
                image=img.attr('src'),
                publish_time=shuoming('span.time.meta-date').text(),
                origin=shuoming('span.meta-befrom').text(),
                url=div('a').attr('href')
            ).to_dict())
    return news_list


if __name__ == '__main__':
    client = MongodbClient('xinlvjie')
    client.insert_many(fetch_news())
