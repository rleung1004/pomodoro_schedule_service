from django.db import models
from django.contrib.auth.models import User


class Schedule(models.Model):
    userId = models.CharField(max_length=180)
    scheduleObj = models.JSONField()

    def __str__(self):
        return self.scheduleObj
