from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.education.models import Education
from apps.city.models import Cities
from apps.company.models import Industries, CompanySize
from apps.job.models import JobFunctions
# Create your models here.


class User(AbstractUser):
    email = models.EmailField(
        max_length=100,
        unique=True,
        blank=False,
        verbose_name="邮箱")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class WorkYear(models.Model):
    name = models.CharField(
        db_index=True,
        max_length=255,
        verbose_name="工作年限")
    low = models.IntegerField(default=0, verbose_name="下限")
    high = models.IntegerField(default=0, verbose_name="上限")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "工作年限"
        verbose_name_plural = verbose_name
        db_table = "workyear"


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        verbose_name="用户")
    avatar = models.ImageField(
        blank=True,
        upload_to='avatars/',
        default='avatars/default.jpg', verbose_name="头像")
    work_year = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name="工作经验")
    school = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="学校")
    education = models.ForeignKey(Education, null=True, blank=True,verbose_name="学历")
    sex = models.IntegerField(default=0, verbose_name="性别")  # 0保密 1男 2女
    birthday = models.DateField(null=True, blank=True, verbose_name="生日")
    city = models.ForeignKey(
        Cities,
        null=True,
        blank=True,
        default=None,
        verbose_name="现居城市")

    class Meta:
        verbose_name = "个人信息"
        verbose_name_plural = verbose_name
        db_table = "userprofile"


class UserWantJob(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        verbose_name="用户")
    want_education = models.ForeignKey(
        Education, default=None, null=True, blank=True, verbose_name="期望学历")
    want_workyear = models.ForeignKey(
        WorkYear, default=None, null=True, blank=True, verbose_name="工作年限")
    want_city = models.ForeignKey(
        Cities,
        default=None,
        null=True,
        blank=True,
        verbose_name="期望城市")
    want_industry = models.ForeignKey(
        Industries, default=None, null=True, blank=True, verbose_name="期望行业")
    want_jobfunction = models.ForeignKey(
        JobFunctions, default=None, null=True, blank=True, verbose_name="期望职能")
    want_salary_low = models.IntegerField(default=0, verbose_name="期望薪资_低")
    want_salary_high = models.IntegerField(default=0, verbose_name="期望薪资_高")
    want_companysize = models.ForeignKey(
        CompanySize, null=True, blank=True, verbose_name="期望公司规模")

    class Meta:
        verbose_name = "求职意向"
        verbose_name_plural = verbose_name
        db_table = "userwantjob"
