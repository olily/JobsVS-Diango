from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.education.models import Education

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
    education = models.ForeignKey(Education, null=True, verbose_name="学历")
    sex = models.IntegerField(default=0, verbose_name="性别")  # 0保密 1男 2女

    class Meta:
        verbose_name = "个人信息"
        verbose_name_plural = verbose_name
        db_table = "userprofile"
