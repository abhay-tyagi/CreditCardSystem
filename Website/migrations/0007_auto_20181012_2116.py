# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-12 15:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0006_cleareddate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cleareddate',
            name='merchant',
        ),
        migrations.AddField(
            model_name='fundtransfer',
            name='ime',
            field=models.TimeField(default=datetime.datetime(2018, 10, 12, 15, 46, 48, 809909, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='transaction',
            name='time',
            field=models.TimeField(default=datetime.datetime(2018, 10, 12, 15, 46, 48, 809350, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='fundtransfer',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.DeleteModel(
            name='ClearedDate',
        ),
    ]
