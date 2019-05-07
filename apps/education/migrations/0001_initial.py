# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-07 12:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('education', models.CharField(choices=[('primaryschool', '小学'), ('juniorschool', '初中'), ('seniorschool', '高中'), ('technicalsecondaryschool', '中专'), ('juniorcollege', '大专'), ('regularcollege', '本科'), ('postgraduate', '研究生'), ('doctor', '博士')], max_length=32)),
                ('level', models.IntegerField(default=0, verbose_name='等级')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True, verbose_name='学历')),
            ],
            options={
                'verbose_name': '学历',
                'verbose_name_plural': '学历',
                'db_table': 'education',
            },
        ),
    ]
