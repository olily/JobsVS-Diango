# -*- coding: utf-8 -*-
__author__ = 'olily'


from bs4 import BeautifulSoup as bs
import requests
import datetime

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

#
# 解析网页
def html_paser(url):
    try:
        response = requests.get(url)
    except :
        return 0
    else:
        response.encoding = 'gbk'
        html_text = response.text
        html = bs(html_text, 'html.parser')
        return html

# 内容抽取
def getContent(html):
    list_table = html.find(attrs={'class':'pcon'})
    list = list_table.findAll('a')
    for item in list:
        city_name = item.text
        city_url = item.get('href')
        city_pinyin = city_url[16:-1]
        print(city_name,city_url,city_pinyin)


url = "https://www.51job.com/sitemap/area_Navigate.php"
html=html_paser(url)
getContent(html)
