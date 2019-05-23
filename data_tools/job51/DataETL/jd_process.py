# -*- coding: utf-8 -*-
__author__ = 'olily'

import pymysql
import datetime

# 打开数据库连接
db_jobsvs = pymysql.connect(
    "localhost",
    "root",
    "123456",
    "jobsvs",
    charset='utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor_jobsvs = db_jobsvs.cursor()

# 打开数据库连接
db_urllist = pymysql.connect("localhost", "root", "123456", "urllist",)
# 使用 cursor() 方法创建一个游标对象 cursor
cursor_urllist = db_urllist.cursor()

def get_jd():
    cursor_urllist.execute('truncate table fun_jd_copy1')
    cursor_urllist.execute('select * from fun_jd')
    for items in cursor_urllist.fetchall():
        item = items[1].split('要求')
        if len(item)<2:
            req=""
        else:
            req = item[1].replace('"',"").replace("\\","")
        res = item[0].replace('"','“”“').replace("\\","")
        sql = 'insert into fun_jd_copy1 values(%d,"%s","%s")'%(items[0],res,req)
        # print(sql)
        cursor_urllist.execute(sql)
    db_urllist.commit()



get_jd()
