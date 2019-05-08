# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: lianshangwang.py
  Desc: 联商网（http://www.linkshop.com.cn）
  Author: CoderPig
  Date: 2019/3/28 0028 11:44
-------------------------------------------------
"""
from news import News, MongodbClient
from tools import str_handle, user_agents
import requests as r
import time

index_url = 'http://www.linkshop.com.cn/'
news_url = index_url + 'news/'
ajax_url = index_url + 'Web/News_Index.aspx'

headers = {
    'Host': str_handle.remove_url_scheme(index_url)[:-1],
    'Origin': index_url,
    'Referer': news_url,
    'User-Agent': user_agents.random_user_agent(),
    'X-Requested-With': 'XMLHttpRequest'
}


def fetch_news(page):
    news_list = []
    resp = r.get(ajax_url, params={'isAjax': 1, 'action': 'zixun_zx', 'pageNo': page, 'tab': 'zx'}, headers=headers)
    print("抓取：", resp.url)
    if resp is not None:
        data = resp.json()['Data']
        if data is not None:
            for d in data:
                news_list.append(News(
                    _id=d['ID'],
                    title=d['Title'],
                    image=d['PicUrl'],
                    overview=d['abstract'],
                    origin=d['Key'],
                    url=index_url + d['APage'],
                    publish_time=d['updatetime']
                ).to_dict())
    return news_list


if __name__ == '__main__':
    cur_page = 1
    client = MongodbClient('lianshangwang')
    while True:
        result_list = fetch_news(cur_page)
        client.insert_many(result_list)
        if int(round(time.time())) - int(
                time.mktime(time.strptime(result_list[-1]['publish_time'], "%Y/%m/%d %H:%M:%S"))) < 43200:
            cur_page += 1
            continue
        else:
            break
