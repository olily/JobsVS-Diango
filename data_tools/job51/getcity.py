# -*- coding: utf-8 -*-
__author__ = 'olily'
file = open("data/test.js", "r", encoding='UTF-8-sig')
count = 1
# print("insert into provinces(name) VALUES ('无');")
print("insert into cities (name,province_id) VALUES ('无',1);")
list = [2,3,5,6,7,34,35,36]
for line in file:
    lin = line.split(':')
    code_str = lin[0][1:-1]
    code = int(code_str)
    if code % 10000 == 0:
        # print("insert into provinces (name) VALUES ('%s');" % lin[1][1:-3])
        count += 1
        if count in list:
            print("insert into cities (name,province_id,city_zh) VALUES ('%s',%d,'%s');" % (lin[1][1:-3], count, str(code_str)))
    # 城市
    if code % 100 == 0 and code % 10000 != 0:
        print("insert into cities (name,province_id,city_zh) VALUES ('%s',%d,'%s');" % (lin[1][1:-3],count,str(code_str)))
        pass
file.close()
