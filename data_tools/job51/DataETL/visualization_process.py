# -*- coding: utf-8 -*-
__author__ = 'olily'

import pymysql
import datetime
import pickle
import random
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
def insert_Map():
    sql = 'insert into map_process select jobsfunction_id,city_id,count(*),avg(salary_low) as s1,avg(salary_high) as s2 from jobs_get_copy9 as t1,jobs_jobfunction as t2 where t1.id = t2.jobs_id GROUP BY jobsfunction_id,city_id;'
    cursor_urllist.execute(sql)
    db_urllist.commit()

# Point
def insert_Point():
    sql = 'insert into point_process select education_id,work_year,avg(salary_low),avg(salary_high) from jobs_get_copy9 GROUP BY education_id,work_year;'
    cursor_urllist.execute(sql)
    db_urllist.commit()

def process_point():
    sql = 'select id,work_year from point_process'
    cursor_urllist.execute(sql)
    for item in cursor_jobsvs.fetchall():
        process_point(item)
        work_year = item[1]
        if work_year ==0:
            work_year = random.uniform(0,1)
        elif work_year  >0 and work_year <3:
            work_year = random.uniform(1,3)
        elif work_year  >=3 and work_year <5:
            work_year = random.uniform(3,5)
        elif work_year>=5 and work_year<8:
            work_year = random.uniform(5,8)
        elif work_year >=8 and work_year<10:
            work_year = random.uniform(8, 10)
        else:
            work_year = random.uniform(10, 13)
        sql2 = 'update point_prosss set work_year = %.3f where id=%d'%(item[0],work_year)
        cursor_urllist.execute(sql2)
    db_urllist.commit()

# 转换sql
def constructMap():
    cursor_urllist.execute('select * from map_process')
    list = cursor_urllist.fetchall()
    for item in list:
        sql = 'insert into jobsmap(jobfunction_id,city_id,job_count,job_salary_low,job_salary_high) values(%d,%d,%d,%d,%d)' % (
            item[0],item[1],item[2],item[3],item[4])
        # print(sql,";")
        fp.write(sql + ';\n')
        fp.flush()

def constructPoint():
    cursor_urllist.execute('select * from point_process')
    list = cursor_urllist.fetchall()
    for item in list:
        sql = 'insert into pointprocess(jobfunction_id,education_id,work_year,job_count,job_salary_low,job_salary_high) values(%d,%d,%d,%d,%d,%d)' % (
            item[0],item[1],item[2],item[3],item[4],item[5])
        # print(sql,";")
        fp2.write(sql + ';\n')
        fp2.flush()


# fp = open("../data/insertjobpoint.sql","w+")
fp2 = open("../data/insertjobpoint.sql","w+")
constructPoint()
fp2.close()

# process_point()

