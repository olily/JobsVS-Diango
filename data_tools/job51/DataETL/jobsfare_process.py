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


#  职能分解
def splitFare():
    funfareDict = {}
    for i in range(68, 1020):
        funfareDict[str(i)] = {}

    # print(funfareDict)

    cursor_urllist.execute('truncate table jobs_fare')
    cursor_urllist.execute('select * from jobfun_fare')

    for items in cursor_urllist.fetchall():
        if items[1] !="" or items[1] is not None:
            item = items[1].split('_')
            # print(item)
            for fun in item:
                if fun in list(funfareDict[str(items[0])].keys()):
                    funfareDict[str(items[0])][fun]+=1
                else:
                    funfareDict[str(items[0])][fun] =1
    for items in funfareDict:
        for item in funfareDict[items]:
            sql = 'insert into jobs_fare values(%d,"%s",%d)'%(int(items),item,funfareDict[items][item])
            # print(sql)
            # exit()
            cursor_urllist.execute(sql)
        db_urllist.commit()

splitFare()