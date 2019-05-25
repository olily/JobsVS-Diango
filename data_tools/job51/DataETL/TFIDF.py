# -*- coding: utf-8 -*-
__author__ = 'olily'


import pymysql
import jieba

start = 198


def construct_dict():
    for i in range(start, 1020):
        res[str(i)] = {}
        req[str(i)] = {}


def process_data(fun_id, text_res, text_req):
    print(fun_id)
    # article = open('test.txt', 'r').read()
    dele = {
        '。',
        '！',
        '？',
        '的',
        '“',
        '”',
        '（',
        '）',
        ' ',
        '》',
        '《',
        '，','of','条件','参与','in','the','能力','to','com','专业','完成',
        '要求','or','and'
        '岗位',
        '应该',
        '职责',
        '工作',
        '描述',
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '相关',
        '以上',
        '优先',
        '具有',
        '经验',
        '学历','以上学历'
        '使用','独立'
        '负责',
        '精通',
        '自由',
        '能够',
        '一定',
        '可能',r'\r\n','常用','根据','2.1','以及','一种','岗位职责','毕业','其他','部门','以上学历','be','00','  '}
    # jieba.add_word('大数据')
    words_res = list(jieba.cut(text_res))
    words_req = list(jieba.cut(text_req))
    resDict = {}
    reqDict = {}
    dele_req = {'30','51','10','大学本科'}
    dele_res = {'责任心','毕业生','5000','7.5','1.3','for','组织协调','985','211','重点本科'}
    resSet = set(words_res) - dele - dele_res
    reqSet = set(words_req) - dele - dele_req
    for w in resSet:
        if len(w) > 2:
            resDict[w] = words_res.count(w)
    for w in reqSet:
        if len(w) > 2:
            reqDict[w] = words_req.count(w)

    reslist = sorted(resDict.items(), key=lambda x: x[1], reverse=True)
    reqlist = sorted(reqDict.items(), key=lambda x: x[1], reverse=True)

    for i in reslist:
        if i[1]<6:
            continue
        sql1 = 'insert into responsecloud(jobfunction_id,response,count) values (%d,"%s",%d)' % (
            fun_id, i[0], i[1])
        # print(sql1)
        cursor_jobsvs.execute(sql1)
    db_jobsvs.commit()
        # res[str(fun_id)][i[0]]=i[1]
    for i in reqlist:
        if i[1]<6:
            continue
        sql2 = 'insert into requestcloud(jobfunction_id,request,count) values (%d,"%s",%d)' % (
            fun_id, i[0], i[1])
        cursor_jobsvs.execute(sql2)
    db_jobsvs.commit()

def get_data():
    for i in range(start, 1020):
        sql = 'select req,res from fun_jd_copy1 where jobsfunction_id=%d' % (i)
        cursor_urllist.execute(sql)
        reqstr = ""
        resstr = ""
        for items in cursor_urllist.fetchall():
            reqstr += items[0]
            resstr += items[1]
        process_data(i, resstr, reqstr)


def insertDB():
    for i in range(start,1020):
        for item in res[str(i)]:
            sql1 = 'insert into responsecloud(jobfunction_id,response,count) values (%d,"%s",%d)'%(i,res[str(i)][item[0]],res[str(i)][item[1]])
            # print(sql1)
            cursor_jobsvs.execute(sql1)
        db_jobsvs.commit()
        for item in req[str(i)]:
            sql2 = 'insert into requestcloud(jobfunction_id,request,count) values (%d,"%s",%d)' % (i, req[str(i)][item[0]], req[str(i)][item[1]])
            # print(sql2)
            cursor_jobsvs.execute(sql2)
        db_jobsvs.commit()


# 打开数据库连接
db_jobsvs = pymysql.connect(
    "localhost",
    "root",
    "123456",
    "jobsvs",
    charset='utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor_jobsvs = db_jobsvs.cursor()

# 打开数据库连接
db_urllist = pymysql.connect(
    "localhost",
    "root",
    "123456",
    "urllist",
    charset='utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor_urllist = db_urllist.cursor()

res = {}
req = {}

construct_dict()
get_data()
# insertDB()

