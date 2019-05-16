# -*- coding: utf-8 -*-
__author__ = 'olily'

# 0401创建，开始编写爬取具体岗位信息
# 采用生产者-消费者模型：producter customer


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
def html_paser(url):
    try:
        response = requests.get(url)
    except BaseException:
        return 0
    else:
        response.encoding = 'utf-8'
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
def cursor_query():
    joburls_queue = Queue()
    query_num = 0
    # 首先查询全量数据
    sscursor = pymysql.cursors.SSCursor(db)
    sscursor.execute('select code,url from jobs_get where status_jd=0')
    while True:
        # 每次获取时会从上次游标的位置开始移动size个位置，返回size条数据
        data = sscursor.fetchone()
        # 数据为空的时候中断循环
        if not data:
            break
        data_row = []
        data_row.append(data[0])
        data_row.append(data[1])
        # data_row.append(user_agent_list[query_num%12])
        # print(data_row)
        Producer.producer(joburls_queue, data_row)
        query_num += 1
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),query_num)
    sscursor.close()
    del sscursor
    return joburls_queue


# 翻页爬取每一个岗位的所有信息
def get_job_detail(items):
    global num
    url = items[1]
    code = items[0]

    job_url = "https://m.51job.com/jobs/"+url[23:]
    # print(job_url)

    job_html = html_paser(job_url)
    if job_html == 0:
        return 0

    # 岗位描述
    jd = None
    jd_tag = job_html.find(attrs={'class': 'ain'})
    if jd_tag is not None:
        if jd_tag.article is not None:
            jd = jd_tag.article.text

    job_info = [jd,code]
    # print(job_info)

    mylock.acquire()
    num+=1
    Producer.producer(jobs_queue,job_info)
    mylock.release()

    if num % 10000 == 0:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"request",num)


def insertDB(sql_value):
    # print(11111111111111111111)
    global save_num
    db.ping(reconnect=True)
    # 提交到数据库执行,每1000条提交一次
    sql = 'update jobs_get set status_jd=1,jd="%s" where code="%s"' % (str(sql_value[0]),str(sql_value[1]))
    # print(sql)
    # SQL 插入语句
    try:
        mylock2.acquire()
        save_num += 1
        cursor.execute(sql)
        # print(save_num)
        if save_num % 1000 == 0:
            db.commit()
            if save_num % 10000 == 0:
                print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"save",save_num)
        mylock2.release()
    except :
        mylock2.release()
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
db = pymysql.connect("localhost", "root", "123456", "urllist", charset='utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

db.commit()

f = open("data/jobid_errsql.txt", "w+", encoding="utf-8")
f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
f.close()

fp = open("data/jobid_errsql.txt", "a+", encoding="utf-8")


q = cursor_query()

jobs_queue = Queue()
save_num = 0

pool = MyThreadPool()
pool.addthread(queue=q, size=18,func=get_job_detail)
pool.addthread(queue=jobs_queue, size=1,func=insertDB)
pool.startAll()
pool.joinAll()


db.close()

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "结束")
