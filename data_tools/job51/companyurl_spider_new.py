# -*- coding: utf-8 -*-
__author__ = 'olily'

# 0510 数据处理

import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "jobs51", charset='utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 打开数据库连接
db1 = pymysql.connect("localhost", "root", "123456", "jobsvs",)
# 使用 cursor() 方法创建一个游标对象 cursor
cursor1 = db1.cursor()

sql1 = 'select id,name from cities'
cursor1.execute(sql1)

cityandidDict = {}
cityandid = cursor1.fetchall()
for item in cityandid:
    cityandidDict[item[1]]=item[0]
# print(cityandidDict)

# sql2 = 'select id,name from industries'
# cursor1.execute(sql2)
#
# industryandidDict = {}
# cityandid = cursor1.fetchall()
# for item in cityandid:
#     industryandidDict[item[1]]=item[0]
# # print(industryandidDict)
#
# sql3 = 'select id,name from companyquality'
# cursor1.execute(sql3)
#
# companyqualityDict = {}
# cityandid = cursor1.fetchall()
# for item in cityandid:
#     companyqualityDict[item[1]]=item[0]
# # print(companyqualityDict)
#
# sql3 = 'select id,name from companysize'
# cursor1.execute(sql3)
#
# companysizeDict = {}
# cityandid = cursor1.fetchall()
# for item in cityandid:
#     companysizeDict[item[1]]=item[0]
# # print(companysizeDict)
#
# sql3 = 'select id,name from education'
# cursor1.execute(sql3)
#
# educationDict = {}
# cityandid = cursor1.fetchall()
# for item in cityandid:
#     educationDict[item[1]]=item[0]
# # print(educationDict)
#
# sql1 = 'select id,name from jobfunction'
# cursor1.execute(sql1)
#
# jonfuncationDict = {}
# cityandid = cursor1.fetchall()
# for item in cityandid:
#     jonfuncationDict[item[1]]=item[0]
# # print(jonfuncationDict)
#
# sql1 = 'select id,name from education'
# cursor1.execute(sql1)
#
# educationDict = {}
# cityandid = cursor1.fetchall()
# for item in cityandid:
#     educationDict[item[1]]=item[0]
# # print(educationDict)

# sql = 'update companies_copy5 set quality_id = 1,size_id=1,city_id = 1'
# # print(sql)
# cursor.execute(sql)
# db.commit()

# for items in companyqualityDict:
#     # print(items)
#     sql = 'update companies_copy5 set quality_id = %d where quality = "%s"' %(int(companyqualityDict[items]),items)
#     # print(sql)
#     cursor.execute(sql)
#     db.commit()
#
# for items in companysizeDict:
#     # print(items)
#     sql = 'update companies_copy5 set size_id = %d where size = "%s"' %(int(companysizeDict[items]),items)
#     # print(sql)
#     cursor.execute(sql)
#     db.commit()
#

for items in cityandidDict:
    print(items,cityandidDict[items])
    sql = 'update companies_copy5 set city_id = %d where city = "%s"' %(int(cityandidDict[items]),items)
    # print(sql)
    cursor.execute(sql)
    db.commit()
#

#
# cursor.execute('SET foreign_key_checks = 0')
# cursor.execute('truncate table companyindustry')
# cursor.execute('SET foreign_key_checks = 1')
# sql = 'select id,industry from companies_copy5'
# cursor.execute(sql)
# co_indus_data = cursor.fetchall()
# i=0
# for items in co_indus_data:
#     co_id = items[0]
#     if items[1] is not None:
#         industries = items[1].split('_')
#         for industry in industries:
#             sql = 'insert into companyindustry(company_id,industry_name) values(%d,"%s")'% (co_id,industry)
#             # print(sql)
#             i+=1
#             cursor.execute(sql)
#             if i % 1000 == 0:
#                 print(i)
#     db.commit()

# for items in industryandidDict:
#     # print(items)
#     sql = 'update companyindustry set industry_id = %d where industry_name = "%s"' %(int(industryandidDict[items]),items)
#     # print(sql)
#     cursor.execute(sql)
#     db.commit()






