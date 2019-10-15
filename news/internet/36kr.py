# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: 36kr.py
  Desc: 36Kr（https://36kr.com/）
  Author: CoderPig
  Date: 2019/3/27 0027 11:52
-------------------------------------------------
"""
from news import News, MongodbClient
from tools import str_handle, user_agents
import requests as r
import re
import json
import time

index_url = 'https://36kr.com/'
web_news_url = index_url + 'information/web_news/'
news_detail_base_url = index_url + 'p/'
load_more_base_url = index_url + 'pp/api/aggregation-entity'
headers = {
    'Referer': index_url,
    'Host': str_handle.remove_url_scheme(index_url)[:-1],
    'User-Agent': user_agents.random_user_agent(),
}

extract_data_pattern = re.compile('window.initialState=(\{.*?\})\<\/script\>', re.S)  # 首页提取数据的正则
last_pos_id = ''  # 加载更多用的id
data_list = []


# 提取首页数据
def fetch_web_news():
    resp = r.get(web_news_url, headers=headers).text
    result = extract_data_pattern.search(resp)
    if result is not None:
        news_list = []
        json_dict = json.loads(result.group(1))
        information_list = json_dict['information']['informationList']
        for information in information_list:
            post = information['post']
            motifs = post['motifs']
            motifs_name = motifs[0]['name'] if motifs is not None else ''
            news_list.append(News(
                _id=str(information['id']),
                title=post['title'],
                url=news_detail_base_url + str(post['id']),
                image=post['cover'],
                publish_time=post['published_at'],
                overview=post['summary'],
                origin=post['user']['name'] + '|' + motifs_name
            ).to_dict())
        return news_list, news_list[-1]['_id']


# 加载更多
def fetch_web_news_more(start_id):
    global data_list
    headers['Referer'] = web_news_url
    resp = r.get(load_more_base_url, params={'type': 'web_latest_article', 'b_id': start_id, 'per_page': 30},
                 headers=headers)
    print("抓取：", resp.url)
    if resp is not None:
        resp_json = resp.json()
        items = resp_json['data']['items']
        for item in items:
            post = item['post']
            motifs = post['motifs']
            motifs_name = motifs[0]['name'] if motifs is not None else ''
            data_list.append(News(
                _id=str(item['id']),
                title=post['title'],
                url=news_detail_base_url + str(post['id']),
                image=post['cover'],
                publish_time=post['published_at'],
                overview=post['summary'],
                origin=post['user']['name'] + '|' + motifs_name
            ).to_dict())
        if int(round(time.time())) - int(
                time.mktime(time.strptime(items[-1]['post']['published_at'], "%Y-%m-%d %H:%M:%S"))) > 86400:
            return None
        else:
            return fetch_web_news_more(items[-1]['id'])


if __name__ == '__main__':
    result_list, end_id = fetch_web_news()
    fetch_web_news_more(end_id)
    client = MongodbClient('36Kr')
    client.insert_many(result_list)
    client.insert_many(data_list)
    print("36kr爬取完毕!")
