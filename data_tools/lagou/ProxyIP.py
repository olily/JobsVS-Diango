# -*- coding: utf-8 -*-
__author__ = 'olily'

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import ssl
import random
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ssl._create_default_https_context = ssl._create_unverified_context


def scripy_ips(header):
    ips = pd.DataFrame(columns=['ip', 'type'])
    index = 1
    # 翻页查询爬取数据
    for i in range(1, 6):
        url = 'https://www.xicidaili.com/wn/' + str(i)
        print(url)
        ip_response = requests.get(url=url, headers=header,verify=False)
        ip_response.encoding = 'utf-8'
        ip_html_text = ip_response.text
        ip_html = bs(ip_html_text, 'html.parser')
        # print(ip_html)

        ip_list = ip_html.find_all(attrs={'class': 'odd'})
        # 获取数据
        for ip_td in ip_list:
            ip_content = ip_td.find_all('td')
            # print(ip_content)
            ip = ip_content[1].string+':'+ip_content[2].string
            # port = ip_content[2].string
            # type = ip_content[5].string
            proxies = {'https': ip}
            # print(proxies)
            # proxies = {'https': '110.184.126.130'}
            # 验证ip是否可用
            try:
                ip_test = requests.get(
                    url='https://www.baidu.com',
                    headers=header,
                    proxies=proxies,
                    verify=False,
                    timeout=10)
                # print(ip_test)
            except:
                continue
            else:
                print(ip)
                type = ip_content[5].string
                ips.loc[index] = [ip, type]
                index += 1

    ips.to_csv('data/ips.csv', encoding='utf-8')


# 检查代理是否设置成功
def check_proxy(header):
    ips_set = pd.read_csv("data/ips.csv")
    # proxy = {'https': '180.164.24.165:53281'}
    proxy = {'https': random.choice(ips_set['ip'])}
    print(proxy)
    res = requests.get(
        url="https://www.ipip.net/",
        proxies=proxy,
        headers=header,
        )
    # status = res.status_code  # 状态码
    content = res.text
    # with open('data/proxy_ip_check.html', 'w', encoding='utf-8') as f:
    #     f.write(content)
    # with open('data/proxy_ip_check.html', 'w', encoding='utf-8') as f:
    #     f.write(content)
    ip_html = bs(content, 'html.parser')
    ip = ip_html.find('ul', attrs={'class': 'inner'}).li.a.string
    print(ip)

# 反爬虫机制
header = {
    # 'Upgrade-Insecure-Requests': '1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
    # 'Referer': 'https://www.kuaidaili.com/free/inha/'
}
scripy_ips(header)
check_proxy(header)






