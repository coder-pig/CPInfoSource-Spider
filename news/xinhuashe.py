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

xhs_url = 'http://www.news.cn/'
xhs_jj_url = 'http://www.news.cn/xhjj.htm'  # 新华聚焦
xhs_gd_url = 'http://www.gd.xinhuanet.com/'  # 新华广东频道
xhs_headers = {
    'Referer': xhs_url,
    'Host': str_handle.remove_url_scheme(xhs_url)[:-1],
    'User-Agent': user_agents.random_user_agent()
}


# 爬取新华聚焦
def fetch_xh_focus():
    resp = r.get(xhs_jj_url, headers=xhs_headers)
    resp.encoding = 'utf-8'
    bs = BeautifulSoup(resp.text, 'lxml')
    data_list = bs.findAll("ul", attrs={'class': 'dataList'})[1]
    lis = data_list.findAll("li")
    news_list = []



# 爬取广东新闻
def fetch_gd_news():
    pass


if __name__ == '__main__':
    fetch_xh_focus()
