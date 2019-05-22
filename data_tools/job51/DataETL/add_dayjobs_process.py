# -*- coding: utf-8 -*-
__author__ = 'olily'

import pymysql


db_urllist = pymysql.connect("localhost", "root", "123456", "urllist", charset='utf8')
cursor_urllist = db_urllist.cursor()

def get_jobs():
    cursor_urllist.execute('select * from jobs_get_copy9_copy4')
    for items in cursor_urllist.fetchall():
        sql = 'insert jobs(name,job_id,put_timem,salary_low,salary_high,work_year,url,city_id,company_id,education_id) values("%s","%s","%s",%d,%d,"%s","%s",%d,%d,%d)'%(items[1],items[2],items[7],items[4],items[5],items[9],items[8],items[6],items[3],items[10])
        fp2.write(sql+';')
        fp2.flush()

fp2 = open("../data/insertjobs.sql","w+")
get_jobs()
fp2.close()