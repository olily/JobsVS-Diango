# -*- coding: utf-8 -*-
__author__ = 'olily'

#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time


import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "jobsvs", charset='utf8')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

time_start = time.time()

# 使用execute方法执行SQL语句
cursor.execute("SELECT id,co_id FROM companies")

# 使用 fetchone() 方法获取一条数据
data = cursor.fetchall()
companyDict = {}
for company in data:
    companyDict[company[1]] = company[0]
time_end = time.time()
print('totally cost', time_end - time_start)
cursor.close()
db.close()

db_urllist = pymysql.connect("localhost", "root", "123456", "urllist", charset='utf8')
cursor_urllist = db_urllist.cursor()

time_start = time.time()
print(companyDict['co2684966'])
time_end = time.time()
print('totally cost', time_end - time_start)

cursor_urllist.execute("SELECT * FROM jobs_get_copy9 limit 0,1000000")
data = cursor_urllist.fetchall()
print(len(data))
time_start = time.time()
for job in data:
    print(job)
    #INSERT INTO `urllist`.`jobs_get_copy9`(`id`, `name`, `code`, `company_code`, `company_id`, `salary_low`, `salary_high`, `salary_type`, `city_id`, `put_time`, `url`, `work_year`, `education`, `job_fun`, `jobfare`, `jd`, `status_update`, `status_jd`, `education_id`) VALUES (2853001, '收银员', '99984913', 'co3672467', NULL, 2000, 3000, '2', 111, '05-14', 'https://jobs.51job.com/jinan/99984913.html', '2年经验', '大专', '收银员_收银主管', '五险一金_员工旅游_餐饮补贴_绩效奖金_定期体检_双休', '\n岗位职责描述： 1、在收银主管的直接领导下，做好收费结算工作； 2、领取、使用、管理和归还收银备用金； 3、制作、打印、核对收银相关凭证； 4、汇总收据、发票，编制相关报表； 5、根据收款凭证登记现金和银行日记账，并将凭证送至会计； 6、妥善保管收银设备。  任职资格： 1、高中以上学历，会计或财务专业优先； 2、有会计证、有出纳工作经验者优先； 3、熟练操作计算机，形象气质佳、工作严谨； 4、具有良好的敬业精神，较强的学习能力和沟通能力。  ', 0, 1, 4);

    sql = "INSERT INTO `urllist`.`jobs_get_copy9_copy1`(`id`, `name`, `code`, `company_code`, `company_id`, `salary_low`, `salary_high`, `salary_type`, `city_id`, `put_time`, `url`, `work_year`, `education`, `job_fun`, `jobfare`, `jd`, `status_update`, `status_jd`, `education_id`) VALUES (%d, '%s', '%s', '%s', %d, %d, %d, '%s', %d, '05-14', '%s', '%s', '%s', '%s', '%s', '%s', %d, %d, %d);" % (companyDict[data['co_id']])
    exit()
time_end = time.time()
print('totally cost', time_end - time_start)
