# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-27 14:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='members',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='teams',
        ),
        migrations.DeleteModel(
            name='Organization',
        ),
    ]
