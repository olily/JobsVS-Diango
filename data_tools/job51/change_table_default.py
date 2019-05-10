# -*- coding: utf-8 -*-
__author__ = 'olily'

import pymysql

# 打开数据库连接
db1 = pymysql.connect("localhost", "root", "123456", "jobsvs")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor1 = db1.cursor()

# 行业
i=1
sql = 'select name from industries where id=1'
cursor1.execute(sql)
name = cursor1.fetchone()
# sql1 = 'update industries set name = "无" where id = 1 and id = 2'
# cursor1.execute(sql1)
db1.commit()
i+=1
while name is not None:
    print(name)
    i += 1
    sql = 'select name from industries where id=%d'%(i)
    cursor1.execute(sql)
    next_name = cursor1.fetchone()
    sql1 = 'update industries set name = "%s" where id = %d'% (name,i)
    db1.commit()
    name = next_name


