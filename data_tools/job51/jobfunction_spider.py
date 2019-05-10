# -*- coding: utf-8 -*-
__author__ = 'olily'

# 0507创建  爬取职能


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

    for i in range(1, 3018):
        data_row = []
        data_row.append("https://company.51job.com/p"+str(i)+"/")
        data_row.append(user_agent_list[i % 12])
        Producer.producer(cities_queue, data_row)
    return cities_queue


# 翻页爬取每一页的所有行业
def spider_page(submission):
    url = submission[0]
    browser = submission[1]
    header = {
        'User-Agent': browser,
        'verify': False
    }

    # 遍历一页所有岗位
    html = html_paser(url, header)
    industry_list_div = html.find(attrs={'class': 'dw_list dw_site'})
    industry_items = industry_list_div.findAll('li')
    # print(industry_items)

    j= 1
    for item in industry_items:
        if item==None or item.a==None:
            continue

        # 保存行业分类
        category_name = item.a.text
        sql = 'insert into jobfunction(name,fun_id,url) values("%s","%s", "%s")' % (category_name, j,None)
        cursor.execute(sql)
        j+=1
    db.commit()

    i=2
    for item in industry_items:
        if item==None or item.a==None:
            continue
        i += 1
        # 遍历保存行业
        industry_li = item.div.findAll('a')
        for industry in industry_li:
            # industry_url=industry_id=industry_name=None
            industry_name = industry.text
            industry_url = industry.get('href')

            regx = re.compile('com/.*')
            industry_url_str = regx.findall(industry_url)
            industry_id = str(industry_url_str[0][4:])

            category_id = i

            row = [industry_name,industry_id,industry_url,category_id]
            mylock.acquire()
            Producer.producer(courls_queue, row)
            mylock.release()


def insertDB(sql_value):
    global save_num
    db.ping(reconnect=True)
    # 提交到数据库执行,每1000条提交一次
    sql = 'insert into jobfunction(name,fun_id,url,category_id) values("%s","%s", "%s",%d)' % (str(sql_value[0]), str(sql_value[1]),str(sql_value[2]), sql_value[3])
    # SQL 插入语句
    try:
        mylock2.acquire()
        save_num += 1
        print(save_num)
        cursor.execute(sql)
        db.commit()
        mylock2.release()
    except :
        mylock2.release()
        fp.write(sql + ';\n')
        fp.flush()
        # 如果发生错误则先提交后回滚
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
cursor.execute('truncate table jobfunction')
cursor.execute('SET foreign_key_checks = 1')
sql = 'insert into jobfunction(name,fun_id) values("无","1")'
cursor.execute(sql)
sql1 = 'insert into jobfunction(name,category_id,fun_id) values("无",1,"2")'
cursor.execute(sql1)
db.commit()

f = open("data/function_errsql.txt", "w+", encoding="utf-8")
f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
f.close()

fp = open("data/function_errsql.txt", "a+", encoding="utf-8")

maxsize = 18
q = product_data(user_agent_list)
courls_queue = Queue()

pool = MyThreadPool()
# pool.addthread(queue=q, size=maxsize, func=spider_page)

submission = ["https://www.51job.com/sitemap/position_Navigate.php",user_agent_list[0]]
spider_page(submission)
pool.addthread(queue=courls_queue, size=1, func=insertDB)
pool.startAll()
pool.joinAll()

db.close()
fp.close()

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),save_num, "结束")


