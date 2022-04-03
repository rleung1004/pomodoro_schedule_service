import json
from datetime import datetime

from django.core import serializers
from django.http import HttpResponse, FileResponse
from pomodoro_schedule_service_api import models
from django.views.decorators.csrf import csrf_exempt

from pomodoro_schedule_service_api.scheduler import Scheduler


@csrf_exempt
def update_schedule(request):
    if request.method == 'POST':
        user_id = request.POST.get("user_id", "")
        user_commitments = list(models.Commitment.objects.all())
        user_goals = list(models.Goal.objects.all())
        # for testing print requests
        user_config = models.UserWeeklyConfig.objects.filter(user_id="userID")

        priorities = set([goal.priority for goal in user_goals])
        user_goals = {priority: [goal for goal in user_goals if goal.priority == priority] for priority in priorities}
        user_config = {int(k): v for k, v in user_config.items()}
        sched = Scheduler.create_schedule(goals=user_goals, commitments=user_commitments, weekly_config=user_config)
        print("beans")
        # SAVE SCHEDULE #
        # schedule_table = models.Schedule()
        # schedule_table.userId = user_id
        # schedule_table.scheduleObj = "JSON OBJ"
        # schedule_table.save()
        # SAVE SCHEDULE #

        # EDIT GOAL #
        # goal_edit = models.Goal.objects.get(userId=user_id)  # object to update
        # goal_edit.totalTimeInMinutes = 10 # update name
        # goal_edit.save()
        # EDIT GOAL #

        # DELETE DATA #
        # models.Commitment.objects.filter(userId=user_id).delete()
        # DELETE DATA #

        # add algorithm to create schedule and return json obj
        # also save schedule to db.
        return HttpResponse(user_config, content_type='application/json')
