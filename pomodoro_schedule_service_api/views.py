from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pomodoro_schedule_service_api import models


class ScheduleApiView(APIView):

    def update(self, request, *args, **kwargs):
        '''
        Create/Update the Schedule for given user id
        '''
        user_id = request.data.get('userId')
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
        return requests
