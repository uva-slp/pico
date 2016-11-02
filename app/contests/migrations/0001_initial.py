# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-02 18:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('creator', models.CharField(max_length=32)),
                ('languages', models.CharField(max_length=100)),
                ('contest_length', models.CharField(max_length=10)),
                ('autojudge', models.CharField(max_length=10)),
                ('contest_admins', models.CharField(max_length=100, null=True)),
                ('contest_participants', models.CharField(max_length=200, null=True)),
                ('teams', models.ManyToManyField(to='teams.Team')),
            ],
        ),
        migrations.CreateModel(
            name='ContestTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('creator', models.CharField(max_length=32)),
                ('languages', models.CharField(max_length=64)),
                ('contest_length', models.CharField(max_length=8)),
                ('time_penalty', models.CharField(max_length=4)),
                ('autojudge_enabled', models.BooleanField(max_length=1)),
                ('autojudge_review', models.CharField(max_length=128)),
                ('problem_description', models.CharField(max_length=128)),
                ('contest_admins', models.TextField()),
                ('contest_participants', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solution', models.FileField(max_length=128, upload_to=b'')),
                ('input_description', models.CharField(max_length=128)),
                ('output_description', models.CharField(max_length=128)),
                ('sample_input', models.FileField(max_length=128, upload_to=b'')),
                ('sample_output', models.FileField(max_length=128, upload_to=b'')),
                ('contest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contests.ContestTemplate')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('name', models.CharField(max_length=2048)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contests.Contest')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_file', models.FileField(blank=True, null=True, upload_to=b'uploads/')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contests.Question')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='teams.Team')),
            ],
        ),
    ]
