# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-02 18:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0003_auto_20170102_1310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alert',
            name='subject',
        ),
    ]
