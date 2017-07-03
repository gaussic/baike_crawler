#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from utils import crawl_html_doc

cat_set = set()


def crawl_root_categories():
    """百科首页分类列表"""
    soup = crawl_html_doc('http://baike.baidu.com')

    categories = []
    big_categories = soup.find(id='commonCategories').find_all('dl')
    for cat in big_categories:
        big_cat = cat.find('h2').text
        small_categories = cat.find('dd').find_all('a')
        small_cat = [sc.text for sc in small_categories]
        categories.append({big_cat: small_cat})
    return categories


def parse_sub_categories(soup):
    """解析当前分类的下级分类"""
    category_list = soup.select('div.category-title')
    if len(category_list) < 2:
        return []
    return [a.text for a in category_list[0].find_all('a')]


def crawl_sub_categories(category, depth):
    """递归抓取下级分类"""
    if depth == 0:
        return []
    soup = crawl_html_doc('http://baike.baidu.com/fenlei/' + category)
    sub_categories = parse_sub_categories(soup)
    subcat_list = []
    for sub_cat in sub_categories:
        if sub_cat in cat_set:  # 去重
            continue
        cat_set.add(sub_cat)
        sub_c = crawl_sub_categories(sub_cat, depth - 1)
        if len(sub_c) != 0:
            subcat_list.append({'cat': sub_cat, 'sub_cat': sub_c})
        else:
            subcat_list.append({'cat': sub_cat})
        print('Done: ' + sub_cat + ', depth=' + str(depth))
    return subcat_list


def crawl_categories_hierarchical(depth=6):
    sub_categories = crawl_sub_categories('政治人物', depth)
    with open('t.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(sub_categories, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    crawl_categories_hierarchical()
