# -*- coding: utf-8 -*-
__author__ = 'olily'

# 0507 创建 更新企业信息
from bs4 import BeautifulSoup as bs
import requests
import threading
from queue import Queue
import datetime
import re
import pymysql


from bs4 import BeautifulSoup as bs
import requests
import threading
from queue import Queue
import datetime
import pymysql

# 设置临界区（资源锁）
mylock = threading.RLock()
mylock2 = threading.RLock()


# 测试速度用
num = 0


# 解析网页
def html_paser(url, headers):
    try:
        response = requests.get(url, headers)
    except BaseException:
        return 0
    else:
        response.encoding = 'gbk'
        html_text = response.text
        html = bs(html_text, 'html.parser')
        return html


# 生产者模型
class Producer(object):
    @staticmethod
    def producer(q, data):
        q.put(data)


# 建立线程函数
class MyThread(threading.Thread):
    def __init__(self, queue,func):
        threading.Thread.__init__(self)
        self.queue = queue
        self.func = func

    def run(self):
        while(True):
            try:
                task = self.queue.get(block=True,timeout=300)
                self.func(task)
                # print(self.func)
                self.queue.task_done()
            except BaseException:
                break


# 建立线程池
class MyThreadPool():
    def __init__(self):
        self.pool = []

    def addthread(self,queue,size,func):
        self.queue = queue
        for i in range(size):
            self.pool.append(MyThread(queue,func))

    def startAll(self):
        for thd in self.pool:
            thd.start()

    def joinAll(self):
        for thd in self.pool:
            if thd.isAlive():
                thd.join()


# 构造生产者
def cursor_query(user_agent_list):
    joburls_queue = Queue()
    query_num = 0
    # 首先查询全量数据
    sscursor = pymysql.cursors.SSCursor(db)
    sscursor.execute('select id,url from companies')
    while True:
        # 每次获取时会从上次游标的位置开始移动size个位置，返回size条数据
        data = sscursor.fetchone()
        # 数据为空的时候中断循环
        if not data:
            break
        data_row = []
        data_row.append(data[0])
        data_row.append(data[1])
        data_row.append(user_agent_list[query_num%12])
        # print(data_row)
        Producer.producer(joburls_queue, data_row)
        query_num += 1
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),query_num)
    sscursor.close()
    del sscursor
    return joburls_queue


# 翻页爬取每一个企业详细信息
def get_job_detail(items):
    job_url = items[1]
    browser = items[2]
    co_id = items[0]

    header = {
        'User-Agent': browser,
        'verify': False
    }

    job_html = html_paser(job_url,header)
    if job_html == 0:
        return 0

    # 企业图标
    img_div = job_html.find(attrs={'class':'cimg'})
    img_url = None
    if img_div is not None:
        img_url = img_div.get('src')
    # print(img_url)

    # 地址
    location_div = job_html.find(attrs={'class': 'fp'})
    location = None
    if location_div is not None:
        location = location_div.text
    # print(location)


    global num
    num += 1
    update_row = [
        img_url,location,co_id]
    mylock.acquire()
    Producer.producer(jobs_queue,update_row)
    mylock.release()

    if num % 1000 == 0:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"request",num)


def insertDB(sql_value):
    global save_num
    db.ping(reconnect=True)
    # 提交到数据库执行,每1000条提交一次
    sql = 'update companies set img_url="%s",location="%s" where id=%d'%(sql_value[0],sql_value[1],sql_value[2])
    # SQL 插入语句
    try:
        mylock2.acquire()
        save_num += 1
        cursor.execute(sql)
        print(save_num)
        # print(sql)
        if save_num % 100 == 0:
            db.commit()
            if save_num % 10000 == 0:
                print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"save",save_num)
        mylock2.release()
    except :
        mylock2.release()
        print("err")
        fp.write(sql + ';\n')
        fp.flush()
        # 如果发生错误则先提交再回滚
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

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "jobsvs", charset='utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# cursor.execute('truncate table job_info')
# db.commit()

f = open("data/co_update_errsql.txt", "w+", encoding="utf-8")
f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
f.close()

fp = open("data/co_update_errsql.txt", "a+", encoding="utf-8")


q = cursor_query(user_agent_list)

jobs_queue = Queue()
save_num = 0

pool = MyThreadPool()
pool.addthread(queue=q, size=18,func=get_job_detail)
pool.addthread(queue=jobs_queue, size=2,func=insertDB)
pool.startAll()
pool.joinAll()


db.close()

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "结束")
