# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-25 19:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0010_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='contest_length',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
