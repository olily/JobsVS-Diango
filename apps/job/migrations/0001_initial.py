# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-08 12:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('education', '0001_initial'),
        ('company', '0001_initial'),
        ('city', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobFunctions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='职能')),
                ('fun_id', models.CharField(db_index=True, default=None, max_length=255, verbose_name='职能代码')),
                ('url', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='url')),
                ('category', models.ForeignKey(blank=True, max_length=255, null=True, on_delete=django.db.models.deletion.CASCADE, to='job.JobFunctions', verbose_name='职能分类')),
            ],
            options={
                'verbose_name': '职能',
                'verbose_name_plural': '职能',
                'db_table': 'jobfunction',
            },
        ),
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='岗位名')),
                ('job_id', models.IntegerField(unique=True, verbose_name='工作id')),
                ('head_count', models.IntegerField(default=0, verbose_name='招聘人数')),
                ('put_time', models.DateField(blank=True, null=True, verbose_name='发布时间')),
                ('salary_low', models.IntegerField(blank=True, null=True, verbose_name='工资_低')),
                ('salary_high', models.IntegerField(blank=True, null=True, verbose_name='工资_高')),
                ('work_year', models.CharField(blank=True, max_length=255, null=True, verbose_name='工作经验')),
                ('work_addr', models.CharField(max_length=255, verbose_name='工作地点')),
                ('jobReqAndRes', models.CharField(max_length=255, verbose_name='岗位要求和职责')),
                ('jobfare', models.CharField(max_length=255, verbose_name='工作福利')),
                ('isUndercarriage', models.BooleanField(default=False, verbose_name='是否关闭')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city.Cities', verbose_name='城市')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.Companies', verbose_name='公司')),
                ('education', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.Education', verbose_name='学历')),
                ('jobfunction', models.ManyToManyField(default=None, to='job.JobFunctions', verbose_name='职能')),
            ],
            options={
                'verbose_name': '岗位',
                'verbose_name_plural': '岗位',
                'db_table': 'jobs',
            },
        ),
    ]
