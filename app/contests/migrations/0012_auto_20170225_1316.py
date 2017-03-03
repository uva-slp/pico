# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-25 18:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0011_auto_20170225_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='contest_admins',
            field=models.ManyToManyField(null=True, related_name='contest_admins', to='users.User'),
        ),
        migrations.AlterField(
            model_name='contesttemplate',
            name='contest_admins',
            field=models.ManyToManyField(null=True, related_name='contesttemplate_admins', to='users.User'),
        ),
    ]
