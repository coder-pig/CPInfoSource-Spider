# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: huanqiulvxun.py
  Desc: 环球旅讯（https://www.traveldaily.cn/）
  Author: CoderPig
  Date: 2019/3/29 0029 16:35
-------------------------------------------------
"""
import requests as r
from pyquery import PyQuery
from news import News, MongodbClient
from tools import user_agents, str_handle
import re

index_url = 'https://www.traveldaily.cn/'
today_url = index_url + 'today/'

headers = {
    'User-Agent': user_agents.random_user_agent(),
    'Host': str_handle.remove_url_scheme(index_url)[:-1],
    'referer': today_url
}

# 提取多少个小时前的正则
hours_pattern = re.compile(r'(\d+)小时前', re.S)


def fetch_news(page):
    news_list = []
    resp = r.get('{}{}/'.format(today_url, page), headers=headers)
    print("抓取：", resp.url)
    if resp is not None:
        resp.encoding = 'utf8'
        pq = PyQuery(resp.text)
        for li in pq('ul.main-wrap > li').items():
            url = index_url + li('div.childR > p > a').attr('href')
            img = li('div > a > img')
            news_list.append(News(
                _id=url.split('/')[-1],
                url=url,
                title=img.attr('alt'),
                overview=li('div.childR > p > a').text(),
                image=index_url[:-1] + img.attr('src'),
                publish_time=li('div.childR > div.time').text()
            ).to_dict())
    return news_list


if __name__ == '__main__':
    client = MongodbClient('huanqiulvxun')
    cur_page = 1
    while True:
        result_list = fetch_news(cur_page)
        client.insert_many(result_list)
        last_publish_time = result_list[-1]['publish_time']
        if '分钟前' in last_publish_time:
            cur_page += 1
            continue
        elif '小时前' in last_publish_time:
            hours_before = hours_pattern.search(last_publish_time)
            if hours_before is not None:
                if int(hours_before.group(1)) < 12:
                    cur_page += 1
                    continue
                else:
                    break
            else:
                break
        else:
            break
    print("环球旅讯爬取完毕!")
