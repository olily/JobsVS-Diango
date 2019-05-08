from django.db import models
from apps.city.models import Cities
# Create your models here.


class Industries(models.Model):
    name = models.CharField(
        db_index=True,
        blank=True,
        null=True,
        max_length=255,
        verbose_name="行业")
    industry_id = models.CharField(
        unique=True,
        db_index=True,
        default=None,
        max_length=255,
        verbose_name="行业代码")
    category = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        db_index=True,
        max_length=255,
        verbose_name="行业分类")
    url = models.CharField(
        db_index=True,
        null=True,
        blank=True,
        max_length=255,
        verbose_name="url")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "行业"
        verbose_name_plural = verbose_name
        db_table = "industries"


class Companies(models.Model):
    name = models.CharField(
        db_index=True,
        blank=True,
        null=True,
        max_length=255,
        verbose_name="公司名")
    co_id = models.CharField(
        unique=True,
        db_index=True,
        default=None,
        max_length=255,
        verbose_name="公司代码")
    quality = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="性质")
    size = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="规模")
    url = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="url")
    location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="地址")
    img_url = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="头像链接")
    industries = models.ManyToManyField(
        Industries, blank=True, verbose_name="行业")
    city = models.ForeignKey(Cities, blank=True, null=True, verbose_name="城市")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "公司"
        verbose_name_plural = verbose_name
        db_table = "companies"
