from django.db import models

# Create your models here.


class Provinces(models.Model):
    name = models.CharField(
        unique=True,
        db_index=True,
        max_length=255,
        verbose_name="省份名")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "省份"
        verbose_name_plural = verbose_name
        db_table = "provinces"


class Cities(models.Model):
    province = models.ForeignKey(Provinces, verbose_name="省份")
    name = models.CharField(
        unique=True,
        db_index=True,
        max_length=255,
        verbose_name="城市")
    city_zh = models.CharField(
        blank=True,
        null=True,
        db_index=True,
        max_length=255,
        verbose_name="城市名")
    url = models.CharField(
        blank=True,
        null=True,
        db_index=True,
        max_length=255,
        verbose_name="url")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name
        db_table = "cities"
