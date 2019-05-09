# -*- coding: utf-8 -*-
__author__ = 'olily'


import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "jobsvs",)
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

sql1 = 'select id,name from cities'
cursor.execute(sql1)

# cityandidDict = {}
# cityandid = cursor.fetchall()
# for item in cityandid:
#     cityandidDict[item[1]]=item[0]
# print(cityandidDict)

sql2 = 'select id,name from industries'
cursor.execute(sql2)

industryandidDict = {}
cityandid = cursor.fetchall()
for item in cityandid:
    industryandidDict[item[1]]=item[0]
print(industryandidDict)

sql3 = 'select id,name from companyquality'
cursor.execute(sql3)

companyqualityDict = {}
cityandid = cursor.fetchall()
for item in cityandid:
    companyqualityDict[item[1]]=item[0]
print(companyqualityDict)

sql3 = 'select id,name from companysize'
cursor.execute(sql3)

companysizeDict = {}
cityandid = cursor.fetchall()
for item in cityandid:
    companysizeDict[item[1]]=item[0]
print(companysizeDict)

sql3 = 'select id,name from education'
cursor.execute(sql3)

educationDict = {}
cityandid = cursor.fetchall()
for item in cityandid:
    educationDict[item[1]]=item[0]
print(educationDict)

sql1 = 'select id,name from jobfunction'
cursor.execute(sql1)

jonfuncationDict = {}
cityandid = cursor.fetchall()
for item in cityandid:
    jonfuncationDict[item[1]]=item[0]
print(jonfuncationDict)

sql1 = 'select id,name from education'
cursor.execute(sql1)

educationDict = {}
cityandid = cursor.fetchall()
for item in cityandid:
    educationDict[item[1]]=item[0]
print(educationDict)

