#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils import crawl_html_doc
import json

keyword_set = set()


def parse_sub_keywords(soup):
    """解析一页中的所有词条"""
    all_key = soup.select('div.p-entry')[0].find_all('li')
    keywords = []
    for ps in all_key:
        cat = [a.text for a in ps.select('div.text > a')]
        keywords.append({'title': ps.select('a.title')[0].text,
                         'desc': ps.select('p.content-abstract')[0].text,
                         'category': cat})
    return keywords


def parse_sub_keywords_short(soup):
    """解析一页中的所有词条，仅保留词条"""
    a_list = soup.select('a.title')
    sub_keys = []
    for a in a_list:
        if a.text in keyword_set:
            continue
        keyword_set.add(a.text)
        sub_keys.append(a.text)
    return sub_keys


def crawl_keyword_by_category(category):
    """抓取一个分类下显示的所有词条"""
    keyword_set.clear()
    soup = crawl_html_doc('http://baike.baidu.com/fenlei/' + category)
    all_keywords = []

    # 顶部轮播热点
    hot_content = soup.select('div.hotcontent')
    for ps in hot_content:
        cat = [a.text for a in ps.select('div.keyword > ul > li > a')]
        cur_keyword = ps.select('h4 > a')[0].text
        if cur_keyword in keyword_set:
            continue
        keyword_set.add(cur_keyword)
        all_keywords.append({'title': cur_keyword,
                             'desc': ps.find('p').text,
                             'category': cat})

    # 逐页抓取
    a_next = soup.select('div > a.next')
    index = 1
    while len(a_next) != 0:
        params = {'limit': 30,
                  'index': index,
                  'offset': (index - 1) * 30}
        soup = crawl_html_doc('http://baike.baidu.com/fenlei/' + category, params=params)
        keywords = parse_sub_keywords(soup)
        all_keywords.extend(keywords)

        index += 1
        a_next = soup.select('div > a.next')
    return all_keywords


def crawl_keyword_by_category_short(category):
    """抓取一个分类下显示的所有词条，仅保留词条"""
    keyword_set.clear()
    soup = crawl_html_doc('http://baike.baidu.com/fenlei/' + category)
    all_keywords = []

    # 顶部轮播热点
    hot_content = soup.select('div.hotcontent')
    all_keywords.extend([ps.select('h4 > a')[0].text for ps in hot_content])

    # 逐页抓取
    a_next = soup.select('div > a.next')
    index = 1
    while len(a_next) != 0:
        params = {'limit': 30,
                  'index': index,
                  'offset': (index - 1) * 30}
        soup = crawl_html_doc('http://baike.baidu.com/fenlei/' + category, params=params)
        keywords = parse_sub_keywords_short(soup)
        all_keywords.extend(keywords)

        index += 1
        a_next = soup.select('div > a.next')
    return all_keywords


def crawl_keyword_by_category_list_short(category_list):
    """抓取一个分类列表显示的全部词条"""
    all_keywords = []
    for category in category_list:
        all_keywords.extend(crawl_keyword_by_category_short(category))
    return all_keywords


def crawl_all_keywords_short():
    """抓取全部词条"""
    keyword_set.clear()
    all_keywords = []
    # all_categories = json.loads(open('category_flat.json', 'r', encoding='utf-8').read())
    all_categories = [{'cat': '人物', 'sub_cat': ['政治人物', '历史人物', '文化人物']}]
    for big_category in all_categories:
        big_cat = big_category['cat']
        big_cat_keywords = crawl_keyword_by_category_list_short(big_category['sub_cat'])
        all_keywords.append({'cat': big_cat, 'keywords': big_cat_keywords})
    return all_keywords


if __name__ == '__main__':
    # all_keywords = crawl_keyword_by_category_short('政治人物')
    # print(len(all_keywords))
    # print(json.dumps(all_keywords, ensure_ascii=False, indent=4))
    all_keywords = crawl_all_keywords_short()
    print(len(all_keywords))
    print(json.dumps(all_keywords, ensure_ascii=False, indent=4))
    print(len(all_keywords[0]['keywords']))
