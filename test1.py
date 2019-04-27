# -*- coding: utf-8 -*-
__author__ = 'olily'

# 0401建立文件，爬取51job所有城市分类名称(移动端)
# 多线程处理优化：一条线程跑一个城市
# 0402 将数据写入数据库永久保存

from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import threading
from queue import Queue
import datetime
import re
import pymysql
# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "tee", charset='utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
sql = "insert into test VALUES(100)"
cursor.execute(sql)
sql = "insert into test1 VALUES(101)"
try:
    cursor.execute(sql)
except:
    print("gg")
    db.commit()

# cursor.fetchmany()
# db.rollback()
db.commit()
db.close()
'''

'''





