# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: chuangyebang.py
  Desc: 创业邦（https://www.cyzone.cn/）
  Author: CoderPig
  Date: 2019/3/27 0027 17:12
-------------------------------------------------
"""

import requests as r
from pyquery import PyQuery

from news import News, MongodbClient
from tools import user_agents, str_handle

index_url = 'https://www.cyzone.cn/'
category_url = index_url + 'category/8/'

headers = {
    'User-Agent': user_agents.random_user_agent(),
    'Host': str_handle.remove_url_scheme(index_url)[:-1],
    'Referer': index_url,
}


def fetch_news():
    news_list = []
    resp = r.get(category_url, headers=headers)
    resp.encoding = 'utf8'
    print('爬取：', resp.url)
    if resp is not None:
        pq = PyQuery(resp.text)
        divs = pq('div.lfn-bar')
        for div in divs.items():
            a = div('div.lfn-title > a')
            form = div('div > div > div > span.form').text()
            url = 'https:' + a.attr('href')
            news_list.append(News(
                _id=url.split('/')[-1].replace('.html', ''),
                url=url,
                title=a.text(),
                overview=div('div.lfn-des').text(),
                publish_time=div('div > div > div > span.time').text(),
                origin=form if form != '' else None
            ).to_dict())
    return news_list


if __name__ == '__main__':
    client = MongodbClient('chuangyebang')
    client.insert_many(fetch_news())
    print("创业邦爬取完毕!")
