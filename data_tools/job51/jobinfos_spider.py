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
def html_paser(url, headers):
    try:
        response = requests.get(url, headers)
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
def cursor_query(user_agent_list):
    joburls_queue = Queue()
    query_num = 0
    # 首先查询全量数据
    sscursor = pymysql.cursors.SSCursor(db)
    sscursor.execute('select * from job_url_info')
    while True:
        # 每次获取时会从上次游标的位置开始移动size个位置，返回size条数据
        data = sscursor.fetchone()
        # 数据为空的时候中断循环
        if not data:
            break
        data_row = []
        data_row.append(data[0])
        data_row.append(data[2])
        data_row.append(user_agent_list[query_num%12])
        # print(data_row)
        Producer.producer(joburls_queue, data_row)
        query_num += 1
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),query_num)
    sscursor.close()
    del sscursor
    return joburls_queue


# 翻页爬取每一个岗位的所有信息
def get_job_detail(items):
    job_url = items[1]
    browser = items[2]
    job_num = items[0]

    header = {
        'User-Agent': browser,
        'verify': False
    }

    job_html = html_paser(job_url, header)
    if job_html == 0:
        return 0

    # 岗位名、发布时间、城市
    div1 = job_html.find(attrs={'class': 'jt'})
    job_name = None
    put_time = None
    if div1 is not None:
        if div1.p is not None:
            job_name = div1.p.text
        if div1.span is not None:
            put_time = div1.span.text

    # 薪资
    salary = None
    salary_tag = job_html.find(attrs={'class': 'jp'})
    if salary_tag is not None:
        salary = salary_tag.text

    # 招聘人数
    recruit_num = None
    recruit_num_tag = job_html.find(attrs={'class': 's_r'})
    if recruit_num_tag is not None:
        recruit_num = recruit_num_tag.text

    # 工作年限
    work_year = None
    work_year_tag = job_html.find(attrs={'class': 's_n'})
    if(work_year_tag is not None):
        work_year = work_year_tag.text

    # 学历
    study = None
    study_tag = job_html.find(attrs={'class': 's_x'})
    if study_tag is not None:
        study = study_tag.text

    # 公司名称
    company = None
    company_tag = job_html.find(attrs={'class': 'c_444'})
    if company_tag is not None:
        company = company_tag.text

    # 工作地址
    work_addr = None
    work_addr_tag = job_html.find(attrs={'class': 'arr a2'})
    if work_addr_tag is not None:
        if work_addr_tag.span is not None:
            work_addr = work_addr_tag.span.text

    # 岗位描述
    jd = None
    jd_tag = job_html.find(attrs={'class': 'ain'})
    if jd_tag is not None:
        if jd_tag.article is not None:
            jd = jd_tag.article.text

    # 岗位福利
    workfare = []
    workfares_tags = job_html.find(attrs={'class': 'welfare'})
    if workfares_tags is not None:
        workfares = workfares_tags.find_all('span')
        for welfare in workfares:
            workfare.append(welfare.text)
    else:
        workfare = None

    global num
    num += 1
    job_info = [
        job_num,
        job_name,
        put_time,
        salary,
        recruit_num,
        work_year,
        study,
        company,
        work_addr,
        jd,
        workfare]
    mylock.acquire()
    Producer.producer(jobs_queue,job_info)
    mylock.release()

    if num % 10000 == 0:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"request",num)


def insertDB(sql_value):
    global save_num
    db.ping(reconnect=True)
    # 提交到数据库执行,每1000条提交一次
    sql = 'insert into job_info values(%d, "%s", "%s","%s", "%s", "%s", "%s", "%s","%s", "%s","%s")' % (sql_value[0],str(sql_value[1]),str(sql_value[2]),str(sql_value[3]),str(sql_value[4]),str(sql_value[5]),str(sql_value[6]), str(sql_value[7]), str(sql_value[8]),str(sql_value[9]),str(sql_value[10]))
    # SQL 插入语句
    try:
        mylock2.acquire()
        save_num += 1
        cursor.execute(sql)
        print(save_num)
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
db = pymysql.connect("localhost", "root", "123456", "jobs51", charset='utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

cursor.execute('truncate table job_info')
db.commit()

f = open("data/job_info_errsql.txt", "w+", encoding="utf-8")
f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
f.close()

fp = open("data/job_info_errsql.txt", "a+", encoding="utf-8")


q = cursor_query(user_agent_list)

jobs_queue = Queue()
save_num = 0

pool = MyThreadPool()
pool.addthread(queue=q, size=18,func=get_job_detail)
pool.addthread(queue=jobs_queue, size=5,func=insertDB)
pool.startAll()
pool.joinAll()


db.close()

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "结束")
