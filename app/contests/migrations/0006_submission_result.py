# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-14 07:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0005_auto_20161113_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='result',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
