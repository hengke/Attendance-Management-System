# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-29 08:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendence',
            name='day',
            field=models.DateField(default=datetime.datetime(2018, 3, 29, 16, 6, 22, 366020)),
        ),
    ]