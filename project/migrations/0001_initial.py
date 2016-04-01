# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-01 08:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0003_remove_customuser_schoolid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=20)),
                ('type', models.IntegerField(choices=[(0, '开题文档'), (1, '中期文档'), (2, '结题文档'), (3, '其他')], verbose_name='文档类型')),
                ('status', models.IntegerField(choices=[(0, '待审核'), (1, '未通过'), (2, '已通过')], verbose_name='审核状态')),
                ('date', models.DateField(default=datetime.date.today)),
                ('filepath', models.FilePathField()),
                ('note', models.CharField(blank=True, max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fund_type', models.CharField(max_length=60)),
                ('date', models.DateField(default=datetime.date.today)),
                ('note', models.CharField(blank=True, max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=100)),
                ('status', models.IntegerField(choices=[(0, '未申请立项'), (1, '申请立项'), (2, '立项通过'), (3, '申请中期'), (4, '中期通过'), (5, '申请结题'), (6, '已结题')], default=0)),
                ('endtime', models.DateField(null=True)),
                ('note', models.CharField(blank=True, max_length=300)),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Project_Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_superuser', models.BooleanField(default=False)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Student')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typename', models.CharField(max_length=20)),
                ('type', models.IntegerField(choices=[(0, '国创'), (1, '市创'), (2, 'SITP'), (3, '院创'), (4, '其他')], verbose_name='认定类型')),
                ('isopening', models.BooleanField(default=True, verbose_name='是否开放中')),
                ('starttime', models.DateField(default=datetime.date.today)),
                ('endtime', models.DateField()),
                ('note', models.CharField(blank=True, max_length=300)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='project_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.ProjectType'),
        ),
        migrations.AddField(
            model_name='fund',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project'),
        ),
        migrations.AddField(
            model_name='document',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project'),
        ),
    ]