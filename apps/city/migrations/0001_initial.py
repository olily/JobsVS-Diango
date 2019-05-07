# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-07 12:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True, verbose_name='城市名')),
            ],
            options={
                'verbose_name': '城市',
                'verbose_name_plural': '城市',
                'db_table': 'cities',
            },
        ),
        migrations.CreateModel(
            name='Provinces',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True, verbose_name='省份名')),
            ],
            options={
                'verbose_name': '省份',
                'verbose_name_plural': '省份',
                'db_table': 'provinces',
            },
        ),
        migrations.AddField(
            model_name='cities',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city.Provinces', verbose_name='省份'),
        ),
    ]
