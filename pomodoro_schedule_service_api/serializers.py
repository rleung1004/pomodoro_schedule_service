from rest_framework import serializers
from .models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        schedule_obj = ""
        # this will be schedule obj fields
        fields = ["userId", schedule_obj]