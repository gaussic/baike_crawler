import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import json


def insert_categories(category_list):
    """将分类插入Mongodb"""
    client = MongoClient('mongodb://121.42.182.174:27017')
    db = client.baike
    try:
        db.category.insert_many(category_list)
    except Exception as e:
        print(e)


def insert_keywords_one_category(keywords):
    client = MongoClient('mongodb://121.42.182.174:27017')
    db = client.baike
    try:
        db.keyword.insert_one(keywords)
    except Exception as e:
        print(e)


def insert_keywords_detail(keyword):
    client = MongoClient('mongodb://121.42.182.174:27017')
    db = client.baike
    try:
        db.keyword_detail.insert_one(keyword)
    except Exception as e:
        print(e)


def query_categories():
    client = MongoClient('mongodb://121.42.182.174:27017')
    db = client.baike
    result = db.category.find(projection={'_id': False})
    return list(result)


def query_one_category(category):
    client = MongoClient('mongodb://121.42.182.174:27017')
    db = client.baike
    result = db.category.find({'cat': category}, projection={'_id': False})
    return list(result)[0]


def query_keywords_one_category(category):
    client = MongoClient('mongodb://121.42.182.174:27017')
    db = client.baike
    result = db.keyword.find({'cat': category}, projection={'_id': False})
    return list(result)[0]



def crawl_html_doc(url, encoding='utf-8', params=None):
    """获取网页内容，转化为soup"""
    r = requests.get(url, params=params)
    print(r.url)
    soup = BeautifulSoup(str(r.content, encoding=encoding, errors='ignore'), 'html5lib')
    return soup




if __name__ == "__main__":
    # category_list = json.load(open('category_flat.json', 'r', encoding='utf-8'))
    # insert_categories(category_list)
    category = query_one_category('人物')
    print(category)
