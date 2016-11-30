# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-24 20:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('contests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContestTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('languages', models.CharField(max_length=64)),
                ('contest_length', models.CharField(max_length=8)),
                ('time_penalty', models.CharField(max_length=4)),
                ('autojudge_enabled', models.BooleanField(default=False, max_length=1)),
                ('autojudge_review', models.CharField(blank=True, max_length=128, null=True)),
                ('contest_admins', models.TextField()),
                ('contest_participants', models.TextField()),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.User')),
            ],
        ),
    ]
