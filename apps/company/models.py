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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "行业"
        verbose_name_plural = verbose_name
        db_table = "industries"


class CompanyQuality(models.Model):
    name = models.CharField(
        db_index=True,
        blank=True,
        null=True,
        max_length=255,
        verbose_name="公司性质")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "公司性质"
        verbose_name_plural = verbose_name
        db_table = "companyquality"


class CompanySize(models.Model):
    name = models.CharField(
        db_index=True,
        blank=True,
        null=True,
        max_length=255,
        verbose_name="公司规模")
    level = models.IntegerField(default=0, verbose_name="等级")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "公司规模"
        verbose_name_plural = verbose_name
        db_table = "companysize"


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
    quality = models.ForeignKey(
        CompanyQuality,
        default=None,
        null=True,
        blank=True,
        verbose_name="公司性质")
    size = models.ForeignKey(
        CompanySize,
        null=True,
        blank=True,
        default=None,
        verbose_name="公司规模")
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
    yesterday_count = models.IntegerField(default=0, verbose_name="昨天新增数量")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "公司"
        verbose_name_plural = verbose_name
        db_table = "companies"
