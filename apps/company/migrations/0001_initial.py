# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-28 10:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('city', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Companies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True, verbose_name='公司名')),
                ('location', models.CharField(max_length=255, verbose_name='地址')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city.Cities', verbose_name='城市')),
            ],
            options={
                'verbose_name': '公司',
                'verbose_name_plural': '公司',
                'db_table': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Industries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True, verbose_name='行业')),
            ],
            options={
                'verbose_name': '行业',
                'verbose_name_plural': '行业',
                'db_table': 'industries',
            },
        ),
        migrations.AddField(
            model_name='companies',
            name='industries',
            field=models.ManyToManyField(to='company.Industries', verbose_name='行业'),
        ),
    ]
