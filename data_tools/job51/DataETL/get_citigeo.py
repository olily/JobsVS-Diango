# -*- coding: utf-8 -*-
__author__ = 'olily'

import requests
import json
import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "jobsvs", charset='utf8' )
# 使用cursor()方法获取操作游标
cursor = db.cursor()
# 使用execute方法执行SQL语句
cursor.execute("SELECT name FROM cities WHERE name!='无'")
data = cursor.fetchall()
print(data)
jsStr = '{'
for city in data:
    req = requests.get("http://api.map.baidu.com/geocoder/v2/?address="+city[0]+"&output=json&ak=NmMSjG5Zar0nfp5TGG9DCTSOLQ0ATmSH")
    jsonStr = json.loads(req.text)
    if jsonStr['status'] == 0:
        jsStr += "\"" + city[0] + "\": " + "[" + str(jsonStr['result']['location']['lng']) + "," + str(jsonStr['result']['location']['lat']) + "],"
    else:
        print(city[0])
jsStr += "}"
print(jsStr)
# 关闭数据库连接
db.close()