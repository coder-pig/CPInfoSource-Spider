# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File     : zgjj.py
   Author   : CoderPig
   date     : 2019/5/9 0009 14:56
   Desc     : 中国经济网（http://www.ce.cn/）
-------------------------------------------------
"""
import re
from bs4 import BeautifulSoup
import requests as r
from news import News, MongodbClient
from tools import str_handle, user_agents
from tools.str_handle import format_current

index_url = 'http://www.ce.cn/'
# 提取url的正则
news_node_pattern = re.compile('<a.*?href="(.*?)".*?>(.*?)</a>')
# 提取新闻id的正则
id_extract_pattern = re.compile("(.*?).shtml", re.S)
# 今天的日期
today_date = format_current('%Y%m/%d')

headers = {
    'Referer': index_url,
    'Host': str_handle.remove_url_scheme(index_url)[:-1],
    'User-Agent': user_agents.random_user_agent(),
}


def fetch_web_news():
    resp = r.get(index_url, headers=headers)
    resp.encoding = 'gbk'  # 设置编码b
    bs = BeautifulSoup(resp.text, 'lxml')
    a_bs = bs.find_all("a")
    news_list = []
    for a in a_bs:
        href = a.get('href')
        if href is not None and a.text != '':
            if today_date in href and href.endswith('.shtml'):
                id_result = id_extract_pattern.search(href.split('/')[-1])
                news_list.append(
                    News(
                        _id=id_result.group(1),
                        title=a.text,
                        url=href,
                        origin='中国经济网'
                    ).to_dict()
                )
    return news_list


if __name__ == '__main__':
    client = MongodbClient('zgjj')
    client.insert_many(fetch_web_news())
    print("中国经济网数据爬取完毕!")
