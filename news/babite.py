# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: babite.py
  Desc: 巴比特（https://www.8btc.com）
  Author: CoderPig
  Date: 2019/3/29 0029 14:28
-------------------------------------------------
"""
import time

import requests as r

from news import News, MongodbClient
from tools import user_agents

index_url = 'https://www.8btc.com/'
load_more_url = 'https://webapi.8btc.com/bbt_api/news/list'
article_url = index_url + 'article/'
headers = {
    'User-Agent': user_agents.random_user_agent(),
}


def fetch_news(page):
    news_list = []
    resp = r.get(load_more_url, params={'page': page, 'num': 20}, headers=headers)
    print("抓取：", resp.url)
    if resp is not None:
        data = resp.json()['data']['list']
        for d in data:
            news_list.append(News(
                _id=d['id'],
                title=d['title'],
                overview=d['desc'],
                publish_time=d['post_date'],
                image=d['image'],
                origin=d['author_info']['name'],
                url=article_url + str(d['id'])
            ).to_dict())
    return news_list


if __name__ == '__main__':
    client = MongodbClient('babite')
    cur_page = 1
    while True:
        result_list = fetch_news(cur_page)
        client.insert_many(result_list)
        last_publish_time = result_list[-1]['publish_time']
        if int(round(time.time())) - int(last_publish_time) < 43200:
            cur_page += 1
            continue
        else:
            break
