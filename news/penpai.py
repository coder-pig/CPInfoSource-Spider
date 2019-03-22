# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: test.py
  Desc: 澎湃新闻（https://www.thepaper.cn/）
  Author: CoderPig
  Date: 2019/3/22 0022 14:46
-------------------------------------------------
"""

import requests as r
import re
from lxml import etree
from tools import str_handle, user_agents
import time
import random
from news import News
from news import MongodbClient

penpai_url = 'https://www.thepaper.cn/'
penpai_ajax_url = 'https://www.thepaper.cn/load_chosen.jsp?'
penpai_headers = {
    'referer': penpai_url,
    'Host': str_handle.remove_url_scheme(penpai_url)[:-1],
    'User-Agent': user_agents.random_user_agent()
}

# 提取topCids的正则
cids_pattern = re.compile('&topCids=(.*?)&', re.S)
# 提取新闻信息的正则
news_pattern = re.compile(
    r'<a href="(.*?)".*?img src="(.*?)" alt="(.*?)".*?<p>(.*?)</p>.*?pdtt_trbs".*?<a.*?>'
    r'(.*?)</a>.*?<span>(.*?)</span>', re.S)


def fetch_penpai_news():
    news_list = []  # 新闻列表
    # 提取首页的新闻数据
    index_resp = r.get(penpai_url).text
    index_html = etree.HTML(index_resp)
    news_urls = index_html.xpath('//div[@class="news_li"]/div[@class="news_tu"]/a')  # 新闻链接
    imgs_urls = index_html.xpath('//div[@class="news_li"]/div[@class="news_tu"]/a/img')  # 新闻图片
    overviews = index_html.xpath('//div[@class="news_li"]/p')  # 新闻简介
    times = index_html.xpath('//div[@class="pdtt_trbs"]/span[1]')  # 新闻时间
    origins = index_html.xpath('//div[@class="pdtt_trbs"]/a')  # 新闻来源
    for i in range(0, int(len(news_urls) / 2)):
        news_list.append(News(_id=news_urls[i].get('href').split('_')[-1],
                              title=imgs_urls[i].get('alt'),
                              overview=overviews[i].text.replace('\n', '').replace(' ', ''),
                              url=penpai_url + news_urls[i].get('href'),
                              image='http:' + imgs_urls[i].get('src'),
                              publish_time=times[i].text,
                              origin=origins[i].text).to_dict())
    # 正则提取topCids
    topCids = ''
    ids = cids_pattern.search(index_resp)
    if topCids is not None:
        topCids = ids.group(1)
    # 设置Ajax请求头
    ajax_params = {
        'nodeids': 25949,
        'topCids': '2840959,2840504,2840804,2841177,',
    }
    pageidx = 2
    while True:
        ajax_params['pageidx'] = pageidx
        ajax_params['lastTime'] = int(round(time.time() * 1000))
        resp = r.get(penpai_ajax_url, params=ajax_params, headers=penpai_headers)
        resp_content = resp.text
        print("爬取：", resp.url)
        results = news_pattern.findall(resp_content)
        for result in results:
            if result[5] == '1天前':
                return news_list
            else:
                news_list.append(News(_id=result[0].split('_')[-1],
                                      title=result[2],
                                      overview=result[3].replace('\n', '').replace(' ', ''),
                                      url=penpai_url + result[0],
                                      image='http:' + result[1],
                                      publish_time=result[5],
                                      origin=result[4]).to_dict())
        pageidx += 1
        time.sleep(random.randint(0, 2))


if __name__ == '__main__':
    client = MongodbClient('penpai')
    data_list = fetch_penpai_news()
    client.insert_many(data_list)
