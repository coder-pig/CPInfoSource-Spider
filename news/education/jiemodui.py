# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: jiemodui.py
  Desc: 芥末堆（https://www.jiemodui.com/）
  Author: CoderPig
  Date: 2019/3/28 0028 14:37
-------------------------------------------------
"""
from news import News, MongodbClient
from tools import str_handle, user_agents
import requests as r
import time

index_url = 'https://www.jiemodui.com/'
ajax_url = index_url + '/Api/Index/news'
detail_url = index_url + 'N/'

headers = {
    'Host': str_handle.remove_url_scheme(index_url)[:-1],
    'Referer': index_url,
    'User-Agent': user_agents.random_user_agent(),
    'X-Requested-With': 'XMLHttpRequest'
}


def fetch_news(page):
    news_list = []
    resp = r.get(ajax_url, params={'p': page}, headers=headers)
    print("抓取：", resp.url)
    if resp is not None:
        data = resp.json()['list']
        if data is not None:
            for d in data:
                news_list.append(News(
                    _id=d['id'],
                    title=d['name'],
                    image=d['picture'],
                    overview=d['brief'],
                    origin=d['writer'],
                    url=detail_url + d['id'] + '.html',
                    publish_time=d['rPtime']
                ).to_dict())
    return news_list


if __name__ == '__main__':
    cur_page = 1
    client = MongodbClient('jiemodui')
    while True:
        result_list = fetch_news(cur_page)
        client.insert_many(result_list)
        if int(round(time.time())) - int(
                time.mktime(time.strptime(result_list[-1]['publish_time'], "%Y-%m-%d %H:%M:%S"))) < 43200:
            cur_page += 1
            continue
        else:
            break
