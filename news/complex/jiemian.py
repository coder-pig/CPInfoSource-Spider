# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: jiemian.py
  Desc: 界面新闻（https://www.jiemian.com/）
  Author: CoderPig
  Date: 2019/3/27 0027 21:28
-------------------------------------------------
"""

import requests as r

from news import News, MongodbClient
from tools import user_agents
from pyquery import PyQuery
import json
import re

ajax_url = 'https://a.jiemian.com/index.php'
headers = {
    'User-Agent': user_agents.random_user_agent(),
    'Referer': 'https://www.jiemian.com/lists/4.html'
}
title_extract_pattern = re.compile('【(.*?)】 (.*。)', re.S)


def fetch_news(page):
    news_list = []
    resp = r.get(ajax_url, params={'m': 'lists', 'a': 'ajaxNews', 'cid': 4, 'page': page}, headers=headers)
    print('爬取：', resp.url)
    if resp is not None:
        resp.encoding = 'utf8'
        rst = json.loads(resp.text[1:-1])['rst']
        pq = PyQuery(rst)
        news_item = pq('div.item-news')
        for item in news_item.items():
            a_url = item('div > p > a').attr('href')
            item_main = title_extract_pattern.search(item('div.item-main').text())
            if item_main is not None:
                news_list.append(News(
                    _id=a_url.split('/')[-1].replace('.html', ''),
                    url=a_url,
                    title=item_main.group(1),
                    overview=item_main.group(2),
                    publish_time=item('div.item-date').text()
                ).to_dict())
    return news_list


if __name__ == '__main__':
    client = MongodbClient('jiemian')
    client.insert_many(fetch_news(1))
    client.insert_many(fetch_news(2))
    print("界面新闻爬取完毕！")
