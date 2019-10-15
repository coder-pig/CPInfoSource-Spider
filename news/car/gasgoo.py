# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: gasgoo.py
  Desc: 盖世汽车资讯（http://auto.gasgoo.com）
  Author: CoderPig
  Date: 2019/3/29 0029 14:41
-------------------------------------------------
"""

import json
import re
import time

import requests as r

from news import News, MongodbClient
from tools import user_agents

index_url = 'http://auto.gasgoo.com/'
ajax_url = index_url + 'Home.aspx/GetHomeList'
headers = {
    'User-Agent': user_agents.random_user_agent(),
    'Content-Type': 'application/json'
}
post_params = {"classIds": "103,106,107,108,109,110,303,409,501,601", "tagIds": "",
               "articleIdsRemove": "0,70132766,70132771,70132769,0,0,0", "pageSize": "25"}


def fetch_news(page):
    news_list = []
    post_params['pageIndex'] = page
    resp = r.post(ajax_url, headers=headers, data=json.dumps(post_params))
    if resp is not None:
        d = resp.json()['d']
        for i in d:
            news_list.append(News(
                _id=i['ArticleId'],
                title=i['Title'],
                overview=i['BriefContent'],
                url=index_url[:-1] + i['LinkUrl'],
                publish_time=i['IssueTime'],
            ).to_dict())
    return news_list


if __name__ == '__main__':
    client = MongodbClient('gasgoo')
    cur_page = 1
    while True:
        print("爬取第%d页" % cur_page)
        result_list = fetch_news(cur_page)
        client.insert_many(result_list)
        last_publish_time = result_list[-1]['publish_time']
        if int(round(time.time())) - int(time.mktime(time.strptime(last_publish_time, "%Y-%m-%d %H:%M:%S"))) < 43200:
            cur_page += 1
            continue
        else:
            break
    print("盖世汽车资讯爬取完毕!")
