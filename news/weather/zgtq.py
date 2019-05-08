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
from news import News, MongodbClient
from tools import str_handle, user_agents
from tools.str_handle import format_current

index_url = 'http://news.weather.com.cn/'
# 提取天气信息的正则
weather_news_pattern = re.compile("c1:'(.*?)',c2:'(.*?)',c3:'(.*?)',c4:'(.*?)',c5:'(.*?)',c6:'(.*?)'", re.S)
# 提取新闻id的正则
id_extract_pattern = re.compile("(.*?).shtml", re.S)
# 今天的日期
today_date = format_current('%Y-%m-%d')

headers = {
    'Referer': index_url,
    'Host': str_handle.remove_url_scheme(index_url)[:-1],
    'User-Agent': user_agents.random_user_agent(),
}


def fetch_web_news():
    resp = r.get(index_url, headers=headers)
    resp.encoding = 'utf8'  # 设置编码
    weather_news_list = weather_news_pattern.findall(resp.text)
    news_list = []
    for weather_news in weather_news_list:
        if weather_news[4] == today_date:
            id_result = id_extract_pattern.search(weather_news[1].split('/')[-1])
            news_list.append(
                News(
                    _id=id_result.group(1),
                    title=weather_news[0],
                    url=weather_news[1],
                    image=weather_news[2],
                    origin=weather_news[3],
                    publish_time=weather_news[4] + ' ' + weather_news[5]
                ).to_dict()
            )
        else:
            break
    return news_list


if __name__ == '__main__':
    client = MongodbClient('zgtq')
    client.insert_many(fetch_web_news())
    print("中国天气网数据爬取完毕!")
