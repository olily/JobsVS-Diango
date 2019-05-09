from django.db import models
from apps.education.models import Education
from apps.city.models import Cities
from apps.company.models import Companies

# Create your models here.


class JobFunctions(models.Model):
    name = models.CharField(
        db_index=True,
        max_length=255,
        verbose_name="职能")
    fun_id = models.CharField(
        default=None,
        db_index=True,
        max_length=255,
        verbose_name="职能代码")
    category = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        db_index=True,
        max_length=255,
        verbose_name="职能分类")
    url = models.CharField(
        db_index=True,
        null=True,
        blank=True,
        max_length=255,
        verbose_name="url")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "职能"
        verbose_name_plural = verbose_name
        db_table = "jobfunction"


class Jobs(models.Model):
    name = models.CharField(
        db_index=True,
        max_length=255,
        verbose_name="岗位名")
    city = models.ForeignKey(Cities, verbose_name="城市")  # 公司城市有可能和岗位城市不一样
    company = models.ForeignKey(
        Companies,
        verbose_name="公司",
        blank=True,
        null=True)
    jobfunction = models.ManyToManyField(
        JobFunctions, verbose_name="职能", blank=True, null=True, default=None)
    job_id = models.IntegerField(unique=True, verbose_name="工作id")  # 用来构造url
    head_count = models.IntegerField(default=0, verbose_name="招聘人数")
    put_time = models.DateField(verbose_name="发布时间", blank=True, null=True, default=None)
    salary_low = models.IntegerField(
        verbose_name="工资_低", blank=True, null=True)
    salary_high = models.IntegerField(
        verbose_name="工资_高", blank=True, null=True)
    work_year = models.IntegerField(
        verbose_name="工作经验",
        blank=True,
        null=True,
        default=0)
    education = models.ForeignKey(Education, blank=True,
                                  null=True, verbose_name="学历")
    work_addr = models.CharField(max_length=255, verbose_name="工作地点")
    jobReqAndRes = models.CharField(max_length=255, verbose_name="岗位要求和职责")
    jobfare = models.CharField(max_length=255, verbose_name="工作福利")
    isUndercarriage = models.BooleanField(default=False, verbose_name="是否关闭")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "岗位"
        verbose_name_plural = verbose_name
        db_table = "jobs"
