# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-24 04:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fund',
            name='value',
            field=models.IntegerField(default=0),
        ),
    ]
