# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File     : zgtq.py
   Author   : CoderPig
   date     : 2019/5/8 0008 17:58
   Desc     : 中国天气网（http://news.weather.com.cn/）
-------------------------------------------------
"""
import re
import requests as r
import json
from news import News, MongodbClient
from tools import str_handle, user_agents
from tools.str_handle import format_current

index_url = 'http://news.weather.com.cn/'
data_url = 'http://www.weather.com.cn/pubm/news2019_more_list10.htm'
# 提取新闻id的正则
id_extract_pattern = re.compile("(.*?).shtml", re.S)
# 提取新闻json的正则
json_extract_pattern = re.compile("jsonpcallback\((.*?)\)", re.S)
# 今天的日期
today_date = format_current('%Y-%m-%d')

headers = {
    'Referer': index_url,
    'Host': str_handle.remove_url_scheme(index_url)[:-1],
    'User-Agent': user_agents.random_user_agent(),
}


def fetch_web_news():
    resp = r.get(data_url, headers=headers)
    resp.encoding = 'utf8'  # 设置编码
    json_result = json_extract_pattern.search(resp.text);
    if json_result is not None:
        json_news = json_result.group(1)
        sites = json.loads(json_news)['sites']
        news_list = []
        for site in sites:
            if site['c5'] == today_date:
                id_result = id_extract_pattern.search(site['c2'].split('/')[-1])
                news_list.append(
                    News(
                        _id=id_result.group(1),
                        title=site['c1'],
                        url=site['c2'],
                        image=site['c3'],
                        origin=site['c4'],
                        publish_time=site['c5'] + ' ' + site['c6']
                    ).to_dict()
                )
            else:
                break
        return news_list


if __name__ == '__main__':
    client = MongodbClient('zgtq')
    client.insert_many(fetch_web_news())
    print("中国天气网数据爬取完毕!")
