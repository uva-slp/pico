# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-21 01:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='problem_description',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='sample_input',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='sample_output',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='solution',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='code_file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='result',
            field=models.CharField(choices=[('YES', 'Yes'), ('WRONG', 'Wrong Answer'), ('OFE', 'Output Format Error'), ('IE', 'Incomplete Error'), ('EO', 'Excessive Output'), ('CE', 'Compilation Error'), ('RTE', 'Run-Time Error'), ('TLE', 'Time-Limit Exceeded'), ('OTHER', 'Other-Contact Staff')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='state',
            field=models.CharField(choices=[('NEW', 'New'), ('YES', 'Yes'), ('NO', 'No')], default='NEW', max_length=20),
        ),
    ]
