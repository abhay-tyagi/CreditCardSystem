# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-12 10:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20181012_1524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='merchant',
            name='govt_id',
        ),
    ]