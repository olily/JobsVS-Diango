# -*- coding: utf-8 -*-
__author__ = 'olily'


# 20190314 增加适用多线程翻页爬取岗位url
# 20190314 增加ip和浏览器代理池


from bs4 import BeautifulSoup as bs
import pandas as pd
import pickle
import requests
import re
import threading


# 全局变量保存招聘url
category_jobs = {}


# 翻页爬取每一个分类的所有岗位
def turn_page_thread(jobs_category, browser, start, step):
    header = {
        'User-Agent': browser
    }

    # 遍历所有岗位分类
    for i in range(start, start + step):
        catg_href = jobs_category.loc[i]['href']
        print(catg_href)
        jobs_hrefs = []

        # 翻页遍历所有岗位
        for j in range(1, 31):
            catg_url = catg_href + str(j)
            catg_response = requests.get(
                url=catg_url, headers=header)
            catg_response.encoding = 'utf-8'
            catg_html_text = catg_response.text
            catg_response.close()
            catg_html = bs(catg_html_text, 'html.parser')
            job_href_page = catg_html.find_all(
                href=re.compile('https://www.lagou.com/jobs/[0-9]+'))
            for page_href in job_href_page:
                jobs_hrefs.append(page_href.get('href'))
        category_jobs[jobs_category.loc[i][0]] = jobs_hrefs
        # break


#多线程爬取岗位url
def spider_url_multithread(jobs_category,user_agent_list,thread_num,thread_start_catg):
    # 存放线程作为线程池
    threads_list = []

    # 根据线程数量创建线程函数
    for i in range(0, thread_num):
        if i != thread_num - 1:
            step = len(jobs_category) // thread_num
        else:
            step = len(jobs_category) // thread_num + \
                   len(jobs_category) % thread_num
        thread = threading.Thread(
            target=turn_page_thread,
            args=(
                jobs_category,
                user_agent_list[i],
                thread_start_catg,
                step))
        thread_start_catg += step
        threads_list.append(thread)

    # 启动并加入主线程，两次for循环不能合并，否则无法起到多线程的作用
    for thread in threads_list:
        thread.start()
    for thread in threads_list:
        thread.join()

    print(len(category_jobs))


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

# 获取岗位分类链接
jobs_category = pd.read_csv("data/lagou_categorys.csv")

# 多线程爬取url
spider_url_multithread(jobs_category,user_agent_list,12,0)

# 写入文件
with open('data/category_jobs.pkl', 'wb') as f:
    pickle.dump(category_jobs, f)
print("结束")