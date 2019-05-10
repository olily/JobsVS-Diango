# -*- coding: utf-8 -*-
__author__ = 'olily'
file = open("data/test.js", "r", encoding='UTF-8-sig')
count = 1
# print("insert into provinces(name) VALUES ('无');")
print("insert into cities (name,province_id) VALUES ('无',1);")
for line in file:
    lin = line.split(':')
    code = int(lin[0][1:-1])
    if code % 10000 == 0:
        # print("insert into provinces (name) VALUES ('%s');" % lin[1][1:-3])
        count += 1
    # 城市
    if code % 100 == 0 and code % 10000 != 0:
        print("insert into cities (name,province_id) VALUES ('%s',%d);" % (lin[1][1:-3],count))
        pass
file.close()
