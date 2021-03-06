# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-05 02:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0001_initial'),
        ('alerts', '0002_target_contest'),
    ]

    operations = [
        migrations.AddField(
            model_name='target',
            name='invite',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teams.Invite'),
        ),
        migrations.AddField(
            model_name='target',
            name='join_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teams.JoinRequest'),
        ),
        migrations.AddField(
            model_name='target',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teams.Team'),
        ),
    ]
