# -*- coding: utf-8 -*-
__author__ = 'olily'
import pymysql


db1 = pymysql.connect("localhost", "root", "123456", "jobsvs",)
cursor1 = db1.cursor()
for line in open("data/yesterday.txt"):
    data = line.split('\t')
    company_id = int(data[0])
    count = int(data[1][:-1])
    # print('UPDATE companies SET yesterday_count=%d WHERE id=%d' % (count,company_id))
    cursor1.execute('UPDATE companies SET yesterday_count=%d WHERE id=%d' % (count,company_id))
    db1.commit()
exit()
# 打开数据库连接

# 使用 cursor() 方法创建一个游标对象 cursor
cursor1 = db1.cursor()

# sql1 = 'select id,name from cities'
cursor1.execute('select id,name from cities')
