from django.db import models
from datetime import datetime
from apps.job.models import Jobs, JobFunctions
from apps.company.models import Companies, Industries
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.


class UserCollectJob(models.Model):
    user = models.ForeignKey(User, verbose_name="用户")
    job = models.ForeignKey(Jobs, verbose_name="岗位")
    create_time = models.DateTimeField(
        default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-create_time']
        verbose_name = "用户收藏岗位"
        verbose_name_plural = verbose_name
        unique_together = ("user", "job")
        db_table = "user_collect_job"


class UserFocusCompany(models.Model):
    user = models.ForeignKey(User, verbose_name="用户")
    company = models.ForeignKey(Companies, verbose_name="公司")
    create_time = models.DateTimeField(
        default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-create_time']
        verbose_name = "用户关注公司"
        verbose_name_plural = verbose_name
        unique_together = ("user", "company")
        db_table = "user_focus_company"


class UserFocusIndustry(models.Model):
    user = models.ForeignKey(User, verbose_name="用户")
    industry = models.ForeignKey(Industries, verbose_name="行业")
    create_time = models.DateTimeField(
        default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-create_time']
        verbose_name = "用户关注行业"
        verbose_name_plural = verbose_name
        unique_together = ("user", "industry")
        db_table = "user_focus_industry"


class UserFocusJobFunction(models.Model):
    user = models.ForeignKey(User, verbose_name="用户")
    jobfunction = models.ForeignKey(JobFunctions, verbose_name="行业")
    create_time = models.DateTimeField(
        default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-create_time']
        verbose_name = "用户关注职能"
        verbose_name_plural = verbose_name
        unique_together = ("user", "jobfunction")
        db_table = "user_focus_jobfunction"
