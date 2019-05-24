# -*- coding: utf-8 -*-
__author__ = 'olily'


import pymysql
import jieba


def construct_dict():
    for i in range(68, 1020):
        res[str(i)] = {}
        req[str(i)] = {}


def process_data(fun_id, text_res, text_req):
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
        '，',
        '要求',
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
        '学历',
        '使用',
        '负责',
        '精通',
        '自由',
        '能够',
        '一定',
        '可能',r'\r\n','常用','根据','以及','一种','岗位职责','毕业','其他','部门'}
    # jieba.add_word('大数据')
    words_res = list(jieba.cut(text_res))
    words_req = list(jieba.cut(text_req))
    resDict = {}
    reqDict = {}
    resSet = set(words_res) - dele
    reqSet = set(words_req) - dele
    for w in resSet:
        if len(w) > 2:
            resDict[w] = words_res.count(w)
    for w in reqSet:
        if len(w) > 1:
            reqDict[w] = words_req.count(w)

    reslist = sorted(resDict.items(), key=lambda x: x[1], reverse=True)
    reqlist = sorted(reqDict.items(), key=lambda x: x[1], reverse=True)

    for i in reslist:
        res[str(fun_id)][i[0]]=i[1]

    for i in reqlist:
        req[str(fun_id)][i[0]] = i[1]


def get_data():
    for i in range(68, 1020):
        sql = 'select req,res from fun_jd_copy1 where jobsfunction_id=%d' % (i)
        cursor_urllist.execute(sql)
        reqstr = ""
        resstr = ""
        for items in cursor_urllist.fetchall():
            reqstr += items[0]
            resstr += items[1]
        process_data(i, resstr, reqstr)

def insertDB():
    for i in range(68,1020):
        for item in res[str(i)]:
            sql1 = 'insert into responsecloud values (%d,"%s",%d)'%(i,res[str(i)][item[0]],res[str(i)][item[1]])
            cursor_urllist.execute(sql1)
        db_urllist.commit()
        for item in req[str(i)]:
            sql2 = 'insert into requestcloud values (%d,"%s",%d)' % (i, req[str(i)][item[0]], req[str(i)][item[1]])
            cursor_urllist.execute(sql2)
        db_urllist.commit()


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
insertDB()

