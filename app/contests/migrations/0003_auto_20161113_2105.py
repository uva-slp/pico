# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-13 21:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0002_auto_20161105_0444'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='problem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contests.Problem'),
        ),
        migrations.AddField(
            model_name='submission',
            name='state',
            field=models.CharField(choices=[('NEW', 'New'), ('YES', 'Yes'), ('NO', 'No')], default='NEW', max_length=20),
        ),
    ]
