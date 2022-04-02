from django.http import JsonResponse
from pomodoro_schedule_service_api import models
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def update_schedule(request):
    if request.method == 'POST':
        user_id = request.POST.get("user_id", "")
        user_commitments = models.Commitment.objects.filter(userId=user_id)
        user_goals = models.Goal.objects.filter(userId=user_id)
        # for testing print requests
        requests = models.Request.objects.all()
        print(requests)

        # SAVE SCHEDULE #
        # schedule_table = models.Schedule()
        # schedule_table.userId = ""
        # schedule_table.scheduleObj = ""
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
        return JsonResponse(requests)
