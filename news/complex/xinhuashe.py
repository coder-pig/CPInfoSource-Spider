# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: xinhuashe.py
  Desc: 新华社（http://www.news.cn/）
  Author: CoderPig
  Date: 2019/3/22 0022 17:26
-------------------------------------------------
"""
import requests as r
from news import News
from news import MongodbClient
from tools import str_handle, user_agents
from bs4 import BeautifulSoup
import re
import time

xhs_url = 'http://www.news.cn/'
xhs_jj_url = 'http://www.news.cn/xhjj.htm'  # 新华聚焦
xhs_gd_url = 'http://www.gd.xinhuanet.com/'  # 新华广东频道
xhs_gd_host = 'www.gd.xinhuanet.com'
xhs_headers = {
    'Referer': xhs_url,
    'Host': str_handle.remove_url_scheme(xhs_url)[:-1],
    'User-Agent': user_agents.random_user_agent()
}
xhs_news_id_pattern = re.compile("c_(\d+).htm", re.S)  # 提取新闻id的正则


# 爬取新华聚焦
def fetch_xh_focus():
    news_list = []
    resp = r.get(xhs_jj_url, headers=xhs_headers)
    resp.encoding = 'utf-8'
    bs = BeautifulSoup(resp.text, 'lxml')
    data_list = bs.findAll("ul", attrs={'class': 'dataList'})[1]
    lis = data_list.findAll("li")
    for li in lis:
        a = li.h3.a
        news_id_result = xhs_news_id_pattern.search(a['href'])
        if news_id_result is not None:
            news_list.append(News(_id=news_id_result.group(1),
                                  url=a['href'],
                                  title=a.text,
                                  publish_time=li.span.text).to_dict())
    return news_list


# 爬取广东新闻
def fetch_gd_news():
    news_list = []
    xhs_headers['Host'] = xhs_gd_host
    resp = r.get(xhs_gd_url, headers=xhs_headers)
    resp.encoding = 'utf-8'
    bs = BeautifulSoup(resp.text, 'lxml')
    data_list = bs.find("ul", attrs={'class': 'gallery l-list-selected l-m'})
    lis = data_list.findAll('li')
    for li in lis:
        l_cbox = li.find('div', attrs={'class': 'l-cbox'})
        spans = l_cbox.find('div', attrs={'class': 'l-foot-par'}).findAll('span')
        news_id_result = xhs_news_id_pattern.search(li.a['href'])
        if news_id_result is not None:
            # 判断新闻的发布时间与当前时间的时间间隔，只保存12个小时以内的新闻
            publish_time = spans[1].text.replace('\n', '').strip()
            if int(round(time.time())) - int(time.mktime(time.strptime(publish_time, "%Y-%m-%d %H:%M:%S"))) < 43200:
                news_list.append(News(
                    _id=news_id_result.group(1),
                    url=li.a['href'],
                    title=li.a.img['alt'],
                    image=xhs_gd_url + li.a.img['src'],
                    origin=spans[0].text,
                    publish_time=publish_time,
                    overview=l_cbox.p.text
                ).to_dict())
    return news_list


if __name__ == '__main__':
    client = MongodbClient('xinhuashe')
    client.insert_many(fetch_xh_focus())
    client.insert_many(fetch_gd_news())