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



# Map
def process_Map():
    sql = 'insert into map_process select jobsfunction_id,city_id,count(*),avg(salary_low) as s1,avg(salary_high) as s2 from jobs_get_copy9 as t1,jobs_jobfunction as t2 where t1.id = t2.jobs_id GROUP BY jobsfunction_id,city_id;'
    cursor_urllist.execute(sql)
    db_urllist.commit()
