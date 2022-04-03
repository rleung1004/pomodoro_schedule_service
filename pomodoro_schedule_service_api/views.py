from django.core import serializers
from django.http import HttpResponse, FileResponse
from pomodoro_schedule_service_api import models
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def update_schedule(request):
    if request.method == 'POST':
        user_id = request.POST.get("user_id", "")
        user_commitments = list(models.Commitment.objects.all())
        user_goals = list(models.Goal.objects.all())
        # for testing print requests
        user_config = models.UserWeeklyConfig.objects.filter(user_id="userID")

        #
        # Entry.objects.bulk_create([
        #     Entry(headline="Django 1.0 Released"),
        #     Entry(headline="Django 1.1 Announced"),
        #     Entry(headline="Breaking: Django is awesome")
        # ])
        names = []
        models.Commitment.objects.bulk_create(
            models.Commitment(
                userId=user_id,

                name="Morning Routine",
                repeat=json.dumps([x for x in range(7)]),
                startTime=datetime.strptime('2022-04-2 8:30:0', "%Y-%m-%d %H:%M:%S"),
                endDate=datetime.strptime('2022-10-3 8:30:0', "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S"),
                minutes=30,

            )
        )

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
