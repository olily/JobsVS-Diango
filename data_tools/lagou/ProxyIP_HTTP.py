# -*- coding: utf-8 -*-
__author__ = 'olily'
# 20190217 过滤失效IP
# 20190228 解决代理IP不成功问题：http无法爬取https网站，反之亦然。所以重新爬取代理ip、建立ip池

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import random
import re


# 反爬虫机制
header = {
    # 'Referer': 'https://www.kuaidaili.com/free/inha/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36',
}












# 爬取http代理ip，网站为www.kuaidaili.com/free/inha
# 开始爬取代理ip
ips = []
# for pg in range(1,6):
#     # print(pg)
#     url = 'https://www.kuaidaili.com/free/inha/'+str(pg)
#     # print(url)
#     response = requests.get(url=url, headers=header)
#     response.encoding = 'utf-8'
#     html = response.text
#     soup = bs(html, 'html.parser')
#     tags = soup.find_all(attrs={'data-title': 'IP'})
#     for i in tags:
#         proxies = {'http':i.string}
#         # proxies = {'http': '182.150.21.204'}
#         # print(proxies)
#         try:
#             ip_response = requests.get(url='https://www.baidu.com', headers=header, proxies=proxies,timeout=10)
#             # print(ip_response)
#             # if ip_response == 200:
#         except:
#             continue
#         else:
#             # print(ip_response)
#             ips.append(i.string)
#
#


# 测试返回本机ip，验证是否代理设置成功
ips_set = pd.read_csv("data/ips.csv")
proxy = {'http': random.choice(ips_set['ip'])}
print(proxy)
res = requests.get(url="https://www.ipip.net/", headers=header)
# status = res.status_code  # 状态码
content = res.text
# with open('data/proxy_ip_check.html', 'w', encoding='utf-8') as f:
#     f.write(content)
# print(content)
ip_html = bs(content, 'html.parser')
ip = ip_html.find('ul',attrs = {'class':'inner'}).li.a.string
# ip = re.compile('//ip//(.+).html””““””').findall(content)
print(ip)
exit()

# print(ips)
# print(len(ips))

if len(ips) == 0:
    exit()

# 保存为csv文件
ip = pd.DataFrame(ips)
# print(ips)
ip.columns = ['ip']
ip.to_csv('data/ips.csv')
