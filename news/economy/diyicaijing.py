# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: diyicaijing.py
  Desc: 第一财经杂志（https://www.cbnweek.com/）
  Author: CoderPig
  Date: 2019/3/26 0026 17:51
-------------------------------------------------
"""
import requests as r

from news import News, MongodbClient
from tools import str_handle, user_agents
from bs4 import BeautifulSoup
import re

url_extract_pattern = re.compile('\((https://.*?)\)', re.S)
msg_extract_pattern = re.compile('(.*?)#News(.*?)(\d+月\d+日)阅读时长\d+分钟.*?', re.S)

diyicaijing_url = 'https://www.cbnweek.com/'
diyicaijing_headers = {
    'Referer': diyicaijing_url,
    'Host': str_handle.remove_url_scheme(diyicaijing_url)[:-1],
    'User-Agent': user_agents.random_user_agent(),
    'x-document-type': 'fragment'
}


def fetch_diyicaijing_news():
    news_list = []
    resp = r.get(diyicaijing_url, params={'page': 2}, headers=diyicaijing_headers)
    print("爬取", resp.url)
    bs = BeautifulSoup(resp.text, 'lxml')
    articles = bs.findAll('article', attrs={'class': 'article-item clearfix'})
    for article in articles:
        detail_url = diyicaijing_url[:-1] + article.a['href']
        if not detail_url.endswith('subscribe'):
            news_content = article.div.text.replace(' ', '').replace('\n', '')
            text_result = msg_extract_pattern.findall(news_content)
            if text_result is not None:
                for content in text_result:
                    news_list.append(News(
                        _id=detail_url.split('/')[-1],
                        url=detail_url,
                        image=url_extract_pattern.search(article.a['style']).group(1),
                        origin=content[0],
                        title=content[1],
                        publish_time=content[2],
                    ).to_dict())
    return news_list


if __name__ == '__main__':
    client = MongodbClient('diyicaijing')
    client.insert_many(fetch_diyicaijing_news())
    print("第一财经爬取完毕！")