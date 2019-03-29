# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: jueshengwang.py
  Desc: 决胜网（http://www.juesheng.com/）
  Author: CoderPig
  Date: 2019/3/29 0029 16:56
-------------------------------------------------
"""

from news import News, MongodbClient
from tools import str_handle, user_agents
import requests as r
import time
from pyquery import PyQuery
import json
import re

index_url = 'http://www.juesheng.com/'
load_more_url = index_url + 'site/home/get_news.json'
headers = {
    'Host': str_handle.remove_url_scheme(index_url)[:-1],
    'User-Agent': user_agents.random_user_agent(),
}
index_data_extract_pattern = re.compile('VAR.theNewsList = (\[.*?\]) \|\|', re.S)
more_data_extract_pattern = re.compile('(.*?)--==|html|==--', re.S)
count_time = int(round(time.time() * 1000))


def fetch_index_news():
    news_list = []
    sort_field = ''
    resp = r.get(index_url, headers=headers)
    print("爬取：", resp.url)
    if resp is not None:
        data_result = index_data_extract_pattern.search(resp.text)
        if data_result is not None:
            data_json = data_result.group(1)
            data_dict = json.loads(data_json)
            for data in data_dict:
                news_list.append(News(
                    _id=data['id'],
                    title=data['title'],
                    overview=data['brief'],
                    image=data['thumb'],
                    publish_time=data['time'],
                    url=data['url'],
                    origin=data['columnName']
                ).to_dict())
                sort_field = data['sort_field']
    return news_list, sort_field


def fetch_more_news(min_id):
    news_list = []
    sort_field = ''
    resp = r.get(load_more_url, params={'_render': '', 'min_id': min_id, '_': count_time}, headers=headers)
    print("爬取：", resp.url)
    if resp is not None:
        data_result = more_data_extract_pattern.search(resp.text)
        if data_result is not None:
            data_json = data_result.group(1)
            data_dict = json.loads(data_json)
            for data in data_dict['data']['list']:
                news_list.append(News(
                    _id=data['id'],
                    title=data['title'],
                    overview=data['brief'],
                    image=data['thumb'],
                    publish_time=data['time'],
                    url=data['url'],
                    origin=data['columnName']
                ).to_dict())
                sort_field = data['sort_field']
    return news_list, sort_field


if __name__ == '__main__':
    client = MongodbClient('jueshengwang')
    result = fetch_index_news()
    client.insert_many(result[0])
    count_time -= 1
    min_id = result[1]
    while True:
        result = fetch_more_news(min_id)
        client.insert_many(result[0])
        if int(round(time.time())) - int(result[0][-1]['publish_time']) < 432000:
            count_time -= 1
            min_id = result[1]
            continue
        else:
            break
