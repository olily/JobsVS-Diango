# -*- coding: utf-8 -*-
__author__ = 'olily'

# 20190310 创建：基于selenium模拟登录的拉勾网信息数据爬取
# 20190315 增加多线程爬取每一个招聘岗位的信息


import time
from selenium import webdriver  # 导入模块
from bs4 import BeautifulSoup as bs
import pandas as pd
import pickle
import requests
import re
import os
import threading
import time
import random
import csv


# 登录拉勾以及手动验证
def GetCookies(username_str, password_str):
    # 声明浏览器对象
    driver = webdriver.Firefox()
    # 访问地址
    driver.get('https://passport.lagou.com/login/login.html')

    # 定位到账号密码输入框
    username = driver.find_element_by_xpath(
        '/html/body/section/div[2]/div[1]/div[2]/form/div[1]/input')
    username.send_keys(username_str)
    password = driver.find_element_by_xpath(
        '/html/body/section/div[2]/div[1]/div[2]/form/div[2]/input')
    password.send_keys(password_str)
    login_submit = driver.find_element_by_xpath(
        '/html/body/section/div[2]/div[1]/div[2]/form/div[5]/input')
    login_submit.click()

    # 等待手动验证
    time.sleep(30)
    print('登录成功')
    cookies = driver.get_cookies()
    driver.quit()
    return cookies
    # return driver


def get_session():  # 获取session
    s = requests.Session()
    if not os.path.exists('session.txt'):  # 如果没有session，则创建一个，并且保存到文件中
        s.headers.clear()
        for cookie in GetCookies('18281580281', 'pxm123456'):
            s.cookies.set(cookie['name'], cookie['value'])
        save_session(s)
    else:
        # 如果已存在session，则直接加载使用
        s = load_session()
    return s


def save_session(session):  # 保存session，下次可直接使用，避免再次登录
    with open('session.txt', 'wb') as f:
        pickle.dump(session, f)
    print("Cookies have been writed.")


def load_session():  # 加载session
    with open('session.txt', 'rb') as f:
        s = pickle.load(f)
    return s


# 获取解析每一个页面的HTML信息
def get_content(session, url):
    content = session.get(url).text
    # time.sleep(1)
    # content = driver.page_source.encode('utf-8')
    soup = bs(content, 'html.parser')
    return soup

# 保存岗位内容至dataframe


def save_jobs(session, category_jobs, job_part, keys, csv_name, columns):
    csvfile = open("data/lagou/" + csv_name + ".csv", "a+",encoding="utf-8")
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(columns)
    index = 0
    for key in keys:
        for job_href in category_jobs[key]:
            job_html = get_content(session, job_href)
            # print(job_href)
            job_name = None
            if job_html.find(attrs={'class': 'name'}) is not None:
                job_name = job_html.find(attrs={'class': 'name'}).text
            job_no = job_href[-12:-5]
            salary = None
            if job_html.find(attrs={'class': 'salary'}) is not None:
                salary = job_html.find(attrs={'class': 'salary'}).text
            company = None
            if job_html.find(attrs={'class': 'company'}) is not None:
                company = job_html.find(attrs={'class': 'company'}).text
            work_city = None
            if job_html.find(attrs={'name': "workAddress"}) is not None:
                work_city = job_html.find(
                    attrs={'name': "workAddress"}).get('value')
            work_addr = None
            if job_html.find(attrs={'name': "positionAddress"}) is not None:
                work_addr = job_html.find(
                    attrs={'name': "positionAddress"}).get('value')
            lables = []
            exp = edu = nature = None
            all_lable = job_html.find_all(attrs={'class': 'labels'})
            if all_lable is not None:
                for lable in all_lable:
                    lables.append(lable.text)
                job_request = job_html.find(attrs={'class': 'job_request'})
                if job_request is not None:
                    exp = job_request.find_all(
                        'span')[-3].text.replace('/', '')
                    edu = job_request.find_all(
                        'span')[-2].text.replace('/', '')
                    nature = job_request.find_all(
                        'span')[-1].text.replace('/', '')
            adv = None
            if job_html.find(attrs={'class': 'job-advantage'}) is not None:
                adv = job_html.find(attrs={'class': 'job-advantage'}).p.text
            jd = None
            if job_html.find(attrs={'class': 'job-detail'}) is not None:
                jd = job_html.find(attrs={'class': 'job-detail'}).text

                jobinfo = [
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
                csvwriter.writerow(jobinfo)
                job_part.loc[index] = jobinfo
            # print(job_href + "    " + job_name)

            # print(jobs.loc[index])
            index += 1

# 将岗位键根据线程数量分组


def key_to_keys(category_jobs, thread_num):
    key_list = []
    j = 0
    keys = []
    for key in category_jobs:
        if j == len(category_jobs) // thread_num:
            key_list.append(keys)
            j = 0
            keys = []
        keys.append(key)
        j += 1

    # print(key_list)
    return key_list


# 多线程保存岗位信息
def save_jobsinfo_multithread(category_jobs, key_list):
    # 存放线程作为线程池
    threads_list = []
    # 保存每一个分组的线程函数返回值（Dataframe）
    jobs_list = []
    # 分类，岗位名称，岗位代码，公司，薪水，工作城市，地址，岗位描述，经验，学历，标签，工作性质
    columns = [
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
        'jd']
    jobs = pd.DataFrame(columns=columns)

    # 登录
    session = get_session()
    i = 1
    for keys in key_list:
        job_part = jobs.copy()
        jobs_list.append(job_part)
        csv_name = "jobs" + str(i)
        thread = threading.Thread(
            target=save_jobs,
            args=(session, category_jobs, job_part, keys, csv_name, columns))
        i += 1
        threads_list.append(thread)

    # 启动并加入主线程，两次for循环不能合并，否则无法起到多线程的作用
    for thread in threads_list:
        # print(thread)
        thread.start()
    for thread in threads_list:
        thread.join()

    jobs_result = jobs.copy()

    for part in jobs_list:
        jobs_result = jobs_result.append(part)
    return jobs_result


with open('data/category_jobs.pkl', 'rb') as f:
    category_jobs = pickle.load(f)
# print(category_jobs)
# length = 0
# inn = 0
# for catg in category_jobs:
#     inn += 1
#     length += len(category_jobs[catg])
#
# print(inn, length)

thread_num = 15

key_list = key_to_keys(category_jobs, thread_num)

jobs = save_jobsinfo_multithread(category_jobs, key_list)

jobs.to_csv('data/jobs_info.csv',encoding='utf-8')
