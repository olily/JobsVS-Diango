# -*- coding: utf-8 -*-
__author__ = 'olily'

# 0330建立文件，爬取51job所有城市分类名称


from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd
import pymysql

# 保存城市名称，将拼音作为index，数据为：中文名，url,页数
columns = ['city_name_zh', 'city_url', 'page_num']
index = []
cityAndurl = pd.DataFrame(index=index, columns=columns)


def insertDB(table_name, index_id,sql_value):
    # db.ping(reconnect=True)
    # SQL 插入语句
    try:
        # 执行sql语句
        cursor.execute(
            'insert into city_info values( %d, "%s", "%s", "%s")' % (index_id,str(sql_value[0]),str(sql_value[1][0]),str(sql_value[1][1])))
        # 提交到数据库执行
        db.commit()
    except BaseException:
        # 如果发生错误则回滚
        db.rollback()


# 解析网页
def html_paser(url, headers):
    response = requests.get(url, headers)
    response.encoding = 'utf-8'
    html_text = response.text

    html = bs(html_text, 'html.parser')
    return html


# 得到城市名称，拼音、中文
def get_cityname(url, headers):
    html = html_paser(url, headers)
    cities = html.find_all(
        'a', attrs={
            'href': re.compile('www.51job.com/[a-z]+/$')})

    # i = 0
    # 保存到dataframe
    for h in cities:
        citi_url = h.get('href')
        city_name = citi_url[16:-1]
        index.append(city_name)
        cityAndurl.loc[city_name, 'city_name_zh'] = h.text


# 构造城市岗位列表的url
def construct_url(url_pre,table_name):
    # i=0
    for city in index:
        url = url_pre + city + '/'
        cityAndurl.loc[city, 'city_url'] = url
        # insertDB(table_name,i,city,cityAndurl.loc[city])

        # i+=1
        # print(i)


# 访问url,得到每一城市的页数,web端
def page_num(headers):
    for city in index:
        city_url = cityAndurl.loc[city, 'city_url']
        html = html_paser(city_url, headers)

        # web端
        page_num_str = html.find(attrs={'id':'hidTotalPage'})
        page_num = page_num_str.get('value')
        cityAndurl.loc[city, 'page_num'] = page_num
        print(city,page_num)
        break


# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "jobs51",)
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
}

# 首页
home = 'http://www.51job.com/'
# 城市url前缀
# url_pre = 'https://jobs.51job.com/'

# 移动端前缀
url_pre = 'https://m.51job.com/jobs/'

get_cityname(home, headers)
construct_url(url_pre,'city_info')

# page_num(headers)
i=1
for row in cityAndurl.iterrows():
    print(i,row[0], row[1][0], row[1][1])
    insertDB('city_info',i,row)
    i+=1
    print(i)
    # print(row[0],row[1][0],row[1][1])

db.close()

cityAndurl.to_csv('data/phone_city_url2.csv')
# ,encoding='gb2312'
