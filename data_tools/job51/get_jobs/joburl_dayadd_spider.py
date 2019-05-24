# -*- coding: utf-8 -*-
__author__ = 'olily'


# 0513创建 爬取岗位URL
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
url_pre = "https://search.51job.com/list/"
url_middle = ",000000,0000,00,0,99,%2B,2,"
url_tail = ".html"

# 设置临界区（资源锁）
mylock = threading.RLock()
mylock2 = threading.RLock()
# 读取城市url
# cityAndurl = pd.read_csv('data/phone_city_url.csv', engine='python')

# 打开数据库连接
db_urllist = pymysql.connect("localhost", "root", "123456", "urllist", charset='utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor_urllist = db_urllist.cursor()
# 清空数据表
cursor_urllist.execute('SET foreign_key_checks = 0')
cursor_urllist.execute('truncate table jobs_get_copy15')
cursor_urllist.execute('SET foreign_key_checks = 1')
db_urllist.commit()

# 打开数据库连接
db_jobsvs = pymysql.connect("localhost", "root", "123456", "jobsvs", charset='utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor_jobsvs = db_jobsvs.cursor()

salary_dict = {'元/天':0,'千/月':2,'万/月':3,'万/年':4}

# 使用execute方法执行SQL语句
cursor_jobsvs.execute("SELECT id,co_id FROM companies")

# 使用 fetchone() 方法获取一条数据
data = cursor_jobsvs.fetchall()
companyDict = {}
for company in data:
    companyDict[company[1]] = company[0]

cursor_jobsvs.execute('select id,name from cities')
cityandidDict = {}
cityandid = cursor_jobsvs.fetchall()
for item in cityandid:
    cityandidDict[item[1]]=item[0]


# 测试速度用
city_num = 0
num = 0
save_num = 0

def getCity ():
    sql = 'select id,city_code from cities'
    cursor_jobsvs.execute(sql)
    cities_list = cursor_jobsvs.fetchall()
    return cities_list

# 解析网页
def html_paser(url):
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
def product_data():
    cities_queue = Queue()
    cities_list = getCity()

    for city_item in cities_list:
        if city_item[0]==1:
            continue
        row = []
        row.append(city_item[0])
        row.append(city_item[1])
        # row.append(user_agent_list[i % 12])
        Producer.producer(cities_queue, row)
    return cities_queue

j=0
# 翻页爬取每一个城市的所有岗位
def turn_page_thread(summission):
    city_code = '000000'
    global num

    j=0
    # 翻页遍历所有岗位
    while (j<=2000):
        j+=1
        city_page_url = url_pre+city_code+url_middle+str(j)+url_tail
        # print(city_page_url)
        html = html_paser(city_page_url)
        if html == 0:
            continue
        job_table= html.find(attrs={'class': 'dw_table'})
        jobs_list = job_table.find_all(attrs={'class': 'el'})
        # 判断是否遍历到达最后一个页面
        if len(jobs_list) ==1:
            print(datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S'), city_code,num,"完成")
            break

        # print(jobs_list)

        company_code=salary_type=put_time=city=None
        salary_low = salary_high=company_id=0

        for items in jobs_list:
            job_basic_div = items.find(attrs={'class': 't1'})
            # print(job_basic_div)
            if job_basic_div.find('input') is None:
                continue
            job_name = job_basic_div.span.a.get('title')
            job_code = job_basic_div.input.get('value')
            job_url = job_basic_div.span.a.get('href')[:-9]
            # print(job_name,job_code)

            company_a = items.find(attrs={'class': 't2'}).a
            if company_a is not None:
                company_url = company_a.get('href')
                regx = re.compile('co[0-9]+.html')
                job_num_str = regx.findall(company_url)
                if len(job_num_str)==0:
                    company_code=None
                else:
                    company_code = job_num_str[0][:-5]
                # print(company_code)
            if company_code not in companyDict.keys():
                continue

            company_id = companyDict[company_code]

            city_span = items.find(attrs={'class': 't3'})
            if city_span is not None:
                city_text = city_span.text.split('-')
                city = city_text[0]
            city_id=1
            if city in cityandidDict.keys():
                city_id = cityandidDict[city]

            salary_span = items.find(attrs={'class': 't4'})
            # print(salary_span)
            if salary_span is not None:
                salary_str = salary_span.text
                if salary_str!= "":
                    # print(salary_str)
                    if salary_str[-3:] not in salary_dict.keys():
                        continue
                    salary_type= salary_dict[salary_str[-3:]]
                    # print(type(salary_str))
                    # print(salary_type)
                    salay_values = salary_str[:-3]
                    salary_couple = salay_values.split('-')
                    if len(salary_couple)!=1:
                        salary_low = salary_couple[0]
                        salary_high = salary_couple[1]
                    else:
                        salary_low = salary_high = salary_couple[0]
                    # print(salary_low,salary_high)

            put_time_span = items.find(attrs={'class': 't5'})
            if put_time_span is not None:
                put_time = put_time_span.text
                # print(put_time)
            # 岗位名，岗位编码，企业编码，薪资（类型）,薪资（低），薪资（高），城市id
            row = [job_name,job_code,company_id,salary_type,salary_low,salary_high,city_id,put_time,job_url]
            # print(row)

            # mylock.acquire()
            num += 1
            # print(2222)
            Producer.producer(joburls_queue, row)
            # print(1111111)
            # mylock.release()

            if num % 10000==0:
                print("num",num)

def insertDB(sql_value):
    # print(11111111111111111111111)
    global save_num
    db_urllist.ping(reconnect=True)
    # 提交到数据库执行,每1000条提交一次
    sql = 'insert into jobs_get_copy15(name,code,company_id,salary_type,salary_low,salary_high,city_id,put_time,url,education_id) values("%s", "%s",%d,"%s", %.2f,%.2f,%d,"%s","%s",1)' % (sql_value[0], str(sql_value[1]), sql_value[2],str(sql_value[3]),float(sql_value[4]),float(sql_value[5]),sql_value[6],str(sql_value[7]),str(sql_value[8]))
    # print(sql)
    # SQL 插入语句
    try:
        mylock2.acquire()
        save_num += 1
        cursor_urllist.execute(sql)
        # print(save_num)
        if save_num % 100 == 0:
            db_urllist.commit()
            if save_num % 10000==0:
                print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),save_num)
        mylock2.release()
    except :
        mylock2.release()
        fp.write(sql + ';\n')
        fp.flush()
        # 如果发生错误则先提交后回滚
        db_urllist.commit()
        db_urllist.rollback()


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

f = open("../data/jobslistsql.txt", "w+", encoding="utf-8")
f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
f.close()

fp = open("../data/jobslistsql.txt", "a+", encoding="utf-8")

maxsize = 1

q = product_data()
joburls_queue = Queue()
# turn_page_thread()

pool = MyThreadPool()
pool.addthread(queue=q, size=maxsize, func=turn_page_thread)
pool.addthread(queue=joburls_queue, size=1, func=insertDB)
pool.startAll()
pool.joinAll()

db_urllist.commit()
db_urllist.close()
fp.close()

# turn_page_thread((18,'032200'))

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),save_num, "结束")
