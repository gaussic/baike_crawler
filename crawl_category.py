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
        categories.append({"cat": big_cat, "sub_cat": small_cat})
    return categories


def parse_sub_categories(soup):
    """解析当前分类的下级分类"""
    category_list = soup.select('div.category-title')
    if len(category_list) < 2:
        return []
    return [a.text for a in category_list[0].find_all('a')]


def crawl_sub_categories_hierarchical(category, depth):
    """递归抓取下级分类，生成层级分类"""
    if depth == 0:
        return []
    soup = crawl_html_doc('http://baike.baidu.com/fenlei/' + category)
    sub_categories = parse_sub_categories(soup)
    subcat_list = []
    for sub_cat in sub_categories:
        if sub_cat in cat_set:  # 去重
            continue
        cat_set.add(sub_cat)
        sub_c = crawl_sub_categories_hierarchical(sub_cat, depth - 1)
        if len(sub_c) != 0:
            subcat_list.append({'cat': sub_cat, 'sub_cat': sub_c})
        else:
            subcat_list.append({'cat': sub_cat})
        print('Done: ' + sub_cat + ', depth=' + str(depth))
    return subcat_list


def crawl_categories_hierarchical(depth=10):
    """生成层级分类列表"""
    cat_set.clear()
    root_categories = crawl_root_categories()
    root_categories = [{'cat': '人物', 'sub_cat': ['政治人物', '历史人物']}]
    categories = []
    for rc in root_categories:
        print('-------' + rc['cat'] + '----------')

        sub_cat = []
        for rc_sub in rc['sub_cat']:
            if rc_sub in cat_set:
                continue
            cat_set.add(rc_sub)
            sub_categories = crawl_sub_categories_hierarchical(rc_sub, depth)
            sub_cat.append({'cat': rc_sub, 'sub_cat': sub_categories})
        if len(sub_cat) != 0:
            categories.append({'cat': rc['cat'], 'sub_cat': sub_cat})
        else:
            categories.append({'cat': rc['cat']})

    with open('category_hierarchical.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(categories, ensure_ascii=False, indent=4))

    cat_set.clear()


def crawl_sub_categories_flat(category, depth):
    """递归抓取下级分类，生成平级分类"""
    if depth == 0:
        return []
    soup = crawl_html_doc('http://baike.baidu.com/fenlei/' + category)
    sub_categories = parse_sub_categories(soup)
    subcat_list = []
    for sub_cat in sub_categories:
        if sub_cat in cat_set:  # 去重
            continue
        cat_set.add(sub_cat)
        sub_c = crawl_sub_categories_flat(sub_cat, depth - 1)
        subcat_list.append(sub_cat)
        if len(sub_c) != 0:
            subcat_list.extend(sub_c)
        print('Done: ' + sub_cat + ', depth=' + str(depth))
    return subcat_list


def crawl_categories_flat(depth=10):
    """生层平级分类列表"""
    cat_set.clear()
    root_categories = crawl_root_categories()
    categories = []
    print(root_categories)
    for rc in root_categories:
        print('-------' + rc['cat'] + '----------')
        sub_cat = []
        for rc_sub in rc['sub_cat']:
            if rc_sub in cat_set:  # 去重
                continue
            cat_set.add(rc_sub)
            sub_categories = crawl_sub_categories_flat(rc_sub, depth)
            sub_cat.append(rc_sub)
            sub_cat.extend(sub_categories)
        if len(sub_cat) != 0:
            categories.append({'cat': rc['cat'], 'sub_cat': sub_cat})
        else:
            categories.append({'cat': rc['cat']})

    with open('category_flat.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(categories, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    # crawl_categories_hierarchical()
    crawl_categories_flat()
