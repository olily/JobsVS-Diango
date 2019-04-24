# -*- coding: utf-8 -*-
__author__ = 'olily'

# 20190307 创建：基于登录的拉勾网信息数据爬取

import requests
import re
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import pickle
import random

session = requests.Session()

def user_agent():
    #浏览器列表,每次访问可以用不同的浏览器访问
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
    #随机选取一个浏览器访问
    user_agent = random.choice(user_agent_list)
    return user_agent
    #调用拉钩函数
    # lagou(page,user_agent)

# 步骤一、首先登陆login.html，获取cookie
r1 = session.get(
    'https://passport.lagou.com/login/login.html',
    headers={
        'Host': "passport.lagou.com",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'})

X_Anti_Forge_Token = re.findall(
    r"window.X_Anti_Forge_Token = '(.*)';", r1.text)[0]
X_Anti_Forge_Code = re.findall(
    r"window.X_Anti_Forge_Code = '(.*)';",
    r1.text)[0]

# 步骤二、用户登陆，携带上一次的cookie，后台对cookie中的 jsessionid 进行授权
r3 = session.post(
    url='https://passport.lagou.com/login/login.json',
    data={
        'isValidate': True,
        # 'username': '424662508@qq.com',
        # 'password': '4c4c83b3adf174b9c22af4a179dddb63',
        'username': '18611453110',
        'password': 'bff642652c0c9e766b40e1a6f3305274',
        'request_form_verifyCode': '',
        'submit': '',
    },
    headers={
        'X-Anit-Forge-Code': X_Anti_Forge_Code,
        'X-Anit-Forge-Token': X_Anti_Forge_Token,
        'X-Requested-With': 'XMLHttpRequest',
        "Referer": "https://passport.lagou.com/login/login.html",
        "Host": "passport.lagou.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    },
)
print(r3.text)
# print(r3.headers)

# 步骤三：进行授权
r4 = session.get(
    'https://passport.lagou.com/grantServiceTicket/grant.html',
    allow_redirects=False,
    headers={
        'Host': "passport.lagou.com",
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'})

# print(r4.headers)
location = r4.headers['Location']
# print(location)

# 步骤四：请求重定向的地址，拿到最终的登录session
r5 = session.get(
    location,
    allow_redirects=True,
    headers={
        'Host': "www.lagou.com",
        'Referer': 'https://passport.lagou.com/login/login.html?',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'})

# print(r5.headers)

# ===============以上是登录环节


# 步骤一：分析
# 搜索职位的url样例：https://www.lagou.com/jobs/list_python%E5%BC%80%E5%8F%91?labelWords=&fromSearch=true&suginput=
ips = pd.read_csv("data/ips.csv")
jobs_category = pd.read_csv("data/lagou_categorys.csv")


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
        useragent=user_agent()
        print(useragent)
        headers = {
            'Host': "www.lagou.com",
            'Referer': 'https://passport.lagou.com/login/login.html?',
            'User-Agent': useragent
        }

        proxies = {'https': '116.209.54.84:9999'}
        # proxies = {'https': random.choice(ips_li)}
        # print(proxies)
        job_response = session.get(
            url=job_href, headers=headers)
        job_response.encoding = 'utf-8'
        job_html_text = job_response.text
        job_html = bs(job_html_text, 'html.parser')
        print(job_html.find_all(attrs={'class':'unick bl'}))
        with open('data/jod_test.html', 'w', encoding='utf-8') as f:
            f.write(job_html_text)

        # 开始保存数据
        # category_no = key
        job_name = None
        # print(job_html.find(attrs={'class': 'name'}))
        if job_html.find(attrs={'class': 'name'}) is not None:
            job_name = job_html.find(attrs={'class': 'name'}).text
        # job_name = job_html.find(attrs={'class': 'name'}).text
        # print(job_name)
        job_no = job_href[-12:-5]
        # print(job_no)
        salary = None
        if job_html.find(attrs={'class': 'salary'}) is not None:
            salary = job_html.find(attrs={'class': 'salary'}).text
        # print(salary)
        company = None
        if job_html.find(attrs={'class': 'company'}) is not None:
            company = job_html.find(attrs={'class': 'company'}).text
        # print(company)
        work_city = None
        if job_html.find(attrs={'name': "workAddress"}) is not None:
            work_city = job_html.find(
                attrs={'name': "workAddress"}).get('value')
        # print(work_city)
        work_addr = None
        if job_html.find(attrs={'name': "positionAddress"}) is not None:
            work_addr = job_html.find(
                attrs={'name': "positionAddress"}).get('value')
        # print(work_addr)
        lables = []
        exp = edu = nature = None
        all_lable = job_html.find_all(attrs={'class': 'labels'})
        if all_lable is not None:
            for lable in all_lable:
                lables.append(lable.text)
            # print(lables)
            job_request = job_html.find(attrs={'class': 'job_request'})
            if job_request is not None:
                # print(job_request)
                exp = job_request.find_all('span')[-3].text.replace('/', '')
                # print(exp)
                edu = job_request.find_all('span')[-2].text.replace('/', '')
                # print(edu)
                nature = job_request.find_all('span')[-1].text.replace('/', '')
                # print(nature)
        adv = None
        if job_html.find(attrs={'class': 'job-advantage'}) is not None:
            adv = job_html.find(attrs={'class': 'job-advantage'}).p.text
        # print(adv)
        jd = None
        if job_html.find(attrs={'class': 'job-detail'}) is not None:
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
        # break
        # if index==3:
        #     break

print(jobs)
jobs.to_csv('data/jobs.csv',encoding='utf-8')
