# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-11 11:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20180411_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendence',
            name='end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='attendence',
            name='start_time',
            field=models.DateTimeField(null=True),
        ),
    ]
