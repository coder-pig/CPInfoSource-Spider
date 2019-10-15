# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: dongmaiwang.py
  Desc: 动脉网（https://vcbeat.net/）
  Author: CoderPig
  Date: 2019/3/29 0029 11:13
-------------------------------------------------
"""
import json
import re
import time

import requests as r

from news import News, MongodbClient
from tools import str_handle, user_agents

index_url = 'https://dynview.vcbeat.top'
ajax_url = index_url + '/dg/list'
news_detail_url = index_url + '/newsDetail/'
headers = {
    'User-Agent': user_agents.random_user_agent(),
    'Content-Type': 'application/json'
}
ajax_params = {"days": "", "type": [], "s_time": "", "e_time": "", "demostic": "", "address_id": [],
               "is_tj": "", "group_id": [], "dynview_tag_ids": [], "entity_uids": [], "entity_ids": []}


def fetch_news(page):
    news_list = []
    ajax_params['page'] = page
    ajax_params['latest_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    resp = r.post(ajax_url, data=json.dumps(ajax_params), headers=headers)
    if resp is not None:
        res = resp.json()
        for i in res['res']:
            news_list.append(News(
                _id=i['id'],
                title=i['title'],
                overview=i['content'],
                publish_time=i['create_time'],
                origin=i['src_name'],
                url=news_detail_url + i['uid']
            ).to_dict())
    return news_list


if __name__ == '__main__':
    client = MongodbClient('dongmaiwang')
    cur_page = 1
    while True:
        print("爬取第%d页" % cur_page)
        result_list = fetch_news(cur_page)
        client.insert_many(result_list)
        if int(round(time.time())) - int(
                time.mktime(time.strptime(result_list[-1]['publish_time'], "%Y-%m-%d %H:%M:%S"))) < 43200:
            cur_page += 1
            continue
        else:
            break
    print("动脉网爬取完毕!")

