#!/usr/bin/python
# -*- coding:utf-8 -*-

from utils import crawl_html_doc, query_keywords_one_category, insert_keywords_detail
from datetime import datetime


def crawl_one_keyword(keyword):
    soup = crawl_html_doc('http://baike.baidu.com/item/' + keyword)
    if len(soup.select('ul.para-list')) != 0:
        new_url = 'http://baike.baidu.com' + soup.select('div.para')[0].find('a')['href']
        soup = crawl_html_doc(new_url)
    return soup.select('div.lemma-summary')[0].text.strip()


def crawl_keywords_one_category(category):
    big_keyword = query_keywords_one_category(category)
    for keyword in big_keyword['keywords']:
        try:
            detail = crawl_one_keyword(keyword)
            keyword_dict = {
                'keyword': keyword,
                'description': detail,
                'category': category,
                'upd_time': datetime.now()
            }
            insert_keywords_detail(keyword_dict)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # detail = crawl_one_keyword('天堂')
    # print(detail)
    crawl_keywords_one_category('人物')
