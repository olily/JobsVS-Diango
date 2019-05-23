from django.db import models
from apps.city.models import Cities,Provinces
from apps.education.models import Education
from apps.company.models import Industries,CompanyQuality,CompanySize,Companies
from apps.job.models import JobFunctions

# Create your models here.


class JobMap(models.Model):
    jobfunction = models.ForeignKey(JobFunctions, verbose_name="职能")
    city = models.ForeignKey(Cities, verbose_name="城市")
    job_count = models.IntegerField(default=0, verbose_name="岗位数量")
    job_salary_low = models.IntegerField(default=0, verbose_name="薪资低")
    job_salary_high = models.IntegerField(default=0, verbose_name="薪资高")

    class Meta:
        verbose_name = "岗位分析-地图"
        verbose_name_plural = verbose_name
        db_table = "jobsmap"


class JobPoint(models.Model):
    jobfunction = models.ForeignKey(
        JobFunctions,
        default=None,
        null=True,
        blank=True,
        verbose_name="职能")
    # 颜色分类
    education = models.ForeignKey(Education, verbose_name="学历")
    # 正态分布生成随机数作为横坐标
    work_year = models.FloatField(default=0, verbose_name="经验")
    # 作为纵坐标
    salary_avg = models.IntegerField(default=0, verbose_name="平均薪资")

    class Meta:
        verbose_name = "岗位分析-散点图"
        verbose_name_plural = verbose_name
        db_table = "jobspoints"


class Jobbar(models.Model):
    jobfunction = models.ForeignKey(
        JobFunctions,
        default=None,
        null=True,
        blank=True,
        verbose_name="职能")
    company = models.ForeignKey(CompanySize, verbose_name="企业")
    count = models.IntegerField(default=0, verbose_name="数量")
    salary_low = models.IntegerField(default=0, verbose_name="薪资_低")
    salary_high = models.IntegerField(default=0, verbose_name="薪资_高")


    class Meta:
        verbose_name = "岗位分析-柱状图"
        verbose_name_plural = verbose_name
        db_table = "jobsbar"


class IndustryPie(models.Model):
    jobfunction = models.ForeignKey(
        JobFunctions,
        default=None,
        null=True,
        blank=True,
        verbose_name="职能")
    industry = models.ForeignKey(Industries, verbose_name="行业")
    count = models.IntegerField(default=0, verbose_name="数量")

    class Meta:
        verbose_name = "岗位分析-饼图"
        verbose_name_plural = verbose_name
        db_table = "jobspie"


class FareCloud(models.Model):
    jobfunction = models.ForeignKey(
        JobFunctions,
        default=None,
        null=True,
        blank=True,
        verbose_name="职能")
    jobfare = models.CharField(
        default=None,
        max_length=255,
        null=True,
        blank=True,
        verbose_name="福利")
    count = models.IntegerField(default=0, verbose_name="数量")

    class Meta:
        verbose_name = "岗位分析-福利词云"
        verbose_name_plural = verbose_name
        db_table = "jobsfarecloud"


class ResponseCloud(models.Model):
    jobfunction = models.ForeignKey(
        JobFunctions,
        default=None,
        null=True,
        blank=True,
        verbose_name="职能")
    response = models.CharField(
        default=None,
        max_length=255,
        null=True,
        blank=True,
        verbose_name="职责")
    count = models.IntegerField(default=0, verbose_name="数量")

    class Meta:
        verbose_name = "岗位分析-职责词云"
        verbose_name_plural = verbose_name
        db_table = "responsecloud"


class RequestCloud(models.Model):
    jobfunction = models.ForeignKey(
        JobFunctions,
        default=None,
        null=True,
        blank=True,
        verbose_name="职能")
    request = models.CharField(
        default=None,
        max_length=255,
        null=True,
        blank=True,
        verbose_name="要求")
    count = models.IntegerField(default=0, verbose_name="数量")

    class Meta:
        verbose_name = "岗位分析-要求词云"
        verbose_name_plural = verbose_name
        db_table = "requestcloud"


class CompanyMap(models.Model):
    city = models.ForeignKey(Cities, verbose_name="城市")
    count = models.IntegerField(default=0, verbose_name="企业数量")

    class Meta:
        verbose_name = "企业分析-地图"
        verbose_name_plural = verbose_name
        db_table = "companysmap"


class CompanyHot(models.Model):
    industries = models.ForeignKey(Industries, verbose_name="行业")
    quality = models.ForeignKey(CompanyQuality, verbose_name="性质")
    count = models.IntegerField(default=0, verbose_name="企业数量")

    class Meta:
        verbose_name = "企业分析-热力图"
        verbose_name_plural = verbose_name
        db_table = "companyshot"


class CompanyParallel(models.Model):
    p = models.ForeignKey(Provinces, verbose_name="省份", default=None)
    c = models.ForeignKey(Cities, verbose_name="城市", default=None)
    s = models.ForeignKey(CompanySize, verbose_name="规模", default=None)
    q = models.ForeignKey(CompanyQuality, verbose_name="性质", default=None)
    i = models.ForeignKey(Industries, verbose_name="行业", default=None)


    class Meta:
        verbose_name = "企业分析-平行坐标"
        verbose_name_plural = verbose_name
        db_table = "companysparallel"


class CompanyRange(models.Model):
    company = models.ForeignKey(Companies,verbose_name="企业")
    count = models.IntegerField(default=0, verbose_name="数量")
    salary_avg = models.IntegerField(default=0, verbose_name="平均薪资")


    class Meta:
        verbose_name = "总体分析-企业分析"
        verbose_name_plural = verbose_name
        db_table = "companysrange"


class IndustrySunburst(models.Model):
    Industries = models.ForeignKey(Industries, verbose_name="行业")
    count = models.IntegerField(default=0, verbose_name="数量")
    salary_avg = models.IntegerField(default=0, verbose_name="平均薪资")


    class Meta:
        verbose_name = "总体分析-行业分析"
        verbose_name_plural = verbose_name
        db_table = "industrysunburst"


class CitySunburst(models.Model):
    province = models.ForeignKey(Provinces, verbose_name="省份")
    city = models.ForeignKey(Cities, verbose_name="城市")
    count = models.IntegerField(default=0, verbose_name="数量")
    salary_avg= models.IntegerField(default=0, verbose_name="平均薪资")


    class Meta:
        verbose_name = "总体分析-城市分析"
        verbose_name_plural = verbose_name
        db_table = "citysunburst"


class FunSunburst(models.Model):
    functions = models.ForeignKey(JobFunctions, verbose_name="职能")
    count = models.IntegerField(default=0, verbose_name="数量")
    salary_avg = models.IntegerField(default=0, verbose_name="平均薪资")


    class Meta:
        verbose_name = "总体分析-职能分析"
        verbose_name_plural = verbose_name
        db_table = "funsunburst"