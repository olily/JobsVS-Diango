# -*- coding: utf-8 -*-
__author__ = 'olily'

# 0401建立文件，爬取51job所有城市分类名称(移动端)
# 缩线程处理优化：一条线程跑一个城市
# 0402 将数据写入数据库永久保存

from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import threading
from queue import Queue
import datetime
import re
import pymysql

# 打印当前时间
nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 设置临界区（资源锁）
mylock = threading.RLock()

# 读取城市url
cityAndurl = pd.read_csv('data/phone_city_url.csv', engine='python')
# ,encoding='gb2312'

# 创建dataframe用于保存数据
columns = ['city', 'job_url']
index = []
jobs_urls = pd.DataFrame(columns=columns)

# 测试速度用
num = 0
city_num = 0


# 解析网页
def html_paser(url, headers):
    try:
        response = requests.get(url, headers)
    except BaseException:
        return 0
    else:
        html_text = response.text

        html = bs(html_text, 'html.parser')
        return html


class Producer(object):
    @staticmethod
    def producer(q, data):
        q.put(data)


class Customer(object):

    @staticmethod
    def customer(q):
        while (q.empty() == 0):
            submission = q.get()
            # print(submission)
            turn_page_thread(submission)


class MyThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        # self.start()

    def run(self):
        while True:
            try:
                task = self.queue.get(block=False)
                turn_page_thread(task)
                self.queue.task_done()
            except:
                break


class MyThreadPool():
    def __init__(self, queue, size):
        self.queue = queue
        self.pool = []
        for i in range(size):
            self.pool.append(MyThread(queue))

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

        global num
        # 判断是否遍历到达最后一个页面
        if len(job_href_pages) == 0:
            global city_num
            city_num += 1
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), city_num, num, city, "完成")
            break

        for page_href in job_href_pages:
            num += 1
            job_url = page_href.get('href')

            regx = re.compile('[0-9]+.html')
            job_num_str = regx.findall(job_url)
            job_num = job_num_str[0][:-5]

            mylock.acquire()
            index.append(job_num)
            jobs_urls.loc[job_num, 'job_url'] = job_url
            jobs_urls.loc[job_num, 'city'] = city
            mylock.release()


def insertDB(table_name, index_id, sql_value):
    db.ping(reconnect=True)
    # SQL 插入语句
    try:
        # 执行sql语句
        cursor.execute(
            'insert into job_url_info values( %d, "%s", "%s", "%s")' % (
            index_id, str(sql_value[0]), str(sql_value[1][0]), str(sql_value[1][1])))
        # 提交到数据库执行
        db.commit()
    except BaseException:
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
db = pymysql.connect("localhost", "root", "123456", "jobs51")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

cursor.execute('truncate table job_info')
db.commit()

maxsize = 18
q = product_data(user_agent_list)

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

pool = MyThreadPool(queue=q, size=maxsize)
pool.startAll()
pool.joinAll()


print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "结束")
