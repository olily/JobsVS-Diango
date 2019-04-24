# -*- coding: utf-8 -*-
__author__ = 'olily'

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import pickle
import numpy as np
import re

import json
import random
from lxml import etree

ips = pd.read_csv("data/ips.csv")
# print(random.choice(ips['ip']))
# exit()

jobs_category = pd.read_csv("data/lagou_categorys.csv")
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
#
header = {
    # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'
    }

# category_jobs = {}
# for catg in jobs_category.iterrows():
#     catg_href = catg[1][-1]
#     # print(catg_href)
#
#     jobs_hrefs = []
#     # 翻页查询
#     for i in range(1, 2):
#         catg_url = catg_href + str(i)
#         catg_response = requests.get(url=catg_url, headers=header)
#         catg_response.encoding = 'utf-8'
#         catg_html_text = catg_response.text
#         catg_html = bs(catg_html_text, 'html.parser')
#         job_href_page = catg_html.find_all(
#             href=re.compile('https://www.lagou.com/jobs/[0-9]+'))
#         # jobs_hrefs += job_href_page
#         for page_href in job_href_page:
#             jobs_hrefs.append(page_href.get('href'))
#         # print(len(jobs_hrefs))
#
#     category_jobs[catg[1][0]] = jobs_hrefs
#     # print(category_jobs)
#     # print(catg_html)
#     # print(jobs_hrefs)
#     break
# print(category_jobs)
# with open('data/category_jobs.pkl', 'wb',encoding='utf-8') as f:
#     pickle.dump(category_jobs, f)


with open('data/category_jobs.pkl', 'rb') as f:
    category_jobs = pickle.load(f, encoding='utf-8')


# 分类，岗位名称，岗位代码，公司，薪水，工作城市，地址，岗位描述，经验，学历，标签，工作性质
jobs = pd.DataFrame(
    columns=[
        'category_no',
        'job_name',
        'job_no',
        'salary',
        'company',
        'work_city',
        'work_addr',
        'lables',
        'exp',
        'edu',
        'nature',
        'adv',
        'jd'])
index = 1
for key in category_jobs:
    for job_href in category_jobs[key]:
        # print(job_href)s
        # print(index)
        # ips_li = ['180.164.24.165:53281','61.189.242.243:55484','61.145.182.27:53281','116.209.54.84:9999']
        # proxies = {'https':random.choice(ips['ip'])}
        proxies = {'https': '116.209.54.84:9999'}
        # proxies = {'https': random.choice(ips_li)}
        # print(proxies)
        job_response = requests.get(url=job_href, proxies = proxies,headers=header)
        job_response.encoding = 'utf-8'
        job_html_text = job_response.text
        job_html = bs(job_html_text, 'html.parser')
        print(job_html)
        with open('data/jod_test.html','w',encoding='utf-8') as f :
            f.write(job_html_text)

        # 开始保存数据
        # category_no = key
        job_name = None
        # print(job_html.find(attrs={'class': 'name'}))
        if job_html.find(attrs={'class': 'name'})!=None:
            job_name = job_html.find(attrs={'class': 'name'}).text
        # job_name = job_html.find(attrs={'class': 'name'}).text
        # print(job_name)
        job_no = job_href[-12:-5]
        # print(job_no)
        salary = None
        if job_html.find(attrs={'class': 'salary'})!=None:
            salary = job_html.find(attrs={'class': 'salary'}).text
        # print(salary)
        company = None
        if job_html.find(attrs={'class': 'company'})!=None:
            company = job_html.find(attrs={'class': 'company'}).text
        # print(company)
        work_city = None
        if job_html.find(attrs={'name': "workAddress"})!=None:
            work_city = job_html.find(attrs={'name': "workAddress"}).get('value')
        # print(work_city)
        work_addr = None
        if job_html.find(attrs={'name': "positionAddress"})!=None:
            work_addr = job_html.find( attrs={'name': "positionAddress"}).get('value')
        # print(work_addr)
        lables = []
        exp=edu=nature=None
        all_lable = job_html.find_all(attrs={'class': 'labels'})
        if all_lable!=None:
            for lable in all_lable:
                lables.append(lable.text)
            # print(lables)
            job_request = job_html.find(attrs={'class': 'job_request'})
            if job_request!=None:
                # print(job_request)
                exp = job_request.find_all('span')[-3].text.replace('/', '')
                # print(exp)
                edu = job_request.find_all('span')[-2].text.replace('/', '')
                # print(edu)
                nature = job_request.find_all('span')[-1].text.replace('/', '')
                # print(nature)
        adv = None
        if job_html.find(attrs={'class': 'job-advantage'})!=None:
            adv = job_html.find(attrs={'class': 'job-advantage'}).p.text
        # print(adv)
        jd = None
        if job_html.find(attrs={'class': 'job-detail'})!=None:
            jd = job_html.find(attrs={'class': 'job-detail'}).text
        # print(jd)

        jobs.loc[index] = [
            key,
            job_name,
            job_no,
            salary,
            company,
            work_city,
            work_addr,
            lables,
            exp,
            edu,
            nature,
            adv,
            jd]
        index += 1
        # print(index)
        # print(jobs)
        break
        # if index==3:
        #     break

print(jobs)
# jobs.to_csv('data/jobs.csv',encoding='utf-8')
