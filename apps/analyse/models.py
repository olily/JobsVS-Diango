from django.db import models
from city.models import Cities
from education.models import Education
from company.models import Industries

# Create your models here.


class JobMap(models.Model):
    city = models.ForeignKey(Cities, verbose_name="城市")
    job_count = models.IntegerField(default=0, verbose_name="岗位数量")
    job_salary_low = models.IntegerField(default=0, verbose_name="薪资低")
    job_salary_high = models.IntegerField(default=0, verbose_name="薪资高")
    job_salary_avg = models.IntegerField(default=0, verbose_name="平均薪资")


class JobPoint(models.Model):
    education = models.Model(Education, verbose_name="学历")
    work_year = models.FloatField(default=0, verbose_name="经验")
    salary_low = models.IntegerField(default=0, verbose_name="薪资低")
    salary_high = models.IntegerField(default=0, verbose_name="薪资高")
    count = models.IntegerField(default=0, verbose_name="数量")


class IndustryPie(models.Model):
    industry = models.ForeignKey(Industries, verbose_name="行业")
    count = models.IntegerField(default=0, verbose_name="数量")
