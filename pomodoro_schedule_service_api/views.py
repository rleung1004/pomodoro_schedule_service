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

        # delete old schedule #
        models.Schedule.objects.filter(userId=user_id).delete()

        user_commitments = list(models.Commitment.objects.filter(userId=user_id))
        user_goals = list(models.Goal.objects.filter(userId=user_id))
        # for testing print requests
        user_config = list(models.UserWeeklyConfig.objects.filter(user_id="1"))[0].weekly_config
        user_config = json.loads(user_config)

        priorities = set([goal.priority for goal in user_goals])
        user_goals = {priority: [goal for goal in user_goals if goal.priority == priority] for priority in priorities}
        user_config = {int(k): v for k, v in user_config.items()}
        sched = Scheduler.create_schedule(goals=user_goals, commitments=user_commitments, weekly_config=user_config)

        for sorted_dict in sched.values():
            for time, work_block in sorted_dict.items():
                schedule_table = models.Schedule()
                schedule_table.userId = user_id
                schedule_table.date = work_block.date.strftime("%Y-%m-%d"),
                schedule_table.time = str(time)
                schedule_table.name = work_block.name
                schedule_table.minutes = work_block.minutes
                schedule_table.is_goal = work_block.is_goal
                schedule_table.priority = work_block.priority if work_block.priority else -1
                schedule_table.save()

        # models.Commitment.objects.bulk_create(
        #     [
        #         models.Commitment(
        #             id="std",
        #             userId=user_id,
        #             location="",
        #             notes="",
        #             url="",
        #
        #             name="Morning Routine",
        #             repeats=json.dumps([x for x in range(7)]),
        #             startTime="2022-04-2 8:30:0",
        #             endDate="2022-10-3 8:30:0",
        #             minutes=30,
        #         ),
        #         models.Commitment(
        #             id="faslhio",
        #             userId=user_id,
        #             location="",
        #             notes="",
        #             url="",
        #
        #             name="Morning Poop",
        #             repeats=json.dumps([x for x in range(7)]),
        #             startTime="2022-04-2 8:30:0",
        #             endDate="2022-10-3 8:30:0",
        #             minutes=40,
        #         ),
        #         models.Commitment(
        #             id="dklfpohjsa",
        #             userId=user_id,
        #             location="",
        #             notes="",
        #             url="",
        #
        #             name="Lunch",
        #             repeats=json.dumps([x for x in range(7)]),
        #             startTime="2022-04-2 12:30:0",
        #             endDate="2022-10-3 8:30:0",
        #             minutes=30,
        #         ),
        #         models.Commitment(
        #             id="dkljhosfa",
        #             userId=user_id,
        #             location="",
        #             notes="",
        #             url="",
        #
        #             name="Dinner",
        #             repeats=json.dumps([x for x in range(7)]),
        #             startTime="2022-04-2 18:30:0",
        #             endDate="2022-10-3 8:30:0",
        #             minutes=30,
        #         ),
        #     ]
        # )

        # models.Goal.objects.bulk_create(
        #     [
        #         models.Goal(
        #             id="dhujklafhjasd",
        #             userId=user_id,
        #             location="",
        #             notes="",
        #             name="BIG DATA",
        #             totalTime=1200,
        #             timeLeft=1200,
        #             priority=0,
        #             endDate="2022-04-15 0:00:0",
        #             minTaskTime=15,
        #
        #         ),
        #         models.Goal(
        #             id="dsafpykhjl",
        #             userId=user_id,
        #             location="",
        #             notes="",
        #             name="ML",
        #             totalTime=1400,
        #             timeLeft=1400,
        #             priority=0,
        #             endDate="2022-04-15 0:00:0",
        #             minTaskTime=15,
        #
        #         ),
        #         models.Goal(
        #             id="dsklhhjja",
        #             userId=user_id,
        #             location="",
        #             notes="",
        #             name="Practice Yodelling",
        #             totalTime=2000,
        #             timeLeft=2000,
        #             priority=1,
        #             endDate="2022-10-15 0:00:0",
        #             minTaskTime=15,
        #         ),
        #     ]
        # )

        # models.UserWeeklyConfig.objects.bulk_create(
        #     [
        #         models.UserWeeklyConfig(user_id=user_id,
        #                         weekly_config=json.dumps({
        #                             "0": {
        #                                 "end": 1200,
        #                                 "start": 360,
        #                                 "breaks": [
        #                                     10,
        #                                     30
        #                                 ],
        #                                 "block_size": 50,
        #                                 "interleaves": 4
        #                             },
        #                             "1": {
        #                                 "end": 1200,
        #                                 "start": 420,
        #                                 "breaks": [
        #                                     10,
        #                                     30
        #                                 ],
        #                                 "block_size": 50,
        #                                 "interleaves": 4
        #                             },
        #                             "2": {
        #                                 "end": 1200,
        #                                 "start": 420,
        #                                 "breaks": [
        #                                     10,
        #                                     30
        #                                 ],
        #                                 "block_size": 50,
        #                                 "interleaves": 4
        #                             },
        #                             "3": {
        #                                 "end": 1200,
        #                                 "start": 360,
        #                                 "breaks": [
        #                                     10,
        #                                     30
        #                                 ],
        #                                 "block_size": 60,
        #                                 "interleaves": 4
        #                             },
        #                             "4": {
        #                                 "end": 1200,
        #                                 "start": 480,
        #                                 "breaks": [
        #                                     10,
        #                                     30
        #                                 ],
        #                                 "block_size": 60,
        #                                 "interleaves": 4
        #                             },
        #                             "5": {
        #                                 "end": 1080,
        #                                 "start": 600,
        #                                 "breaks": [
        #                                     60,
        #                                     120
        #                                 ],
        #                                 "block_size": 40,
        #                                 "interleaves": 2
        #                             },
        #                             "6": {
        #                                 "end": 1080,
        #                                 "start": 600,
        #                                 "breaks": [
        #                                     60,
        #                                     120
        #                                 ],
        #                                 "block_size": 30,
        #                                 "interleaves": 2
        #                             }
        #                         }))
        #     ]
        # )

        print("beans")
        # SAVE SCHEDULE #
        # schedule_table = models.Schedule()
        # schedule_table.userId = user_id
        # schedule_table.scheduleObj = json.dumps(schedule)
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
        # return HttpResponse(user_config, content_type='application/json')

        return HttpResponse(status=201)
