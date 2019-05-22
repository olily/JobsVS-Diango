# -*- coding: utf-8 -*-
__author__ = 'olily'

#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time


import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "jobsvs", charset='utf8')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

time_start = time.time()

# 使用execute方法执行SQL语句
cursor.execute("SELECT id,co_id FROM companies")

# 使用 fetchone() 方法获取一条数据
data = cursor.fetchall()
companyDict = {}
for company in data:
    companyDict[company[1]] = company[0]
time_end = time.time()
print('totally cost', time_end - time_start)
cursor.close()
db.close()

db_urllist = pymysql.connect("localhost", "root", "123456", "urllist", charset='utf8')
cursor_urllist = db_urllist.cursor()

time_start = time.time()
time_end = time.time()
print('totally cost', time_end - time_start)

cursor_urllist.execute('truncate table jobs_get_copy9_copy4')

cursor_urllist.execute("SELECT * FROM jobs_get_copy9 ")
data = cursor_urllist.fetchall()
time_start = time.time()
for job in data:
    if job[3] not in companyDict.keys():
        continue
    co_id = companyDict[job[3]]
    sql = 'insert into jobs_get_copy9_copy4 values("%s","%s",%d,%d,%d,%d,"%s","%s","%s",%d)' %(job[1],job[2],co_id,job[5],job[6],job[7],job[8],job[9],job[10],job[11])
    # print(sql)
    # exit()
    cursor_urllist.execute(sql)
db_urllist.commit()
time_end = time.time()
print('totally cost', time_end - time_start)
