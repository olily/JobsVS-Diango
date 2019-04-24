# -*- coding: utf-8 -*-
__author__ = 'olily'

# 0401建立文件，爬取51job所有城市分类名称(移动端)
# 多线程处理优化：一条线程跑一个城市
# 0402 将数据写入数据库永久保存

from bs4 import BeautifulSoup as bs
import pandas as pd
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
# 读取城市url
cityAndurl = pd.read_csv('data/phone_city_url.csv', engine='python')

# 测试速度用
city_num = 0
num = 0
save_num = 0


# 解析网页
def html_paser(url, headers):
    try:
        response = requests.get(url, headers)
    except :
        return 0
    else:
        response.encoding = 'utf-8'
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
                task = self.queue.get(block=True, timeout=100)
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

    for i in range(0, cityAndurl.shape[0]):
        data_row = []
        data_row.append(cityAndurl.iloc[i][0])
        data_row.append(cityAndurl.loc[i]['city_url'])
        data_row.append(user_agent_list[i % 12])
        Producer.producer(cities_queue, data_row)
    return cities_queue


# 翻页爬取每一个城市的所有岗位
def turn_page_thread(submission):
    city = submission[0]
    city_url = submission[1]
    browser = submission[2]
    header = {
        'User-Agent': browser,
        'verify': False
    }
    global num

    # 翻页遍历所有岗位
    j = 0
    while (True):
        j += 1
        city_page_url = city_url + 'p' + str(j)
        html = html_paser(city_page_url, header)
        if html == 0:
            continue

        job_href_page = html.find(attrs={'class': 'items'})
        job_href_pages = job_href_page.find_all('a')

        # 判断是否遍历到达最后一个页面
        if len(job_href_pages) == 0:
            global city_num
            city_num += 1
            print(datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S'), city_num, num, city, "完成")
            break

        for page_href in job_href_pages:
            job_url = page_href.get('href')

            regx = re.compile('[0-9]+.html')
            job_num_str = regx.findall(job_url)
            job_num = job_num_str[0][:-5]
            joburl_row = [job_num, city, job_url]

            mylock.acquire()
            num += 1
            Producer.producer(joburls_queue, joburl_row)
            mylock.release()


def insertDB(sql_value):
    global save_num
    db.ping(reconnect=True)
    # 提交到数据库执行,每1000条提交一次
    sql = 'insert into job_url_info values( %d, "%s","%s")' % (int(sql_value[0]), str(sql_value[1]), str(sql_value[2]))
    # SQL 插入语句
    try:
        mylock2.acquire()
        save_num += 1
        cursor.execute(sql)
        if save_num % 1000 == 0:
            db.commit()
            if save_num % 10000==0:
                print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),save_num)
        mylock2.release()
    except :
        mylock2.release()
        fp.write(sql + ';\n')
        fp.flush()
        # 如果发生错误则回滚
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
cursor.execute('truncate table job_url_info')
db.commit()

f = open("data/errsql.txt", "w+", encoding="utf-8")
f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
f.close()

fp = open("data/errsql.txt", "a+", encoding="utf-8")

maxsize = 18
q = product_data(user_agent_list)
joburls_queue = Queue()

pool = MyThreadPool()
pool.addthread(queue=q, size=maxsize, func=turn_page_thread)
pool.addthread(queue=joburls_queue, size=5, func=insertDB)
pool.startAll()
pool.joinAll()

db.commit()
db.close()
fp.close()

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),save_num, "结束")
