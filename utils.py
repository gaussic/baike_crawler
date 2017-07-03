import requests
from bs4 import BeautifulSoup


def crawl_html_doc(url, encoding='utf-8', params=None):
    """获取网页内容，转化为soup"""
    r = requests.get(url, params=params)
    soup = BeautifulSoup(str(r.content, encoding=encoding, errors='ignore'), 'html5lib')
    return soup
