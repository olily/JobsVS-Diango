# -*- coding: utf-8 -*-
__author__ = 'olily'

# 0330建立文件，爬取51job所有城市分类名称


from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd
import pymysql
import pickle

# 保存城市名称，将拼音作为index，数据为：中文名，url,页数
columns = ['city_name_zh', 'city_url', 'page_num']
index = []
cityAndurl = pd.DataFrame(index=index, columns=columns)

def insertDB(sql_value):
    db.ping(reconnect=True)
    province = city_provinces[row[1][0]]
    sql = 'select id from provinces where name = "%s"' % (province)
    cursor.execute(sql)
    province_id = cursor.fetchone()[0]
    # SQL 插入语句
    sql = 'insert into cities(name,province_id,city_zh,url) values("%s",%d, "%s", "%s")' % (str(sql_value[0]),province_id,str(sql_value[1][0]),str(sql_value[1][1]))
    # print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except BaseException:
        # 如果发生错误则回滚
        db.rollback()


# 解析网页
def html_paser(url, headers):
    response = requests.get(url, headers)
    response.encoding = 'gbk'
    html_text = response.text

    html = bs(html_text, 'html.parser')
    return html


# 得到城市名称，拼音、中文
def get_cityname(url, headers):
    html = html_paser(url, headers)
    cities = html.find_all(
        'a', attrs={
            'href': re.compile('www.51job.com/[a-z]+/$')})

    # i = 0
    # 保存到dataframe
    for h in cities:
        citi_url = h.get('href')
        city_name = citi_url[16:-1]
        index.append(city_name)
        cityAndurl.loc[city_name, 'city_name_zh'] = h.text


# 构造城市岗位列表的url
def construct_url(url_pre,table_name):
    # i=0
    for city in index:
        url = url_pre + city + '/'
        cityAndurl.loc[city, 'city_url'] = url
        # insertDB(table_name,i,city,cityAndurl.loc[city])

        # i+=1
        # print(i)


# 访问url,得到每一城市的页数,web端
def page_num(headers):
    for city in index:
        city_url = cityAndurl.loc[city, 'city_url']
        html = html_paser(city_url, headers)

        # web端
        page_num_str = html.find(attrs={'id':'hidTotalPage'})
        page_num = page_num_str.get('value')
        cityAndurl.loc[city, 'page_num'] = page_num
        print(city,page_num)
        break


# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "jobsvs",)
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

province_city = {
    '北京': ['北京'],
    '天津': ['天津'],
    '上海': ['上海'],
    '重庆': ['重庆'],
    '河南': ['郑州', '洛阳', '焦作', '商丘', '信阳', '周口', '鹤壁', '安阳', '濮阳', '驻马店', '南阳', '开封', '漯河', '许昌', '新乡', '济源', '灵宝', '偃师', '邓州', '登封', '三门峡', '新郑', '禹州', '巩义', '永城', '长葛', '义马', '林州', '项城', '汝州', '荥阳', '平顶山', '卫辉', '辉县', '舞钢', '新密', '孟州', '沁阳', '郏县'],
    '安徽': ['合肥', '亳州', '芜湖', '马鞍山', '池州', '黄山', '滁州', '安庆', '淮南', '淮北', '蚌埠', '宿州', '宣城', '六安', '阜阳', '铜陵', '明光', '天长', '宁国', '界首', '桐城'],
    '福建': ['福州', '厦门', '泉州', '漳州', '南平', '三明', '龙岩', '莆田', '宁德', '建瓯', '武夷山', '长乐', '福清', '晋江', '南安', '福安', '龙海', '邵武', '石狮', '福鼎', '建阳', '漳平', '永安'],
    '甘肃': ['兰州', '白银', '武威', '金昌', '平凉', '张掖', '嘉峪关', '酒泉', '庆阳', '定西', '陇南', '天水', '玉门', '临夏', '合作', '敦煌', '甘南州'],
    '贵州': ['贵阳', '安顺', '遵义', '六盘水', '兴义', '都匀', '凯里', '毕节', '清镇', '铜仁', '赤水', '仁怀', '福泉'],
    '海南': ['海口', '三亚', '万宁', '文昌', '儋州', '琼海', '东方', '五指山'],
    '河北': ['石家庄', '保定', '唐山', '邯郸', '邢台', '沧州', '衡水', '廊坊', '承德', '迁安', '鹿泉', '秦皇岛', '南宫', '任丘', '叶城', '辛集', '涿州', '定州', '晋州', '霸州', '黄骅', '遵化', '张家口', '沙河', '三河', '冀州', '武安', '河间', '深州', '新乐', '泊头', '安国', '双滦区', '高碑店'],
    '黑龙江': ['哈尔滨', '伊春', '牡丹江', '大庆', '鸡西', '鹤岗', '绥化', '齐齐哈尔', '黑河', '富锦', '虎林', '密山', '佳木斯', '双鸭山', '海林', '铁力', '北安', '五大连池', '阿城', '尚志', '五常', '安达', '七台河', '绥芬河', '双城', '海伦', '宁安', '讷河', '穆棱', '同江', '肇东'],
    '湖北': ['武汉', '荆门', '咸宁', '襄阳', '荆州', '黄石', '宜昌', '随州', '鄂州', '孝感', '黄冈', '十堰', '枣阳', '老河口', '恩施', '仙桃', '天门', '钟祥', '潜江', '麻城', '洪湖', '汉川', '赤壁', '松滋', '丹江口', '武穴', '广水', '石首', '大冶', '枝江', '应城', '宜城', '当阳', '安陆', '宜都', '利川'],
    '湖南': ['长沙', '郴州', '益阳', '娄底', '株洲', '衡阳', '湘潭', '岳阳', '常德', '邵阳', '永州', '张家界', '怀化', '浏阳', '醴陵', '湘乡', '耒阳', '沅江', '涟源', '常宁', '吉首', '津', '冷水江', '临湘', '汨罗', '武冈', '韶山', '湘西州'],
    '吉林': ['长春', '吉林', '通化', '白城', '四平', '辽源', '松原', '白山', '集安', '梅河口', '双辽', '延吉', '九台', '桦甸', '榆树', '蛟河', '磐石', '大安', '德惠', '洮南', '龙井', '珲春', '公主岭', '图们', '舒兰', '和龙', '临江', '敦化'],
    '江苏': ['南京', '无锡', '常州', '扬州', '徐州', '苏州', '连云港', '盐城', '淮安', '宿迁', '镇江', '南通', '泰州', '兴化', '东台', '常熟', '江阴', '张家港', '通州', '宜兴', '邳州', '海门', '溧阳', '泰兴', '如皋', '昆山', '启东', '江都', '丹阳', '吴江', '靖江', '扬中', '新沂', '仪征', '太仓', '姜堰', '高邮', '金坛', '句容', '灌南县'],
    '江西': ['南昌', '赣州', '上饶', '宜春', '景德镇', '新余', '九江', '萍乡', '抚州', '鹰潭', '吉安', '丰城', '樟树', '德兴', '瑞金', '井冈山', '高安', '乐平', '南康', '贵溪', '瑞昌', '东乡县', '广丰县', '信州区', '三清山'],
    '辽宁': ['沈阳', '葫芦岛', '大连', '盘锦', '鞍山', '铁岭', '本溪', '丹东', '抚顺', '锦州', '辽阳', '阜新', '调兵山', '朝阳', '海城', '北票', '盖州', '凤城', '庄河', '凌源', '开原', '兴城', '新民', '大石桥', '东港', '北宁', '瓦房店', '普兰店', '凌海', '灯塔', '营口'],
    '青海': ['西宁', '格尔木', '德令哈'],
    '山东': ['济南', '青岛', '威海', '潍坊', '菏泽', '济宁', '莱芜', '东营', '烟台', '淄博', '枣庄', '泰安', '临沂', '日照', '德州', '聊城', '滨州', '乐陵', '兖州', '诸城', '邹城', '滕州', '肥城', '新泰', '胶州', '胶南', '即墨', '龙口', '平度', '莱西'],
    '山西': ['太原', '大同', '阳泉', '长治', '临汾', '晋中', '运城', '忻州', '朔州', '吕梁', '古交', '高平', '永济', '孝义', '侯马', '霍州', '介休', '河津', '汾阳', '原平', '潞城'],
    '陕西': ['西安', '咸阳', '榆林', '宝鸡', '铜川', '渭南', '汉中', '安康', '商洛', '延安', '韩城', '兴平', '华阴'],
    '四川': ['成都', '广安', '德阳', '乐山', '巴中', '内江', '宜宾', '南充', '都江堰', '自贡', '泸州', '广元', '达州', '资阳', '绵阳', '眉山', '遂宁', '雅安', '阆中', '攀枝花', '广汉', '绵竹', '万源', '华蓥', '江油', '西昌', '彭州', '简阳', '崇州', '什邡', '峨眉山', '邛崃', '双流县'],
    '云南': ['昆明', '玉溪', '大理', '曲靖', '昭通', '保山', '丽江', '临沧', '楚雄', '开远', '个旧', '景洪', '安宁', '宣威'],
    '浙江': ['杭州', '宁波', '绍兴', '温州', '台州', '湖州', '嘉兴', '金华', '舟山', '衢州', '丽水', '余姚', '乐清', '临海', '温岭', '永康', '瑞安', '慈溪', '义乌', '上虞', '诸暨', '海宁', '桐乡', '兰溪', '龙泉', '建德', '富德', '富阳', '平湖', '东阳', '嵊州', '奉化', '临安', '江山'],
    '台湾': ['台北', '台南', '台中', '高雄', '桃源'],
    '广东': ['广州', '深圳', '珠海', '汕头', '佛山', '韶关', '湛江', '肇庆', '江门', '茂名', '惠州', '梅州', '汕尾', '河源', '阳江', '清远', '东莞', '中山', '潮州', '揭阳', '云浮'],
    '广西壮族自治区': ['南宁', '贺州', '玉林', '桂林', '柳州', '梧州', '北海', '钦州', '百色', '防城港', '贵港', '河池', '崇左', '来宾', '东兴', '桂平', '北流', '岑溪', '合山', '凭祥', '宜州'],
    '内蒙古自治区': ['呼和浩特', '呼伦贝尔', '赤峰', '扎兰屯', '鄂尔多斯', '乌兰察布', '巴彦淖尔', '二连浩特', '霍林郭勒', '包头', '乌海', '阿尔山', '乌兰浩特', '锡林浩特', '根河', '满洲里', '额尔古纳', '牙克石', '临河', '丰镇', '通辽'],
    '宁夏回族自治区': ['银川', '固原', '石嘴山', '青铜峡', '中卫', '吴忠', '灵武'],
    '西藏藏族自治区': ['拉萨', '日喀则'],
    '新疆维吾尔自治区': ['乌鲁木齐', '石河子', '喀什', '阿勒泰', '阜康', '库尔勒', '阿克苏', '阿拉尔', '哈密', '克拉玛依', '昌吉', '奎屯', '米泉', '和田'],
    '香港': ['香港'],
    '澳门': ['澳门']}

# 每次获取新数据前清空表
# cursor.execute('SET foreign_key_checks = 0')
# cursor.execute('truncate table provinces')
# cursor.execute('truncate table cities')
# cursor.execute('SET foreign_key_checks = 1')
# db.commit()

# 保存省市
# for item in province_city:
#     province_name = item
#     sql = 'insert into provinces( name ) values("%s")' % (province_name)
#     cursor.execute(sql)
#     db.commit()
#     print(sql)

# 反转字典
city_provinces = {}
for province in province_city:
    for city in province_city[province]:
        city_provinces[city] = province

with open('data/province_city.pkl','wb+') as f:
    pickle.dump(province_city, f)

with open('data/city_province.pkl','wb+') as f:
    pickle.dump(city_provinces, f)

exit()


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
}

# 首页
home = 'http://www.51job.com/'
# 城市url前缀
# url_pre = 'https://jobs.51job.com/'

# 移动端前缀
url_pre = 'https://m.51job.com/jobs/'

get_cityname(home, headers)
construct_url(url_pre,'city_info')

for row in cityAndurl.iterrows():
    insertDB(row)

db.close()

