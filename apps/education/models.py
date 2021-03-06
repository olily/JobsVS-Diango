from django.db import models

# Create your models here.


class Education(models.Model):
    # 初始无学历，依次上升，判断的时候level大于等于某个数字
    level = models.IntegerField(default=0, verbose_name="等级")
    name = models.CharField(
        unique=True,
        db_index=True,
        max_length=255,
        verbose_name="学历")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "学历"
        verbose_name_plural = verbose_name
        db_table = "education"
