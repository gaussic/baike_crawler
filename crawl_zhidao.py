#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from utils import crawl_html_doc
from utils_zhidao import insert_question_url
from urllib import parse

zhidao_search_url = 'https://zhidao.baidu.com/search?ie=gbk&site=-1&sites=0&date=0&'


def crawl_insert_by_keyword(keyword):
    pn = 0
    while True:
        try:
            word = parse.urlencode({'word': keyword, 'pn': pn * 10}, encoding='gbk')
            url = zhidao_search_url + word
            soup = crawl_html_doc(url, encoding='gbk')
            cnt = 0
            for dl in soup.find(id='wgt-list').select("dl"):
                text = dl.find('a').text
                href = dl.find('a')['href']
                if not text.startswith('http://www.zybang.com'):
                    q_u = {
                        'keyword': keyword,
                        'question': text,
                        'url': href
                    }
                    insert_question_url(q_u)
                    cnt += 1
            print(str(cnt) + '--' * 50 + str(pn + 1))
            pn += 1
            if len(soup.select('a.pager-next')) == 0:
                break
        except Exception as e:
            print(e)


if __name__ == '__main__':
    crawl_insert_by_keyword('自然')
