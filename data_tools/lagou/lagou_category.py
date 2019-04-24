# -*- coding: utf-8 -*-
__author__ = 'olily'


# 导入要用到的模块
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import re


# 反爬虫机制
header = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
}

url = "https://www.lagou.com/"

# 开始爬取
response = requests.get(url=url, headers=header)
response.encoding = 'utf-8'
html_text = response.text
# 解析
html = bs(html_text, 'html.parser')


# 新建dataframe并修改列名
columns = [
    'catg_no',
    'category2_no',
    'category1_name',
    'category2_name',
    'category3_no',
    'category3_name',
    'href']
category = pd.DataFrame(columns=columns)

# 3级目录,自顶向下爬取
index = 1
catg_no = 1
category1 = html.find_all(attrs={"class": "menu_box"})
for catg1 in category1:
    category1_name = catg1.find("h2").string
    category1_name = category1_name.replace(' ','').replace('\t','').replace('\r','').replace('\r\n','').replace('\n','')
    category2 = catg1.find_all('dl')
    for catg2 in category2:
        category2_name = catg2.find("span").text
        category3 = catg2.find_all('a')
        for catg3 in category3:
            category2_no = catg3.get('data-lg-tj-id')
            category3_no = catg3.get('data-lg-tj-no')
            category3_name = catg3.string
            href = catg3.get('href')
            category.loc[index] = [
                catg_no,
                category2_no,
                category1_name,
                category2_name,
                category3_no,
                category3_name,
                href]
            index+=1
    catg_no += 1

# indexs = pd.Series
indexs = category['catg_no'].map(str)+category['category3_no']
print(type(indexs))
category.index = indexs
# category.reindex()


category.to_csv('data/lagou_categorys.csv',encoding='utf-8')


