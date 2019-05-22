# -*- coding: utf-8 -*-
__author__ = 'olily'


import pymysql


# 打开数据库连接
db1 = pymysql.connect("localhost", "root", "123456", "jobsvs",)
# 使用 cursor() 方法创建一个游标对象 cursor
cursor1 = db1.cursor()

sql1 = 'select id,name from cities'
cursor1.execute('select id,name from cities')
cityandidDict = {}
cityandid = cursor1.fetchall()
for item in cityandid:
    cityandidDict[item[1]]=item[0]
print(cityandidDict)

sql2 = 'select id,name from industries'
cursor1.execute(sql2)

industryandidDict = {}
cityandid = cursor1.fetchall()
for item in cityandid:
    industryandidDict[item[1]]=item[0]
# print(industryandidDict)

sql3 = 'select id,name from companyquality'
cursor1.execute(sql3)

companyqualityDict = {}
cityandid = cursor1.fetchall()
for item in cityandid:
    companyqualityDict[item[1]]=item[0]
# print(companyqualityDict)

sql3 = 'select id,name from companysize'
cursor1.execute(sql3)

companysizeDict = {}
cityandid = cursor1.fetchall()
for item in cityandid:
    companysizeDict[item[1]]=item[0]
# print(companysizeDict)

sql3 = 'select id,name from education'
cursor1.execute(sql3)

educationDict = {}
cityandid = cursor1.fetchall()
for item in cityandid:
    educationDict[item[1]]=item[0]
# print(educationDict)

sql1 = 'select id,name from jobfunction'
cursor1.execute(sql1)

jonfuncationDict = {}
cityandid = cursor1.fetchall()
for item in cityandid:
    jonfuncationDict[item[1]]=item[0]
# print(jonfuncationDict)

sql1 = 'select id,name from education'
cursor1.execute(sql1)

educationDict = {}
cityandid = cursor1.fetchall()
for item in cityandid:
    educationDict[item[1]]=item[0]
# print(educationDict)

