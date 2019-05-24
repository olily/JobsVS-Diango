from django.test import TestCase

# Create your tests here.


import random
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

random_data=random.sample(range(1,300000),10000)
for i in random_data:
    sql = 'select * from companysparallel_com where id= %d'%(i)
    cursor_jobsvs.execute(sql)
    data = cursor_jobsvs.fetchone()
    sql2 = 'insert into companysparallel values(%d,%d,%d,%d,%d,%d)' %(data[0],data[1],data[2],data[3],data[4],data[5])
    cursor_jobsvs.execute(sql2)
db_jobsvs.commit()

