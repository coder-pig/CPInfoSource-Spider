# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: bianews.py
  Desc: BiaNews（https://www.bianews.com/）
  Author: CoderPig
  Date: 2019/3/29 0029 13:52
-------------------------------------------------
"""
from news import News, MongodbClient
from tools import str_handle, user_agents
import requests as r
from pyquery import PyQuery
import time
import re
import json

index_url = 'https://www.bianews.com/'
ajax_url = index_url + 'news/news_list?channel=flash&type=1'
flash_url = index_url + 'news/flash?'
news_flash_url = index_url + 'news-flash/flash'
headers = {
    'Host': str_handle.remove_url_scheme(index_url)[:-1],
    'User-Agent': user_agents.random_user_agent(),
    'Origin': index_url,
    'Referer': flash_url,
    'X-Requested-With': 'XMLHttpRequest'
}


def fetch_news(page):
    news_list = []
    resp = r.post(ajax_url, data={'page_no': page, 'page_size': 15, 'search': ''})
    print("抓取：", resp.url)
    if resp is not None:
        resp.encoding = 'utf8'
        pq = PyQuery(resp.text)
        lis = pq('li')
        for li in lis.items():
            news_list.append(News(
                _id=li('div.share_btn > a').attr('id'),
                title=li('div > div.title').text(),
                overview=li('div > div.content').text().replace('\n', '').strip(),
                publish_time=li('div > div.pub_time').attr('data-time'),
                url="{}?id={}".format(flash_url, li('div.share_btn > a').attr('id'))
            ).to_dict())
    return news_list


if __name__ == '__main__':
    client = MongodbClient('bianews')
    cur_page = 1
    while True:
        result_list = fetch_news(cur_page)
        client.insert_many(result_list)
        last_publish_time = result_list[-1]['publish_time']
        if int(round(time.time() * 1000)) - int(last_publish_time) < 43200000:
            cur_page += 1
            continue
        else:
            break
    print("bianews爬取完毕!")