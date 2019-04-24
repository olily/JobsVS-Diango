# -*- coding: utf-8 -*-
__author__ = 'olily'

# 0401创建，开始编写爬取具体岗位信息
# 采用生产者-消费者模型：producter customer


from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import threading
from queue import Queue
import datetime

# 设置临界区（资源锁）
mylock = threading.RLock()

# 读取岗位url
jobAndurl = pd.read_csv('data/phone_jobs_urls3.csv', engine='python')

# 创建dataframe用于保存数据
columns = [
    'job_name',
    'job_url',
    'put_time',
    'salary',
    'city',
    'city_zh',
    'recruit_num',
    'work_year',
    'study',
    'company',
    'company_url',
    'work_addr',
    'jd',
    'jd_duty',
    'jd_require',
    'workfare']
index = []
jobs_detail = pd.DataFrame(columns=columns)

# 测试速度用
num = 0


# 解析网页
def html_paser(url, headers):
    try:
        response = requests.get(url, headers)
    except BaseException:
        return 0
    else:
        response.encoding = 'gb2313'
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
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while(True):
            try:
                task = self.queue.get(block=False)
                get_job_detail(task)
                self.queue.task_done()
            except BaseException:
                break


# 建立线程池
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
    joburls_queue = Queue()
    for i in range(0, jobAndurl.shape[0]):
        # 将岗位编号append到索引index
        index.append(jobAndurl.iloc[i][0])

        # put到队列
        data_row = []
        data_row.append(jobAndurl.iloc[i][0])
        data_row.append(jobAndurl.loc[i]['job_url'])
        data_row.append(jobAndurl.loc[i]['city'])
        data_row.append(user_agent_list[i % 12])
        Producer.producer(joburls_queue, data_row)

    return joburls_queue


# 翻页爬取每一个岗位的所有信息
def get_job_detail(items):
    job_url = items[1]
    browser = items[3]
    job_num = items[0]
    city = items[2]

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
    city_zh = None
    if div1 is not None:
        if div1.p is not None:
            job_name = div1.p.text
        if div1.span is not None:
            put_time = div1.span.text
        if div1.em is not None:
            city_zh = div1.em.text

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

    # 公司链接
    company_url = None
    company_url_tag = job_html.find(attrs={'class': 's_n'})
    if (company_url_tag is not None):
        company_url = company_url_tag.get('href')

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

    # 恭喜资源设置锁
    mylock.acquire()
    global num
    num += 1
    jobs_detail.loc[job_num] = [
        job_name,
        put_time,
        city,
        city_zh,
        salary,
        recruit_num,
        work_year,
        study,
        company,
        company_url,
        work_year,
        work_addr,
        jd,
        None,
        None,
        workfare]
    mylock.release()

    if num % 1000 == 0:
        print(num)




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

maxsize = 18
q = product_data(user_agent_list)
pool = MyThreadPool(queue=q, size=maxsize)
pool.startAll()
pool.joinAll()

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
print(num)

jobs_detail.to_csv('data/mphone_jobs.csv')

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "结束")
