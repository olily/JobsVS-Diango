import requests,re
session = requests.Session()

#步骤一、首先登陆login.html，获取cookie
r1 = session.get('https://passport.lagou.com/login/login.html', headers={'Host': "passport.lagou.com",'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'})

X_Anti_Forge_Token = re.findall(r"window.X_Anti_Forge_Token = '(.*)';",r1.text)[0]
X_Anti_Forge_Code = re.findall(r"window.X_Anti_Forge_Code = '(.*)';",r1.text)[0]

#步骤二、用户登陆，携带上一次的cookie，后台对cookie中的 jsessionid 进行授权
r3 = session.post(
    url='https://passport.lagou.com/login/login.json',
    data={
        'isValidate': True,
        # 'username': '424662508@qq.com',
        # 'password': '4c4c83b3adf174b9c22af4a179dddb63',
        'username':'18611453110',
        'password':'bff642652c0c9e766b40e1a6f3305274',
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

#步骤三：进行授权
r4 = session.get('https://passport.lagou.com/grantServiceTicket/grant.html',
                  allow_redirects=False,
                  headers={'Host': "passport.lagou.com",'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'})

# print(r4.headers)
location=r4.headers['Location']
# print(location)

#步骤四：请求重定向的地址，拿到最终的登录session
r5= session.get(location,
                  allow_redirects=True,
                  headers={
                      'Host': "www.lagou.com",
                      'Referer':'https://passport.lagou.com/login/login.html?',
                      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'})

# print(r5.headers)

#===============以上是登录环节

#爬取职位信息

#步骤一：分析
#搜索职位的url样例：https://www.lagou.com/jobs/list_python%E5%BC%80%E5%8F%91?labelWords=&fromSearch=true&suginput=
from urllib.parse import urlencode
keyword='python开发'
url_encode=urlencode({'k':keyword},encoding='utf-8') #k=python%E5%BC%80%E5%8F%91
url='https://www.lagou.com/jobs/list_%s?labelWords=&fromSearch=true&suginput=' %url_encode.split('=')[1] #根据用户的keyword拼接出搜索职位的url
print(url)

#拿到职位信息的主页面
r7=session.get(url,
               headers={
                   'Host': "www.lagou.com",
                   'Referer': 'https://passport.lagou.com/login/login.html?',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
               })
#发现主页面中并没有我们想要搜索的职位信息，那么肯定是通过后期js渲染出的结果，一查，果然如此
r7.text
#搜索职位：请求职位的url后只获取了一些静态内容，关于职位的信息是向https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0发送请求拿到json

#步骤二：验证分析的结果
#爬取职位信息，发post请求，拿到json数据：'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0'
r8=session.post('https://www.lagou.com/jobs/positionAjax.json',
               params={
                   'needAddtionalResult':False,
                   'isSchoolJob':'0',

               },
               headers={
                   'Host': "www.lagou.com",
                   'Origin':'https://www.lagou.com',
                   'Referer': url,
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                   'X-Anit-Forge-Code':'0',
                   'X-Anit-Forge-Token': '',
                   'X-Requested-With': 'XMLHttpRequest',
'Accept':'application/json, text/javascript, */*; q=0.01'
               },
               data={
                    'first':True,
                    'pn':'1',
                    'kd':'python开发'
               }
               )

print(r8.json()) #pageNo:1 代表第一页，pageSize:15代表本页有15条职位记录，我们需要做的是获取总共有多少页就可以了

#步骤三（最终实现）：实现根据传入参数，筛选职位信息
from urllib.parse import urlencode
keyword='python开发'
url_encode=urlencode({'k':keyword},encoding='utf-8') #k=python%E5%BC%80%E5%8F%91
url='https://www.lagou.com/jobs/list_%s?labelWords=&fromSearch=true&suginput=' %url_encode.split('=')[1] #根据用户的keyword拼接出搜索职位的url

def search_position(
                    keyword,
                    pn=1,
                    city='北京',
                    district=None,
                    bizArea=None,
                    isSchoolJob=None,
                    xl=None,
                    jd=None,
                    hy=None,
                    yx=None,
                    needAddtionalResult=False,
                    px='detault'):
    params = {
                 'city': city,  # 工作地点,如北京
                 'district': district,  # 行政区，如朝阳区
                 'bizArea': bizArea,  # 商区，如望京
                 'isSchoolJob': isSchoolJob,  # 工作性质，如应届
                 'xl': xl,  # 学历要求，如大专
                 'jd': jd,  # 融资阶段，如天使轮,A轮
                 'hy': hy,  # 行业领域，如移动互联网
                 'yx': yx,  # 工资范围，如10-15k
                 'needAddtionalResult': needAddtionalResult,
                 'px': 'detault'
             },
    r8 = session.post('https://www.lagou.com/jobs/positionAjax.json',
                      params={
                          'city': city, #工作地点,如北京
                          'district': district,#行政区，如朝阳区
                          'bizArea': bizArea, #商区，如望京
                          'isSchoolJob': isSchoolJob, #工作性质，如应届
                          'xl': xl, #学历要求，如大专
                          'jd': jd,#融资阶段，如天使轮,A轮
                          'hy': hy, #行业领域，如移动互联网
                          'yx': yx, #工资范围，如10-15k
                          'needAddtionalResult': needAddtionalResult,
                          'px':'detault'
                      },
                      headers={
                          'Host': "www.lagou.com",
                          'Origin': 'https://www.lagou.com',
                          'Referer': url,
                          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                          'X-Anit-Forge-Code': '0',
                          'X-Anit-Forge-Token': '',
                          'X-Requested-With': 'XMLHttpRequest',
                          'Accept': 'application/json, text/javascript, */*; q=0.01'
                      },
                      data={
                          'first': True,
                          'pn': pn,
                          'kd': keyword,
                      }
                      )
    print(r8.status_code)
    print(r8.json())
    return r8.json()


#求一份北京朝阳区10-15k的python开发工作
keyword='python开发'
yx='10k-15k'
city='北京'
district='朝阳区'
isSchoolJob='0' #应届或实习

response=search_position(keyword=keyword,yx=yx,city=city,district=district,isSchoolJob=isSchoolJob)
results=response['content']['positionResult']['result']

#打印公司的详细信息
def get_company_info(results):
    for res in results:
        info = '''
        公司全称 : %s
        地址 : %s,%s
        发布时间 : %s
        职位名 : %s
        职位类型 : %s,%s
        工作模式 : %s
        薪资 : %s
        福利 : %s
        要求工作经验 : %s
        公司规模 : %s
        详细链接 : https://www.lagou.com/jobs/%s.html
        ''' % (
            res['companyFullName'],
            res['city'],
            res['district'],
            res['createTime'],
            res['positionName'],
            res['firstType'],
            res['secondType'],
            res['jobNature'],
            res['salary'],
            res['positionAdvantage'],
            res['workYear'],
            res['companySize'],
            res['positionId']
        )
        print(info)
        # 经分析，公司的详细链接都是：https://www.lagou.com/jobs/2653020.html ，其中那个编号就是职位id
        #print('公司全称[%s],简称[%s]' %(res['companyFullName'],res['companyShortName']))
get_company_info(results)