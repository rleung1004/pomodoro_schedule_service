from django.db import models
from datetime import datetime
import json


class Goal(models.Model):
    class Meta:
        db_table = "goal"

    def get_end_date(self):
        return datetime.strptime(self.endDate, "%Y-%m-%d %H:%M:%S").date()

    id = models.CharField(primary_key=True, max_length=36)
    userId = models.CharField(max_length=180)
    location = models.CharField(max_length=180)
    name = models.CharField(max_length=180)
    notes = models.CharField(max_length=180)
    totalTime = models.IntegerField()
    timeLeft = models.IntegerField()
    priority = models.IntegerField()
    endDate = models.CharField(max_length=180)
    minTaskTime = models.IntegerField(default=15)

    def __eq__(self, other):
        return self.name == other.name


class Commitment(models.Model):
    class Meta:
        db_table = "commitment"

    def get_start_time(self):
        return datetime.strptime(self.startTime, "%Y-%m-%d %H:%M:%S")

    def get_end_date(self):
        return datetime.strptime(self.endDate, "%Y-%m-%d %H:%M:%S").date()

    def get_repeats(self):
        return json.loads(self.repeat)

    id = models.CharField(primary_key=True, max_length=36)
    userId = models.CharField(max_length=180)
    location = models.CharField(max_length=180)
    notes = models.CharField(max_length=180)
    url = models.CharField(max_length=180)

    name = models.CharField(max_length=180)
    repeat = models.JSONField()
    startTime = models.CharField(max_length=180)
    endDate = models.CharField(max_length=180)
    minutes = models.IntegerField()


class UserWeeklyConfig(models.Model):
    class Meta:
        db_table = "user_weekly_config"

    user_id = models.CharField(max_length=180, primary_key=True)
    weekly_config = models.JSONField()


class Schedule(models.Model):
    class Meta:
        db_table = "schedule"

    def get_work_blocks(self):
        return json.loads(self.work_blocks)

    user_id = models.CharField(max_length=180, primary_key=True)
    work_blocks = models.JSONField()