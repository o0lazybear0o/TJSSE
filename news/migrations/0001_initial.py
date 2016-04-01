# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-01 07:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0003_remove_customuser_schoolid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filepath', models.FilePathField()),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('date', models.DateField(auto_now=True)),
                ('content', models.CharField(max_length=2000)),
                ('status', models.IntegerField(choices=[(0, '待审核'), (1, '未通过'), (2, '已通过')], verbose_name='审核状态')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.CustomUser')),
            ],
        ),
        migrations.AddField(
            model_name='attachment',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.News'),
        ),
    ]