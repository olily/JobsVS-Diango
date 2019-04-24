# -*- coding: utf-8 -*-
__author__ = 'olily'

#导入要用到的模块
import requests #网络请求
import re
import pandas as pd  #数据框操作
import numpy as np
import time  #增加延时
import random


# 反爬虫机制
header = {'Accept':'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9',
'Connection':'keep-alive',
'Content-Length':'20',
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
#Cookie:LGUID=20161214153335-9f0eacc2-c1cf-11e6-bd6c-5254005c3644; user_trace_token=20180122030442-efefe00e-fedd-11e7-b2cb-525400f775ce; LG_LOGIN_USER_ID=e619b07cb5d026e017473de3d4ef1bb5a3da9a0ddd6ea0a5; gray=resume; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%227288096%22%2C%22%24device_id%22%3A%221626117eb3016-0703ff024b7ae5-71292b6e-1049088-1626117eb3569%22%2C%22first_id%22%3A%221626117eb3016-0703ff024b7ae5-71292b6e-1049088-1626117eb3569%22%7D; WEBTJ-ID=20180403125347-16289da9860300-0dcabf1bb6b166-71292b6e-1049088-16289da98619b; login=true; unick=%E6%8B%89%E5%8B%BE%E7%94%A8%E6%88%B73739; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; gate_login_token=63a7401b950e42d41a03d8ce1db134ac22aeefc46c120c43; index_location_city=%E6%B7%B1%E5%9C%B3; JSESSIONID=ABAAABAAADEAAFIDFE252684FD90098F44851E32F917A9F; TG-TRACK-CODE=search_code; SEARCH_ID=e267bafce9b0431d8f8a867e48f2a7bf; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1522167431,1522215930,1522219100,1522731245; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1522741185; _gat=1; _ga=GA1.2.983742987.1481700649; _gid=GA1.2.1178844706.1522731227; LGSID=20180403154252-9d580c63-3712-11e8-b228-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%25E6%2595%25B0%25E6%258D%25AE%25E5%2588%2586%25E6%259E%2590%3Fcity%3D%25E6%25B7%25B1%25E5%259C%25B3%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; LGRID=20180403154252-9d580e4e-3712-11e8-b228-525400f775ce; _putrc=2C1A435C1A81EDB8
'Host':'www.lagou.com',
'Origin':'https://www.lagou.com',
'Referer':'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?city=%E6%B7%B1%E5%9C%B3&cl=false&fromSearch=true&labelWords=&suginput=',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36',
'X-Anit-Forge-Code':'0',
'X-Anit-Forge-Token':'None',
'X-Requested-With':'XMLHttpRequest'}

dat = {'first':'false',
       'kd':'数据分析',
       'pn':'1'}     #这是我们刚刚复制的内容
url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'    #真实网址
html = requests.request('POST',url,data=dat,headers=header)
#进行请求

# data = re.findall('"companyId":.*?,"workYear":"(.*?)","education":"(.*?)","city":"(.*?)","positionName":"(.*?)","companyLogo":".*?","companyShortName":"(.*?)","positionLables":.*?,"industryLables":.*?,"businessZones":.*?,"score":.*?,"approve":.*?,"jobNature":".*?","companyLabelList":(.*?),"publisherId":.*?,"district":"(.*?)","companySize":".*?","createTime":".*?","positionAdvantage":".*?","salary":"(.*?)"',html.text)

# 数据分析岗位有30页，用for循环实现翻页
for i in range(1, 31):
    print(i)
    # 写入真实网址，不是网页上的网址，是在消息头那，别的浏览器是Headers
    url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'

    # 提交数据,在参数那一栏，把这个复制过来，然后加上引号和逗号
    dat = {'first': 'false',
           'kd': '数据分析',
           'pn': '3', }

    time.sleep(random.randint(2, 10))

    html = requests.request('POST', url, data=dat, headers=header)
    # print(html)

    # 用正则表达式来提取数据
    # 在jupyterF5找出你想要的信息，然后复制你想要的信息，像我的话直接复制到薪水就可以了
    data = re.findall(
        '"companyId":.*?,"workYear":"(.*?)","education":"(.*?)","city":"(.*?)","positionName":"(.*?)","companyLogo":".*?","companyShortName":"(.*?)","positionLables":.*?,"industryLables":.*?,"businessZones":.*?,"score":.*?,"approve":.*?,"jobNature":".*?","companyLabelList":(.*?),"publisherId":.*?,"district":"(.*?)","companySize":".*?","createTime":".*?","positionAdvantage":".*?","salary":"(.*?)"',
        html.text)

    # 转成数据框
    data2 = pd.DataFrame(data)

    # 写入本地
    # header、index是行名、列名的意思，让他们等于False的意思是，原来的行名和列名我们都不要，mode=a+就是要追加信息，
    # 就是你要继续加信息的时候，他会往下写。而不是把你之前的信息覆盖掉
    # 执行完毕后，可在刚刚的文件夹里发现csv文件
    data2.to_csv('data\\lagoujob.csv', header=False, index=False, mode='a+')