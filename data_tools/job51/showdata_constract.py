# -*- coding: utf-8 -*-
__author__ = 'olily'

import pymysql

# 打开数据库连接
db1 = pymysql.connect("localhost", "root", "123456", "jobsvs")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor1 = db1.cursor()

# 城市
cities = []
sql = 'select id,name from provinces'
cursor1.execute(sql)
provinces_table = cursor1.fetchall()
for items in provinces_table:
    province_dict = {}
    province_dict['value'] = items[0]
    province_dict['label'] = items[1]
    province_list = []
    sql1 = 'select id,name from cities where province_id= %d' % (int(items[0]))
    cursor1.execute(sql1)
    city_list = cursor1.fetchall()
    for city in city_list:
        city_dict = {}
        city_dict['value'] = city[0]
        city_dict['label'] = city[1]
        province_list.append(city_dict)
    province_dict['children'] = province_list
    cities.append(province_dict)

cities.sort(key=lambda city: city['value'])

print(cities)

# 行业
sql  = 'select id,name from industries where category_id is Null'
cursor1.execute(sql)
industries = []
category_table = cursor1.fetchall()
for items in category_table:
    # print(items)
    category_dict = {}
    category_dict['value'] = items[0]
    category_dict['label'] = items[1]
    sql = 'select id,name from industries where category_id=%d'% (int(items[0]))
    cursor1.execute(sql)
    category_dict['children'] = []
    item_list = cursor1.fetchall()
    for item in item_list:
        row = {}
        row['value'] = item[0]
        row['label'] = item[1]
        category_dict['children'].append(row)
    industries.append(category_dict)
print(industries)



# 职能
sql  = 'select id,name from jobfunction where category_id is Null'
cursor1.execute(sql)
jobfunction = []
category_table = cursor1.fetchall()
for items in category_table:
    # print(items)
    category_dict = {}
    category_dict['value'] = items[0]
    category_dict['label'] = items[1]
    sql = 'select id,name from jobfunction where category_id=%d'% (int(items[0]))
    cursor1.execute(sql)
    category_dict['children'] = []
    item_list = cursor1.fetchall()
    for item in item_list:
        row = {}
        row['value'] = item[0]
        row['label'] = item[1]
        category_dict['children'].append(row)
    jobfunction.append(category_dict)
print(jobfunction)
