from django.db import models
from apps.city.models import Cities
# Create your models here.


class Industries(models.Model):
    name = models.CharField(
        unique=True,
        db_index=True,
        max_length=255,
        verbose_name="行业")

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
