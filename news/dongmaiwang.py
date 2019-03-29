# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: dongmaiwang.py
  Desc: 动脉网（https://vcbeat.net/）
  Author: CoderPig
  Date: 2019/3/29 0029 11:13
-------------------------------------------------
"""
from news import News, MongodbClient
from tools import str_handle, user_agents
import requests as r
import time
import re
import json

index_url = 'https://vcbeat.net/'
ajax_url = index_url + 'Index/Index/ajaxGetArticleList'
headers = {
    'Host': str_handle.remove_url_scheme(index_url)[:-1],
    'User-Agent': user_agents.random_user_agent(),
    'Origin': index_url,
    'Referer': index_url,
    'X-Requested-With': 'XMLHttpRequest'
}

# 提取多少个小时前的正则
hours_pattern = re.compile(r'(\d+)小时前', re.S)


def fetch_news(page):
    news_list = []
    resp = r.get(ajax_url, params={'page': page, 'industry_class': ''}, headers=headers)
    print("抓取：", resp.url)
    if resp is not None:
        resp_str = resp.text
        if resp_str.startswith(u'\ufeff'):
            resp_str = resp_str.encode('utf8')[3:].decode('utf8')
            data = json.loads(resp_str)['data']
            for d in data:
                news_list.append(News(
                    _id=d['detail_id'],
                    title=d['title'],
                    overview=d['summary'],
                    image=index_url + d['logo_path'],
                    publish_time=d['publish_time'],
                    origin=d['categoryName'] + '|' + d['authorName'],
                    url=index_url + d['detail_id']
                ).to_dict())
    return news_list


if __name__ == '__main__':
    client = MongodbClient('dongmaiwang')
    cur_page = 1
    while True:
        result_list = fetch_news(cur_page)
        client.insert_many(result_list)
        last_publish_time = result_list[-1]['publish_time']
        if '分钟前' in last_publish_time:
            cur_page += 1
            continue
        elif '小时前' in last_publish_time:
            hours_before = hours_pattern.search(last_publish_time)
            if hours_before is not None:
                if int(hours_before.group(1)) < 12:
                    cur_page += 1
                    continue
                else:
                    break
            else:
                break
        else:
            break
