from django.db import models

# Create your models here.


class CompanyProfile(models.Model):
    """
    岗位详情
    """
    company_name = models.CharField(max_length=30, verbose_name="公司名称")
    campany_addr = models.CharField(max_length=10, null=True, blank=True, verbose_name="公司地址")
    campany_url = models.CharField(max_length=10, null=True, blank=True, verbose_name="公司链接")
    campany_num = models.CharField(max_length=10, null=True, blank=True, verbose_name="规模")
    industry = models.CharField(max_length=20, null=True, blank=True, verbose_name="行业")

    class Meta:
        verbose_name = "公司信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.company_name




