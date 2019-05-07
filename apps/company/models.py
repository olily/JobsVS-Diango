from django.db import models
from apps.city.models import Cities
# Create your models here.


class Industries(models.Model):
    name = models.CharField(
        db_index=True,
        max_length=255,
        verbose_name="行业")
    industry_id = models.CharField(
        unique=True,
        default = None,
        db_index=True,
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
        unique=True,
        db_index=True,
        max_length=255,
        verbose_name="公司名")
    city = models.ForeignKey(Cities, verbose_name="城市")
    location = models.CharField(max_length=255, verbose_name="地址")
    industries = models.ManyToManyField(Industries, verbose_name="行业")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "公司"
        verbose_name_plural = verbose_name
        db_table = "companies"
