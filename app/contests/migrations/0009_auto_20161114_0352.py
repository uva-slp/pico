# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-14 03:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0008_auto_20161114_0348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='autojudge_enabled',
            field=models.BooleanField(default=b'0', max_length=1),
        ),
    ]
