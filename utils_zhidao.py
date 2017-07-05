#!/usr/bin/python
# -*- coding: utf-8 -*-

from pymongo import MongoClient


def connect():
    client = MongoClient('mongodb://121.42.182.174:27017')
    db = client.zhidao
    return db


def insert_question_url(q_u):
    db = connect()
    try:
        db.qa.insert_one(q_u)
    except Exception as e:
        print(e)
