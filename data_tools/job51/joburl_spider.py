# -*- coding: utf-8 -*-
__author__ = 'olily'

# 0330创建，开始编写爬取岗位爬虫
# 添加异步写入数据库

from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import re
import threading

mylock = threading.RLock()

cityAndurl = pd.read_csv('data/city_url.csv',engine='python')
# ,encoding='gb2312'

num = 0
city_num = 0

columns = ['city','job_url']
index = []
jobs_urls = pd.DataFrame(columns=columns)

# 解析网页
def html_paser(url,headers):
    try:
        response = requests.get(url, headers)
    except:
        return 0
    else:
        html_text = response.text

        html = bs(html_text,'html.parser')
        return html


# 翻页爬取每一个城市的所有岗位
def turn_page_thread(browser, start, step):
    header = {
        'User-Agent': browser,
        'verify':  False
    }

    # 遍历城市
    for i in range(start, start + step):
        city_url = cityAndurl.loc[i]['city_url']
        # print(city_url)
        city = cityAndurl.iloc[i][0]
        page_num = cityAndurl.loc[i]['page_num']

        # 翻页遍历所有岗位
        for j in range(1, page_num+1):
            city_page_url = city_url + 'p'+str(j)
            html = html_paser(city_page_url,header)
            if html == 0:
                break

            job_href_page = html.find_all(
                href=re.compile('https://jobs.51job.com/[a-z]+-[a-z]*/[0-9]+.html?'))

            for page_href in job_href_page:
                global num
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

                # print(num)
                # print(job_num,job_url,city)
        global city_num
        city_num+=1
        print(city_num,num,city,"完成")
            # break


#多线程爬取岗位url
def spider_url_multithread(user_agent_list,thread_num,thread_start_catg):
    # 存放线程作为线程池
    threads_list = []

    # 根据线程数量创建线程函数
    for i in range(0, thread_num):
        if i != thread_num - 1:
            step = len(cityAndurl) // thread_num
        else:
            step = len(cityAndurl) // thread_num + \
                   len(cityAndurl) % thread_num
        thread = threading.Thread(
            target=turn_page_thread,
            args=(
                user_agent_list[i%12],
                thread_start_catg,
                step))
        thread_start_catg += step
        threads_list.append(thread)

    # 启动并加入主线程，两次for循环不能合并，否则无法起到多线程的作用
    for thread in threads_list:
        thread.start()
    for thread in threads_list:
        thread.join()

    # print(len(jobs_urls))


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
# jobs_category = pd.read_csv("data/lagou_categorys.csv")

#多线程爬取url
spider_url_multithread(user_agent_list,18,0)

jobs_urls.to_csv('data/jobs_urls2.csv')


print("结束")