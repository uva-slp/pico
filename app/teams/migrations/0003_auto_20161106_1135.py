# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-06 11:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_auto_20161104_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=32),
        ),
    ]
