# -*- coding: utf-8 -*-
__author__ = 'olily'

# 0507 创建 爬取企业信息（简要）


from bs4 import BeautifulSoup as bs
import requests
import threading
from queue import Queue
import datetime
import re
import pymysql

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# 设置临界区（资源锁）
mylock = threading.RLock()
mylock2 = threading.RLock()

# 测试速度用
city_num = 0
num = 0
save_num = 0


# 解析网页
def html_paser(url, headers):
    try:
        response = requests.get(url)
    except :
        return 0
    else:
        response.encoding = 'gbk'
        html_text = response.text
        html = bs(html_text, 'html.parser')
        return html


class Producer(object):
    @staticmethod
    def producer(q, data):
        q.put(data)


# 建立线程函数
class MyThread(threading.Thread):
    def __init__(self, queue, func):
        threading.Thread.__init__(self)
        self.queue = queue
        self.func = func

    def run(self):
        while(True):
            try:
                task = self.queue.get(block=True, timeout=300)
                self.func(task)
                self.queue.task_done()
            except :
                break


# 建立线程池
class MyThreadPool():
    def __init__(self):
        self.pool = []

    def addthread(self, queue, size, func):
        self.queue = queue
        for i in range(size):
            self.pool.append(MyThread(queue, func))

    def startAll(self):
        for thd in self.pool:
            thd.start()

    def joinAll(self):
        for thd in self.pool:
            if thd.isAlive():
                thd.join()

# 构造生产者
def product_data(user_agent_list):
    cities_queue = Queue()

    for i in range(1, 3027):
        data_row = []
        data_row.append("https://company.51job.com/p"+str(i)+"/")
        data_row.append(user_agent_list[i % 12])
        Producer.producer(cities_queue, data_row)
    return cities_queue


# 翻页爬取每一页的所有企业
def spider_page(submission):
    url = submission[0]
    browser = submission[1]
    header = {
        'User-Agent': browser,
        'verify': False
    }
    global num

    # 遍历一页所有岗位
    html = html_paser(url, header)
    co_main_div = html.find(attrs={'class': 'c2-main'})
    co_items = co_main_div.findAll(attrs={'class': 'c2-t'})
    for item in co_items:
        # co_id=co_name=co_quality=co_size=city=industry=co_url=None
        co_id = co_name = co_quality_src = co_size_src = city_src = industry = co_url = None
        co_name_url = item.find(attrs={'class': 's1'})
        if co_name_url is not None:
            co_url = co_name_url.a.get('href')

            regx = re.compile('co[0-9]+.html')
            co_id_str = regx.findall(co_url)
            co_id = str(co_id_str[0][:-5])

            co_name = co_name_url.a.get("title")


        co_quality_span = item.find(attrs={'class': 's2'})
        if co_quality_span is not None:
            co_quality_src = co_quality_span.text
            # co_quality = companyqualityDict[co_quality_src]


        co_size_span = item.find(attrs={'class': 's3'})
        if co_size_span is not None:
            co_size_src = co_size_span.text
            # co_size = companysizeDict[co_size_src]

        city_span = item.find(attrs={'class': 's4'})
        if city_span is not None:
            city_src = city_span.text
            # city = cityandidDict[city_src]

        industry_span = item.find(attrs={'class': 's5'})
        if industry_span is not None:
            industry = industry_span.text

        co_row = [co_id,co_name,co_quality_src,co_size_src,city_src,co_url]

        mylock.acquire()
        num += 1
        Producer.producer(courls_queue, co_row)
        mylock.release()

        if(num%10000)==0:
            print(num)



def insertDB(sql_value):
    global save_num
    db.ping(reconnect=True)
    # 提交到数据库执行,每1000条提交一次
    sql = 'insert into companies(co_id,name,quality,size,city,url) values("%s","%s","%s","%s","%s","%s")' % (str(sql_value[0]), str(sql_value[1]),str(sql_value[2]), str(sql_value[3]),str(sql_value[4]), str(sql_value[5]))
    # SQL 插入语句
    try:
        mylock2.acquire()
        save_num += 1
        print(save_num)
        # print(sql)
        cursor.execute(sql)
        # print(sql)
        if save_num % 1000 == 0:
            db.commit()
            if save_num % 10000==0:
                print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),save_num)
        mylock2.release()
    except :
        mylock2.release()
        fp.write(sql + ';\n')
        fp.flush()
        # 如果发生错误则先提交后回滚
        # print(sql)
        db.commit()
        db.rollback()


# 浏览器代理池
user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"
]

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "jobs51", charset='utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

#
# sql1 = 'select id,name from cities'
# cursor.execute(sql1)
#
# cityandidDict = {}
# cityandid = cursor.fetchall()
# for item in cityandid:
#     cityandidDict[item[1]]=item[0]
# print(cityandidDict)
#
# sql2 = 'select id,name from industries'
# cursor.execute(sql2)
#
# industryandidDict = {}
# cityandid = cursor.fetchall()
# for item in cityandid:
#     industryandidDict[item[1]]=item[0]
# print(industryandidDict)
#
# sql3 = 'select id,name from companyquality'
# cursor.execute(sql3)
#
# companyqualityDict = {}
# cityandid = cursor.fetchall()
# for item in cityandid:
#     companyqualityDict[item[1]]=item[0]
# print(companyqualityDict)
#
# sql3 = 'select id,name from companysize'
# cursor.execute(sql3)
#
# companysizeDict = {}
# cityandid = cursor.fetchall()
# for item in cityandid:
#     companysizeDict[item[1]]=item[0]
# print(companysizeDict)
#
# sql3 = 'select id,name from education'
# cursor.execute(sql3)
#
# educationDict = {}
# cityandid = cursor.fetchall()
# for item in cityandid:
#     educationDict[item[1]]=item[0]
# print(educationDict)
#
# sql1 = 'select id,name from jobfunction'
# cursor.execute(sql1)
#
# jonfuncationDict = {}
# cityandid = cursor.fetchall()
# for item in cityandid:
#     jonfuncationDict[item[1]]=item[0]
# print(jonfuncationDict)
#
# sql1 = 'select id,name from education'
# cursor.execute(sql1)
#
# educationDict = {}
# cityandid = cursor.fetchall()
# for item in cityandid:
#     educationDict[item[1]]=item[0]
# print(educationDict)

# 每次获取新数据前清空表
cursor.execute('SET foreign_key_checks = 0')
cursor.execute('truncate table companies')
cursor.execute('SET foreign_key_checks = 1')

db.commit()

f = open("data/co_errsql.txt", "w+", encoding="utf-8")
f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
f.close()

fp = open("data/co_errsql.txt", "a+", encoding="utf-8")

maxsize = 18
q = product_data(user_agent_list)
courls_queue = Queue()

pool = MyThreadPool()
pool.addthread(queue=q, size=maxsize, func=spider_page)
pool.addthread(queue=courls_queue, size=5, func=insertDB)
pool.startAll()
pool.joinAll()

db.commit()
db.close()
fp.close()

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),save_num, "结束")
