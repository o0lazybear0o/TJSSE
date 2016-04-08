# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-08 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20160408_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='credit',
            name='credit_second_type',
            field=models.IntegerField(choices=[(11, '校级'), (12, '省级'), (13, '国家级'), (14, '国际级'), (15, '其他'), (21, '权威报纸'), (22, '核心期刊'), (23, 'SCI/EI检索'), (0, '无')], default=0, verbose_name='认定等级2'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='credit',
            name='credit_third_type',
            field=models.IntegerField(choices=[(11, '一等奖'), (12, '二等奖'), (13, '三等奖'), (21, '第一作者'), (22, '第二作者'), (23, '第三作者'), (0, '无')], default=0, verbose_name='认定等级3'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='credit',
            name='grade',
            field=models.IntegerField(choices=[(5, '优'), (4, '良'), (3, '中'), (2, '及格'), (0, '暂无')], default=0, verbose_name='学分等级'),
        ),
        migrations.AddField(
            model_name='credit',
            name='status',
            field=models.IntegerField(choices=[(0, '待审核'), (1, '未通过'), (2, '已通过')], default=0, verbose_name='审核状态'),
        ),
    ]
