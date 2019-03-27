# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: techweb.py
  Desc: TechWeb（http://www.techweb.com.cn/）
  Author: CoderPig
  Date: 2019/3/27 0027 20:41
-------------------------------------------------
"""
from news import News, MongodbClient
from tools import user_agents, str_handle
import requests as r
from pyquery import PyQuery

index_url = 'http://www.techweb.com.cn/'
roll_url = index_url + 'roll/'
headers = {
    'User-Agent': user_agents.random_user_agent(),
    'Host': str_handle.remove_url_scheme(index_url)[:-1],
    'Referer': roll_url,
}


def fetch_news():
    news_list = []
    resp = r.get(roll_url, headers=headers)
    if resp is not None:
        resp.encoding = 'utf8'
        pq = PyQuery(resp.text)
        lis = pq('div.newslist > ul >li')
        for li in lis.items():
            if li.attr('class') != 'line':
                a = li('span.tit > a')
                news_list.append(News(
                    _id=a.attr('href').split('/')[-1].replace('.shtml', ''),
                    url=a.attr('href'),
                    title=a.text(),
                    origin=li('span.column').text() + '|' + li('span.source').text(),
                    update_time=li('span.time').text()
                ).to_dict())
    return news_list


if __name__ == '__main__':
    client = MongodbClient('techweb')
    client.insert_many(fetch_news())
