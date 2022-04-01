from django.db import models


class Schedule(models.Model):
    class Meta:
        db_table = "schedule"

    userId = models.CharField(max_length=180)
    scheduleObj = models.JSONField()


class Commitment(models.Model):
    class Meta:
        db_table = "commitment"

    class RepeatTypes(models.TextChoices):
        NEVER = 'NEVER'
        DAILY = 'DAILY'
        MON = 'MON'
        TUES = 'TUES'
        WED = 'WED'
        THUR = 'THUR'
        FRI = 'FRI'
        SAT = 'SAT'
        SUN = 'SUN'

    userId = models.CharField(max_length=180)
    location = models.CharField(max_length=180)
    name = models.CharField(max_length=180)
    notes = models.CharField(max_length=180)
    repeatType = models.CharField(
        max_length=6,
        choices=RepeatTypes.choices,
        default=RepeatTypes.NEVER,
    )
    url = models.CharField(max_length=180)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()


class Goal(models.Model):
    class Meta:
        db_table = "goal"

    class PriorityTypes(models.TextChoices):
        LOW = 'LOW'
        MEDIUM = 'MEDIUM'
        HIGH = 'HIGH'

    userId = models.CharField(max_length=180)
    location = models.CharField(max_length=180)
    name = models.CharField(max_length=180)
    notes = models.CharField(max_length=2000)
    url = models.CharField(max_length=180)
    priority = models.CharField(
        max_length=6,
        choices=PriorityTypes.choices,
        default=PriorityTypes.HIGH,
    )
    totalTimeInMinutes = models.IntegerField()
    deadline = models.DateTimeField()


class Request(models.Model):
    class Meta:
        db_table = "request"

    route = models.CharField(max_length=180)
    count = models.IntegerField()

