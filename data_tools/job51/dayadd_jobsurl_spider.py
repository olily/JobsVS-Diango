# -*- coding: utf-8 -*-
__author__ = 'olily'

# 0507 每日新增岗位

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

    for i in range(1, 2001):
        data_row = []
        data_row.append("https://search.51job.com/list/000000,000000,0000,00,9,99,%2B,2,"+str(i)+".html?")
        data_row.append(user_agent_list[i % 12])
        Producer.producer(cities_queue, data_row)
    return cities_queue


# 翻页爬取每一页的所有岗位
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
    # co_main_div = html.find(attrs={'class': 'c2-main'})
    job_items = html.findAll(attrs={'class': 'el'})
    for item in job_items:
        job_id=job_name=job_url=put_time=salary=None

        job_url_div = item.find(attrs={'class':"t1 "})
        if job_url_div is not None:
            job_name = job_url_div.span.get('title')
            job_url = job_url_div.span.get('href')

            regx = re.compile('[0-9]+.html')
            co_id_str = regx.findall(job_url)
            job_id = str(co_id_str[0][:-5])

        co_div = item.find(attrs={'class': "t2"}).a
        if co_div is not None:
            co_url = co_div.get('href')

            regx = re.compile('co[0-9]+.html')
            co_id_str = regx.findall(co_url)
            co_id = str(co_id_str[0][:-5])

        salary_span = item.find(attrs={'class': "t4"})
        if salary_span is not None:
            salary = salary_span.text
            print(salary)
            exit()

        put_time_span = item.find(attrs={'class': "t5"})
        if put_time_span is not None:
            put_time = put_time_span.text

        job_row = [job_id,job_name, put_time,salary,job_url,]

        mylock.acquire()
        num += 1
        Producer.producer(courls_queue, job_row)
        mylock.release()

        if(num%10000)==0:
            print(num)



def insertDB(sql_value):
    global save_num
    db.ping(reconnect=True)
    # 提交到数据库执行,每1000条提交一次
    sql = 'insert into jobs(co_id,name,quality,size,note_city,note_industry,url) values("%s","%s", "%s","%s", "%s","%s", "%s")' % (str(sql_value[0]), str(sql_value[1]),str(sql_value[2]), str(sql_value[3]),str(sql_value[4]), str(sql_value[5]),str(sql_value[6]))
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
db = pymysql.connect("localhost", "root", "123456", "jobsvs", charset='utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 每次获取新数据前清空表
cursor.execute('SET foreign_key_checks = 0')
cursor.execute('truncate table jobs')
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