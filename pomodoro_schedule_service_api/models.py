from django.db import models
from datetime import datetime
import json


class Goal(models.Model):
    class Meta:
        db_table = "goal"

    @property
    def end(self):
        return datetime.strptime(self.endDate, "%Y-%m-%d %H:%M:%S").date()

    @property
    def total_time(self):
        return self.totalTime

    @property
    def time_left(self):
        return self.timeLeft

    @time_left.setter
    def time_left(self, value):
        self.timeLeft = value

    @property
    def min_task_time(self):
        return self.minTaskTime

    id = models.CharField(primary_key=True, max_length=36)
    userId = models.CharField(max_length=180)
    location = models.CharField(max_length=180)
    notes = models.CharField(max_length=180)

    name = models.CharField(max_length=180)
    totalTime = models.IntegerField()
    timeLeft = models.IntegerField()
    priority = models.IntegerField()
    endDate = models.CharField(max_length=180)
    minTaskTime = models.IntegerField(default=15)
    ignoreDeadline = models.BooleanField(default=False)

    def __eq__(self, other):
        return self.name == other.name


class Commitment(models.Model):
    class Meta:
        db_table = "commitment"

    @property
    def start(self):
        return datetime.strptime(self.startTime, "%Y-%m-%d %H:%M:%S")

    @property
    def end(self):
        return datetime.strptime(self.endDate, "%Y-%m-%d %H:%M:%S").date()

    @property
    def repeat(self):
        return json.loads(self.repeats)

    id = models.CharField(primary_key=True, max_length=36)
    userId = models.CharField(max_length=180)
    location = models.CharField(max_length=180)
    notes = models.CharField(max_length=180)
    url = models.CharField(max_length=180)

    name = models.CharField(max_length=180)
    repeats = models.JSONField()
    startTime = models.CharField(max_length=180)
    endDate = models.CharField(max_length=180)
    minutes = models.IntegerField()


class WorkBlock:
    def __init__(self, name: str, date: datetime, minutes: int, is_goal: bool, priority: int = None):
        self.name = name
        self.date = date
        self.minutes = minutes
        self.is_goal = is_goal
        self.priority = priority

    def __lt__(self, other):
        return self.date < other.date


class Schedule(models.Model):
    class Meta:
        db_table = "schedule"

    id = models.AutoField(primary_key=True)
    userId = models.CharField(max_length=180)
    date = models.CharField(max_length=180)
    time = models.CharField(max_length=180)

    name = models.CharField(max_length=180)
    minutes = models.IntegerField()
    isGoal = models.BooleanField()
    priority = models.IntegerField()


class UserConfig(models.Model):
    class Meta:
        db_table = "user_config"

    userId = models.CharField(max_length=180, primary_key=True)
    dayOfWeek = models.IntegerField()
    start = models.IntegerField()
    end = models.IntegerField()
    breaks = models.JSONField(default=[10, 30])
    blockSize = models.IntegerField(default=15)
    interleaves = models.IntegerField(default=3)


