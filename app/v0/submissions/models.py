from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import Group

from datetime import datetime


class Submission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    team = models.ForeignKey(Group, null=True)
    question = models.ForeignKey('contests.Question', null=True, on_delete=models.CASCADE)
    code_file = models.FileField(upload_to='uploads/', null=True, blank=True)
    timestamp = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return str(self.submission_id)
