from datetime import datetime
from django.db import models
from jobs import models as job
from cities import models as city
from companies import models as company

# Create your models here.


class JobRealation(models.Model):
    """
    岗位
    """
    job_id = models.ForeignKey(job.JobInfo)
    city = models.ForeignKey(city.CityInfo)
    put_time = models.DateField(verbose_name="添加时间")
    company = models.ForeignKey(company.CompanyProfile)
    job_url = models.CharField(max_length=255, null=True, blank=True, verbose_name="岗位链接")