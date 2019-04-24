from django.db import models

# Create your models here.


class JobInfo(models.Model):
    """
    岗位详情
    """
    job_id = models.CharField(max_length=10, verbose_name="岗位代码")
    job_name = models.CharField(max_length=30, verbose_name="岗位名称")
    salary = models.CharField(max_length=10, null=True, blank=True, verbose_name="薪资")
    recruit_num = models.CharField(max_length=10, null=True, blank=True, verbose_name="招聘人数")
    work_year = models.CharField(max_length=20, null=True, blank=True, verbose_name="经验")
    study = models.CharField(max_length=10, null=True, blank=True, verbose_name="学历")
    work_addr = models.CharField(max_length=255, null=True, blank=True, verbose_name="工作地址")
    jd = models.TextField(max_length=255, null=True, blank=True, verbose_name="岗位描述")
    workfare = models.TextField(max_length=255, null=True, blank=True, verbose_name="福利")

    class Meta:
        verbose_name = "岗位详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.job_name




