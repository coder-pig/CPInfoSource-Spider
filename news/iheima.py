# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: iheima.py
  Desc: i黑马（http://www.iheima.com/）
  Author: CoderPig
  Date: 2019/3/26 0026 16:56
-------------------------------------------------
"""
import requests as r
import time

from news import News, MongodbClient
from tools import str_handle, user_agents

iheima_url = 'http://www.iheima.com/'
iheima_headers = {
    'Referer': iheima_url,
    'Host': str_handle.remove_url_scheme(iheima_url)[:-1],
    'User-Agent': user_agents.random_user_agent(),
    'X-Requested-With': 'XMLHttpRequest'
}


def fetch_iheima_news():
    page = 1
    news_list = []
    while True:
        resp = r.get(iheima_url, params={'page': page, 'pagesize': 20}, headers=iheima_headers)
        print("爬取：", resp.url)
        if resp is not None:
            resp_json = resp.json()
            contents = resp_json['contents']
            for content in contents:
                # 只抓取12个小时以内的新闻
                if int(round(time.time())) - int(
                        time.mktime(time.strptime(content['published'], "%Y-%m-%d %H:%M"))) > 43200:
                    return news_list
                else:
                    news_list.append(News(
                        _id=content['contentid'],
                        title=content['title'],
                        url=iheima_url[:-1] + content['url'],
                        image=content['thumb'],
                        publish_time=content['published'],
                        origin=content['author'],
                        overview=content['description']
                    ).to_dict())
            page += 1


if __name__ == '__main__':
    client = MongodbClient('iheima')
    client.insert_many(fetch_iheima_news())
