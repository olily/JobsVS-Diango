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
# sscursor_jobsvs = pymysql.cursors.SSCursor(db_jobsvs)
# sscursor_jobsvs.execute('SET NET_WRITE_TIMEOUT = 5000000')

# 打开数据库连接
db_urllist = pymysql.connect("localhost", "root", "123456", "urllist",)
# 使用 cursor() 方法创建一个游标对象 cursor
cursor_urllist = db_urllist.cursor()
# sscursor_urllist = pymysql.cursors.SSCursor(db_urllist)
# sscursor_urllist.execute('SET  session NET_WRITE_TIMEOUT = 5000000')
#

# 转换学历
def processEducation():
    cursor_jobsvs.execute('select id,name from education')
    for data in cursor_jobsvs.fetchall():
        sql = 'update jobs_get set education_id = %d where education = "%s"' % (
            data[0], data[1])
        # print(sql)
        cursor_urllist.execute(sql)
    db_urllist.commit()


#
def processCity():
    cursor_jobsvs.execute('select id,name from cities')
    for data in cursor_jobsvs.fetchall():
        sql = 'update jobs_get set city_id = %d where city = "%s"' % (
            data[0], data[1])
        # print(sql)
        cursor_urllist.execute(sql)
    db_urllist.commit()

# 转换企业
def processCompany():
    # sscursor_jobsvs.execute('select id,co_id from companies')
    cursor_jobsvs.execute('select id,co_id from companies where status_update = 0')
    datas = cursor_jobsvs.fetchall()
    # cursor_jobsvs.close()
    for data in datas:
        # print(data)
        sql = 'update jobs_get_copy9 set company_id = %d where company_code = "%s"' % (
            data[0], data[1])
        # print(sql)
        sql2 = ''
        cursor_urllist.execute(sql)
        db_urllist.commit()

        # print('update companies set status_update = 1 where id = %d' % (data[0]))
        cursor_jobsvs.execute('update companies set status_update = 1 where id = %d' % (data[0]))
        print(data[0])
        # print('update companies set status_update = 1 where id = %d' % (data[0]))
        db_jobsvs.commit()
    cursor_jobsvs.close()
    db_urllist.commit()

#  转换工资
def processSalary():
    cursor_urllist.execute(
        'select code,salary_low,salary_high,salary_type from jobs_get where status_update=1')
    list = cursor_urllist.fetchall()
    for data in list:
        if data is None:
            continue
        if data[3] == '0':
            salary_low = data[1] * 22
            salary_high = data[2] * 22
            sql = 'update jobs_get set salary_low=%d,salary_high=%d,status_update=0 where code = "%s"' % (
                salary_low, salary_high, data[0])
            cursor_urllist.execute(sql)
            # print(sql, ";")
            db_urllist.commit()
        elif data[3] == '2':
            salary_low = data[1] * 1000
            salary_high = data[2] * 1000
            sql = 'update jobs_get set salary_low=%d,salary_high=%d,status_update=0 where code = "%s"' % (
                salary_low, salary_high, data[0])
            cursor_urllist.execute(sql)
            # print(sql, ";")
            db_urllist.commit()
        elif data[3] == '3':
            salary_low = data[1] * 10000
            salary_high = data[2] * 10000
            sql = 'update jobs_get set salary_low=%d,salary_high=%d,status_update=0 where code = "%s"' % (
                salary_low, salary_high, data[0])
            cursor_urllist.execute(sql)
            # print(sql, ";")
            db_urllist.commit()
        elif data[3] == '4':
            salary_low = data[1] * 10000 / 12
            salary_high = data[2] * 10000 / 12
            sql = 'update jobs_get set salary_low=%d,salary_high=%d,status_update=0 where code = "%s"' % (
                salary_low, salary_high, data[0])
            cursor_urllist.execute(sql)
            # print(sql, ";")
            db_urllist.commit()
        else:
            sql = 'update jobs_get set salary_low=0,salary_high =0,status_update=0 where code = "%s"' % (
                data[0])
            cursor_urllist.execute(sql)
            # print(sql, ";")
            db_urllist.commit()

#  职能分解
def splitFunction():
    cursor_urllist.execute('truncate table jobs_jobfunction')
    cursor_urllist.execute('select id,job_fun from jobs_get')
    for items in cursor_urllist.fetchall():
        if items[1] !="" and items[1] is not None:
            item = items[1].split('_')
            for fun in item:
                sql = 'insert into jobs_jobfunction(jobs_id,jobsfunction_id,jobsfunction) values(%d,2,"%s")'%(items[0],fun)
                # print(sql)
                cursor_urllist.execute(sql)
            db_urllist.commit()

# 处理职能
def processJobfunction():
    cursor_jobsvs.execute('select id,name from jobfunction')
    for items in cursor_jobsvs.fetchall():
        sql = 'update jobs_jobfunction set jobsfunction_id = %d where jobsfunction = "%s"' % (items[0],items[1])
        # print(sql)
        cursor_urllist.execute(sql)
    db_urllist.commit()


#  职能分解
def splitFare():
    cursor_urllist.execute('truncate table jobs_fare')
    cursor_urllist.execute('select id,jobfare from jobs_get_copy9_copy2')
    for items in cursor_urllist.fetchall():
        if items[1] !="" and items[1] is not None:
            item = items[1].split('_')
            for fun in item:
                sql = 'insert into jobs_fare values(%d,"%s")'%(items[0],fun)
                # print(sql)
                cursor_urllist.execute(sql)
            db_urllist.commit()

# 转换sql
def construct():
    cursor_urllist.execute('select * from jobs_get')
    list = cursor_urllist.fetchall()
    for item in list:
        str = "2019-"+item[7]
        # print(str)
        put_time = datetime.datetime.strptime(str, "%Y-%m-%d").date()  # 字符串转化为date形式
        # print(put_time)
        sql = 'insert into jobs(id,name,job_id,company_id,salary_low,salary_high,city_id,put_time,url,work_year,jobfare,jobReqAndRes,education_id,isUndercarriage) values(%d,"%s","%s",%d,%d,%d,%d,"%s","%s","%s","%s","%s",%d,%d)' % (
            item[0],item[1],item[2],item[3],item[4],item[5],item[6],put_time,item[8],item[9],item[10],item[11],item[12],item[13])
        print(sql,";")


# 执行函数
# processEducation()
# processCity()
# processCompany()
# processSalary()
# construct()
# splitFunction()
# processJobfunction()
splitFare()
