from django.db import models

# Create your models here.


class CityInfo(models.Model):
    """
    岗位详情
    """
    city = models.CharField(max_length=30, verbose_name="城市")
    city_name = models.CharField(max_length=30, verbose_name="城市名称")
    city_url = models.CharField(max_length=10, null=True, blank=True, verbose_name="城市链接")

    class Meta:
        verbose_name = "城市信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.city_name




