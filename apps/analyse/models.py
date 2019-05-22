from django.db import models
from apps.city.models import Cities
from apps.education.models import Education
from apps.company.models import Industries
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
    jobfunction = models.ForeignKey(JobFunctions, default=None, null=True,blank=True,verbose_name="职能")
    education = models.ForeignKey(Education, verbose_name="学历")
    work_year = models.FloatField(default=0, verbose_name="经验")
    salary_low = models.IntegerField(default=0, verbose_name="薪资低")
    salary_high = models.IntegerField(default=0, verbose_name="薪资高")
    count = models.IntegerField(default=0, verbose_name="数量")

    class Meta:
        verbose_name = "岗位分析-散点图"
        verbose_name_plural = verbose_name
        db_table = "jobspoints"


class IndustryPie(models.Model):
    jobfunction = models.ForeignKey(JobFunctions,default=None, null=True,blank=True,verbose_name="职能")
    industry = models.ForeignKey(Industries, verbose_name="行业")
    count = models.IntegerField(default=0, verbose_name="数量")

    class Meta:
        verbose_name = "岗位分析-饼图"
        verbose_name_plural = verbose_name
        db_table = "jobspie"
