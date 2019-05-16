# -*- coding: utf-8 -*-
__author__ = 'olily'

import pymysql

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
    sscursor_jobsvs.execute('select id,name from education')
    while True:
        db_urllist.ping(reconnect=True)
        data = sscursor_jobsvs.fetchone()
        if not data:
            break
        sql = 'update jobs_get_copy6 set education_id = %d where education = "%s"' % (
            data[0], data[1])
        # print(sql)
        cursor_urllist.execute(sql)
    db_urllist.commit()


# 转换职能
def processJobfunction():
    sscursor_jobsvs.execute('select id,name from jobfunction')
    while True:
        data = sscursor_jobsvs.fetchone()
        if not data:
            break
        sql = 'update jobs_get_copy6 set fun_id = %d where job_fun = "%s"' % (
            data[0], data[1])
        cursor_urllist.execute(sql)
    db_urllist.commit()

# 转换企业


def processCompany():
    # sscursor_jobsvs.execute('select id,co_id from companies')
    cursor_jobsvs.execute('select id,co_id from companies')
    datas = cursor_jobsvs.fetchall()
    cursor_jobsvs.close()
    for data in datas:
        sql = 'update jobs_get_copy6 set company_id = %d where company_code = "%s"' % (
            data[0], data[1])
        # print(sql)
        cursor_urllist.execute(sql)
        db_urllist.commit()
    # while True:
    #     db_urllist.ping(reconnect=True)
    #     data = sscursor_jobsvs.fetchone()
    #     if not data:
    #         break
    #     sql = 'update jobs_get_copy6 set company_id = %d where company_code = "%s"'%(data[0],data[1])
    #     # print(sql)
    #     cursor_urllist.execute(sql)
    #     db_urllist.commit()
    db_urllist.commit()

#  转换工资


def processSlary():
    cursor_urllist.execute(
        'select code,salary_low,salary_high,salary_type from jobs_get_copy6')
    list = cursor_urllist.fetchall()
    for data in list:
        if data is None:
            continue
        if data[3] == '0':
            salary_low = data[1] * 22
            salary_high = data[2] * 22
            sql = 'update jobs_get_copy6 set salary_low=%d,salary_high=%d where code = "%s"' % (
                salary_low, salary_high, data[0])
            cursor_urllist.execute(sql)
            # print(sql, ";")
            db_urllist.commit()
        elif data[3] == '2':
            salary_low = data[1] * 1000
            salary_high = data[2] * 1000
            sql = 'update jobs_get_copy6 set salary_low=%d,salary_high=%d where code = "%s"' % (
                salary_low, salary_high, data[0])
            cursor_urllist.execute(sql)
            # print(sql, ";")
            db_urllist.commit()
        elif data[3] == '3':
            salary_low = data[1] * 10000
            salary_high = data[2] * 10000
            sql = 'update jobs_get_copy6 set salary_low=%d,salary_high=%d where code = "%s"' % (
                salary_low, salary_high, data[0])
            cursor_urllist.execute(sql)
            # print(sql, ";")
            db_urllist.commit()
        elif data[3] == '4':
            salary_low = data[1] * 10000 / 12
            salary_high = data[2] * 10000 / 12
            sql = 'update jobs_get_copy6 set salary_low=%d,salary_high=%d where code = "%s"' % (
                salary_low, salary_high, data[0])
            cursor_urllist.execute(sql)
            # print(sql, ";")
            db_urllist.commit()
        else:
            sql = 'update jobs_get_copy6 set salary_low=0,salary_high =0 where code = "%s"' % (
                data[0])
            cursor_urllist.execute(sql)
            # print(sql, ";")
            db_urllist.commit()

#  职能分解
def splitFunction():
    cursor_urllist.execute('select id,jobfunction from jobs_get_copy7')

# 处理职能
def processFunction():
    cursor_jobsvs.execute('select id,name from jobfunction where category_id is not NULL')

    list = cursor_jobsvs.fetchall()
    for item in list:




# 构造jobs表
def construct():
    cursor_urllist.execute('select * from jobs_get_copy6_copy1')
    list = cursor_urllist.fetchall()
    for item in list:
        sql = 'insert into jobs(id,name,job_id,company_id,salary_low,salary_high,city_id,put_time,url,work_year,jobfare,jobReqAndRes,education_id,fun_id,isUndercarriage) values(%d,"%s","%s",%d,%d,%d,%d,"%s","%s","%s","%s","%s",%d,%d,%d)' % (
            item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[11],item[12],item[13],item[14])
        print(sql,";")



# processEducation()
# processJobfunction()
# processCompany()
# processSlary()
construct()
