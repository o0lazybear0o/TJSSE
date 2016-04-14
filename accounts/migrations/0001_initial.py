# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-14 10:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_credit_date', models.DateField(auto_now=True)),
                ('get_project_date', models.DateField(null=True)),
                ('name', models.CharField(max_length=300, verbose_name='名称')),
                ('credit_type', models.IntegerField(choices=[(1, '竞赛获奖'), (2, '学术论文'), (3, '国家发明专利'), (4, '大学生创新项目')], default='1', verbose_name='认定类型')),
                ('credit_second_type', models.IntegerField(choices=[(11, '校级'), (12, '省级'), (13, '国家级'), (14, '国际级'), (15, '其他'), (21, '权威报纸'), (22, '核心期刊'), (23, 'SCI/EI检索'), (0, '无')], default='11', verbose_name='认定等级2')),
                ('credit_third_type', models.IntegerField(choices=[(11, '一等奖'), (12, '二等奖'), (13, '三等奖'), (21, '第一作者'), (22, '第二作者'), (23, '第三作者'), (0, '无')], default='11', verbose_name='认定等级3')),
                ('status', models.IntegerField(choices=[(0, '待审核'), (1, '未通过'), (2, '已通过')], default=0, verbose_name='审核状态')),
                ('grade', models.IntegerField(choices=[(5, '优'), (4, '良'), (3, '中'), (2, '及格'), (0, '暂无')], default=0, verbose_name='学分等级')),
                ('value', models.IntegerField(default=0, verbose_name='认定学分')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['create_credit_date'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=10)),
                ('grade', models.IntegerField(null=True)),
                ('major', models.IntegerField(choices=[(0, '暂无'), (1, '软件技术与管理'), (2, '网络与主机软件'), (3, '嵌入式软件与系统'), (4, '数字媒体'), (5, '其他')], default=0)),
                ('phone', models.CharField(blank=True, max_length=11)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
