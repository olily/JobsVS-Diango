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

# 打开数据库连接
db_urllist = pymysql.connect("localhost", "root", "123456", "urllist", charset='utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor_urllist = db_urllist.cursor()

# 清空数据表
# cursor_urllist.execute('SET foreign_key_checks = 0')
# cursor_urllist.execute('truncate table companies')
# cursor_urllist.execute('SET foreign_key_checks = 1')
# cursor_urllist.execute('truncate table jobs_get_copy1')
# db_urllist.commit()

# 打开数据库连接
# db_jobsvs = pymysql.connect("localhost", "root", "123456", "jobsvs", charset='utf8')
# # 使用 cursor() 方法创建一个游标对象 cursor
# cursor_jobsvs = db_jobsvs.cursor()

salary_dict = {'元/天':0,'千/月':2,'万/月':3,'万/年':4}


# 测试速度用
num = 0

# 解析网页
def html_paser(url):
    try:
        response = requests.get(url)
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
                task = self.queue.get(block=True,timeout=500)
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
    sscursor = pymysql.cursors.SSCursor(db_urllist)
    sscursor.execute('select code,url from jobs_get where status_update=0')
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


# 翻页爬取每一个岗位详细信息
def get_job_detail(items):
    # print(items)
    job_url = items[1]
    # browser = items[2]
    job_id = items[0]

    job_html = html_paser(job_url)
    if job_html == 0:
        return 0
    # print(job_html)

    response = job_html.find(attrs={'class':'tHeader tHjob'})
    study=work_year=workfare=jobfun=None
    if response is not None:
        job_div = job_html.find(attrs={'class': 'msg ltype'}).text
        # print(job_div)
        work_year = study = None
        if job_div is not None:
            job_div_list = job_div.split('|')
            # print(job_div_list)
            if len(job_div_list) >= 3:
                work_year = job_div_list[1].replace('\xa0','')
                study = job_div_list[2].replace('\xa0','')
                # print(work_year,study)

        # # 工作地址
        # work_addr = None
        # work_addr_tag = job_html.find(attrs={'class': 'bmsg inbox'})
        # # print(work_addr_tag)
        # if work_addr_tag is not None:
        #     if work_addr_tag.p is not None:
        #         work_addr = work_addr_tag.p.text
        # # print(work_addr)

        # 岗位描述
        # jd = ""
        # jd_tag = job_html.find(attrs={'class': 'bmsg job_msg inbox'})
        # # print(jd_tag)
        # if jd_tag is not None:
        #     jd_content = jd_tag.contents
        #     print(jd_tag.contents[1].text)
        #     for item in jd_tag.contents:
        #         print(11111,item.text)
        #         jd += item.text + '_'
        # jd = jd[:-1]
        # print(jd)

        # 岗位福利
        workfare = ""
        workfares=job_html.find_all(attrs={'class':'sp4'})
        # print(workfares)
        if len(workfares) !=0 or workfares is not None:
            for welfare in workfares:
                # print(welfare.text)
                workfare += welfare.text+'_'
            workfare = workfare[:-1]
        else:
            workfare = None
        # print(workfare)

        # 岗位职能
        jobfun = ""
        jobfun_fun = job_html.find(attrs={'class': 'fp'})
        jobfun_div = jobfun_fun.findAll(attrs={'class': 'el tdn'})
        if len(jobfun_div)!=0 or jobfun_div is not None :
            for item in jobfun_div:
                jobfun+=item.text+'_'
            jobfun = jobfun[:-1]
            jobfun = jobfun.replace('\r','').replace('\t','').replace('\n','').replace(' ','')

            global num
            job_info = [
                study,
                work_year,
                workfare,
                jobfun, job_id]
            # print(job_info)

            mylock.acquire()
            num += 1
            Producer.producer(jobs_queue, job_info)
            mylock.release()



    if num % 10000 == 0:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "request", num)


def insertDB(sql_value):
    # print("进入insertdb")
    global save_num
    db_urllist.ping(reconnect=True)
    # 提交到数据库执行,每1000条提交一次
    sql = 'update jobs_get set education="%s",work_year="%s",jobfare = "%s",job_fun = "%s",status_update=1 where code="%s"' % (str(sql_value[0]),str(sql_value[1]),str(sql_value[2]),str(sql_value[3]),str(sql_value[4]))
    # print(sql)
    # SQL 插入语句
    try:
        mylock2.acquire()
        save_num += 1
        cursor_urllist.execute(sql)
        # print(save_num)
        # db_urllist.commit()
        # print(sql)
        if save_num % 1000 == 0:
            db_urllist.commit()
            if save_num % 10000 == 0:
                print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"save",save_num)
        mylock2.release()
    except :
        mylock2.release()
        print("err")
        fp.write(sql + ';\n')
        fp.flush()
        # 如果发生错误则先提交再回滚
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

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


f = open("job_update.txt", "w+", encoding="utf-8")
f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
f.close()

fp = open("job_update.txt", "a+", encoding="utf-8")


q = cursor_query()

jobs_queue = Queue()
save_num = 0

pool = MyThreadPool()
pool.addthread(queue=q, size=18,func=get_job_detail)
pool.addthread(queue=jobs_queue, size=1,func=insertDB)
pool.startAll()
pool.joinAll()


db_urllist.close()

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "结束")
